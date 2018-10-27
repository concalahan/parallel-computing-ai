# encoding=utf8

import csv
import scrapy
from scrapy.linkextractors import LinkExtractor
import sys
import os, os.path
import re

sys.path.append(os.path.realpath('..'))

# save to this directory
WRITE_DIR = '../data/url/'

class RustSpider(scrapy.Spider):
    name = "rust"
    isCreateFolder = False
    export_urls = []

    # add domain here
    allowed_domains = ["stream-hub.com"]
    start_urls = (
        'http://stream-hub.com/',
    )

    def create_project_dir(self, directory):
        # delete file if exist
        if os.path.exists(WRITE_DIR + 'all_links.csv'):
            os.remove(WRITE_DIR + 'all_links.csv')
        else:
            print("The file does not exist") 

        # create folder if not exist
        if not os.path.exists(directory):
            print('Create directory : ' + directory)
            os.makedirs(directory)
        else:
            print(directory + ' is already created !')

    def parse(self, response):
        
        if(self.isCreateFolder == False):
            # create save data directory once
            self.create_project_dir(WRITE_DIR)
            self.isCreateFolder = True

        extractor = LinkExtractor(allow_domains='stream-hub.com')
        links = extractor.extract_links(response)
        items = []
        
        with open(WRITE_DIR + 'all_links.csv', 'a') as file:
            # write to last row
            for link in links:
                # remove stupid character in url
                tempLink = link.url.split('#', 1)[0]
                
                if(tempLink not in self.export_urls):
                    print("Process " + tempLink)

                    # write to file
                    file.write(tempLink)

                    # insert new line
                    file.write('\n')

                    # add to existing array
                    self.export_urls.append(tempLink)

                    # go to next link
                    yield response.follow(tempLink, callback=self.parse)

        