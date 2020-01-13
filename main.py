#!/usr/bin/python3.7

import sched
import time
import argparse
import os
import sys
import logging
from datetime import datetime
from config import *
from process_image import apply_harper_collins_logo
import xlrd
import twitter

def tweet(book_data, twitter, logger):
    """
    Send a tweet using the provided book data tuple,
    twitter API instance, and logger
    """
    id, text, image, _ = book_data
    if len(text) > 280:
        logger.error(f'Message is too long to be tweeted,'
                ' not generating tweet for book: {id}')
        return
    logger.info(f'Generating tweet for book: {id}')
    image_bytes = apply_harper_collins_logo(image)
    twitter.PostUpdate(status=text, media=image_bytes)

def extract_book_info(row):
    """
    Given an excel row object, return the book info
    contained in the row, in tuple form
    """
    id, text, image_url, date = row
    return (id.value, text.value, image_url.value, 
            xlrd.xldate.xldate_as_tuple(date.value, 0))

if __name__ == '__main__':
    logging.basicConfig(filename='tweet_scheduler.log', filemode='w', 
            format='%(asctime)s - %(name)s - %(message)s',
            level=logging.INFO)

    # Add an argument to allow this script to be run as a daemon in the background
    arg_parser = argparse.ArgumentParser(description='Tweet scheduler')
    arg_parser.add_argument('--daemon', default=False, const=True,
                            action='store_const', dest='daemon')

    args = arg_parser.parse_args()
    run_as_daemon = args.daemon

    # If run with --daemon, fork and kill the original process
    if run_as_daemon:
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as err:
            logging.error(f'Failed to execute fork: {err}')
            sys.exit(1)

    current_row = 1
    data_sheet = xlrd.open_workbook('data_table.xlsx').sheets()[0]
    number_of_rows = data_sheet.nrows
    s = sched.scheduler(time.time, time.sleep)
    next_tweet_time = datetime.min
    twitter = twitter.api.Api(consumer_key=CONSUMER_KEY,
                          consumer_secret=CONSUMER_SECRET,
                          access_token_key=ACCESS_TOKEN,
                          access_token_secret=ACCESS_TOKEN_SECRET)

    while current_row < number_of_rows:

        now = datetime.now()

        # Keep searching through the rows until we find one with a tweet time
        # later than the present time
        while next_tweet_time < now and current_row < number_of_rows:
            row = data_sheet.row(current_row)
            extracted_book_info = extract_book_info(row)
            next_tweet_time = datetime(*extracted_book_info[-1])
            current_row += 1

        if current_row > number_of_rows:
            break

        logging.info(f'Waiting until {next_tweet_time} to send next tweet')

        # Get the total number of seconds in the time delta between 
        # the desired send date and now, so we can pass it to sched
        time_to_sleep = (next_tweet_time - now).total_seconds()

        s.enter(time_to_sleep, 1, tweet, argument=(extracted_book_info, twitter, logging))
        s.run()

    logging.info('No more tweets left to send, exiting')
    raise SystemExit
