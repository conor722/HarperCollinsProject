## Method used

The method used is to iterate through the rows in the excel data sheet, until we find a book with a tweet date that is in the future. The process then sleeps until that date, when it awakes it sends the tweet. This assumes that the Tweets in the sheet are in chronological order, an improvement would be to pre-process the list and order them by the date the tweets should be sent.

The script can be run as a daemon with --daemon, as this is how it would probably be used in production.

I cut the text off from the provided logo to match the example in the Excel sheet, as the text clashed with some of the covers.

I used the commonly used PIL library to process the image, the requests library for getting the image data, an excel reader library, and a Twitter API library to avoid manually generating OAuth signatures.

## Things I would improve on

Adding things like function annotations.

Error handling is minimal at the moment, things like incorrect image URLs would cause requests to throw an Exception which would end the running of the script, even if other URLs were correct. 

The approach is entirely function based, another approach may have been to create some kind of Twitter Update class which contained the book data, which could incorporate error handling and post methods.

The approach might not work if Tweets are scheduled to be sent very close to eachother, as by the time one had finished, the other's date would now be in the past. This could be fixed by adding the posts to some kind of queue or forking before sending the tweet.

More tests - due to the network and time based nature of the script, it would probably require some kind of mock framework to unit test it properly.

## Things that went well

I believe the basic structure of the __main__ loop is easy to understand and uses the Python standard library for scheduling, rather than something more complex.

The addition of the --daemon argument along with the logging framework means it can be run in the background, with logging output monitored or checked periodically. 

Use of a pre-existing Twitter API library to simplify the OAuth process.

## How to run the script 

### Note - I have replaced the secrets in the config file with empty strings

pip3 install -r requirements.txt

./main.py [-h] [--daemon]


