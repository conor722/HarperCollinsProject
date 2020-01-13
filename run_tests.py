#!/usr/bin/python3.7
import unittest
import xlrd
from main import extract_book_info

class TestTweetScheduler(unittest.TestCase):
    def setUp(self):
        self.sheet = xlrd.open_workbook('data_table.xlsx').sheets()[0]

    def test_extract_book_info(self):
        """
        Test the return values of he extract_book_info function
        """
        number_of_rows = self.sheet.nrows
        counter = 1
        while counter < number_of_rows:
            row = self.sheet.row(counter)
            id, text, text2, date_tuple = extract_book_info(row)
            self.assertIsInstance(id, float)
            self.assertIsInstance(text, str)
            self.assertIsInstance(text2, str)
            self.assertIsInstance(date_tuple, tuple)
            counter += 1

if __name__ == '__main__':
    unittest.main()
