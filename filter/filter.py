from html.parser import HTMLParser
from bs4 import BeautifulSoup
import html2text
import sys
import os, os.path
import json
import datetime
from parser_ import Parser

sys.path.append(os.path.realpath('..'))

NOW = datetime.datetime.now()
# read data from this directory
READ_DIR = '../data/raw/'
# write data from this directory
WRITE_DIR = '../data/json/'


class Filter():

    @staticmethod
    def create_project_dir(directory):
        if not os.path.exists(directory):
            print('Create directory : ' + str(directory))
            os.makedirs(directory)
        else:
            print(directory + ' is already created !')

    @staticmethod
    def write_file(name, i, data):
        with open(WRITE_DIR + name + str(i) + '.json', 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False)

    def __init__(self):
        self.boot()
        self.filter_data()

    @staticmethod
    def boot():
        # create the directory if not empty
        Filter.create_project_dir(WRITE_DIR)

    def filter_data(self):
        # get number of files in directory
        export_files_length = len(
            [name for name in os.listdir(READ_DIR) if os.path.isfile(os.path.join(READ_DIR, name))])

        trustedreviews_parser = Parser()

        for filename in os.listdir(READ_DIR):
            with open(READ_DIR + filename, encoding='utf-8') as fp:
                if 'trustedreviews' in filename:
                    trustedreviews_parser.parseProductFromTrustedReviews(filename, fp)

                    if(trustedreviews_parser.get_data() != None):
                        self.write_file('trustedreviews', trustedreviews_parser.count, trustedreviews_parser.get_data())
                        trustedreviews_parser.count += 1
                else:
                    continue
