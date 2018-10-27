# encoding=utf8

from html.parser import HTMLParser
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from urllib import parse
import sys
import os, os.path
import urllib

sys.path.append(os.path.realpath('..'))

# save to this directory
READ_DIR = '../data/url/'

WRITE_DIR = '../data/raw/'

def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Create directory : ' + directory)
        os.makedirs(directory)
    else:
        print(directory + ' is already created !')


def writeFile(provider, soup, i):
    with open(WRITE_DIR + provider + "_" + str(i) + '.html', 'w', encoding='utf-8') as the_file:
        the_file.write(str(soup))


def parser_main():
    # create the directory if not empty
    create_project_dir(WRITE_DIR)

    headers = {'User-Agent': 'User-Agent:Mozilla/5.0'}

    with open(READ_DIR + "all_links.csv") as fp:
        i = 0

        for url in fp:
            print("Processing file " + str(url))

            try:
                dataTemp = urllib.request.Request(url, headers=headers)
                data = urllib.request.urlopen(dataTemp).read()
                soup = BeautifulSoup(data, "lxml")
                writeFile('trustedreviews', soup, i)

                i += 1
            except HTTPError as e:
                # do something
                print('Error code: ', e.code)
            except URLError as e:
                # do something
                print('Reason: ', e.reason)


if __name__ == "__main__":
    parser_main()
