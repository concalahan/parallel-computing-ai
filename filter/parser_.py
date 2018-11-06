from html.parser import HTMLParser
from bs4 import BeautifulSoup
import html2text
import sys
import os, os.path
import json
import datetime
import re
import urllib

NOW = datetime.datetime.now()


class Parser():
    def __init__(self):
        super().__init__()
        self.data = {}
        # Count var is to index in Filter
        self.count = 0

    @staticmethod
    def json_serial(obj):
        """JSON serializer for objects not serializable by default json code"""

        if type(obj) is datetime.date or type(obj) is datetime.datetime:
            return obj.isoformat()
        raise TypeError("Type %s not serializable" % type(obj))

    @staticmethod
    def exact_number(paragraph):
        result = []
        for s in paragraph:
            if s.isdigit():
                result.append(s)

        result = ''.join(str(i) for i in result)
        return result

    def get_data(self):
        return self.data

    def parseProductFromTrustedReviews(self, filename, fp):
        soup = BeautifulSoup(fp, 'lxml')

        # HTML2Text: for exact text from html
        h = html2text.HTML2Text()

        # delete .html
        filenameNotHtml = filename[:-5]

        # all sites share this
        url = soup.findAll("link", {"rel": "canonical"})

        title = soup.findAll("title")

        # if no canonical url found, skip the iteration
        if len(url) == 0:
            return

        description_temp = soup.findAll("div", {"class": "post-main__inner"})

        product_description = ''
        if len(description_temp) != 0:
            product_description = h.handle(str(description_temp[0]))

        self.data['result'] = 0
        self.data['title'] = title[0].text
        self.data['description'] = product_description