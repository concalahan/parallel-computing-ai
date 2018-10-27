# -*- coding: utf-8 -*-

from __future__ import print_function
# from __future__ import division, unicode_literals
from textblob import TextBlob as tb
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.cluster import KMeans
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from numpy import array
import math
import json
import re
import sys
import string
import os.path
import unicodedata
import pandas as pd

save_path = os.path.expanduser('~') + '/Code/ML/python/clustering/data/'

patterns = {
    '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
    '[đ]': 'd',
    '[èéẻẽẹêềếểễệ]': 'e',
    '[ìíỉĩị]': 'i',
    '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
    '[ùúủũụưừứửữự]': 'u',
    '[ỳýỷỹỵ]': 'y'
}

def convert(text):
    """
    Convert from 'Tieng Viet co dau' thanh 'Tieng Viet khong dau'
    text: input string to be converted
    Return: string converted
    """
    output = text
    for regex, replace in patterns.items():
        output = re.sub(regex, replace, output)
        # deal with upper case
        output = re.sub(regex.upper(), replace.upper(), output)
    return output

def clean_text(text):
    # to lower case character
    text = text.lower()

    # invalid character
    text = text.replace("{","")
    text = text.replace("}","")
    text = text.replace(",","")
    text = text.replace(":","")

    # skip enter and tab
    text = text.replace("\n"," ")
    text = text.replace("\t"," ")

    # skip large space
    text = re.sub(' +',' ',text)

    # return cleaned text
    return text

# write a file to disk
def write_file(text, pattern, count):
    completeName = os.path.join(save_path, pattern + str(count) + ".txt")
    file = open(completeName, 'w')
    file.write(text.encode('utf-8')) # .encode('utf-8')
    file.close()

# get content of a file
def file_get_contents(filename):
    with open(filename) as f:
        return f.read()

# label X for training data
def create_tf_idf(max_count):
    fileList = [save_path + "document_" + str(i) + ".txt" for i in range(1,max_count)]
    X = TfidfVectorizer(input="filename", encoding='utf-8').fit_transform(fileList).toarray()
    return X

# label y for training data; create (n,1) matrix
def expect_result(max_count):
    y= np.array([])
    for i in range(1,max_count):
        y = np.append(y, file_get_contents(save_path + "result_" + str(i) + ".txt"))
    return y

# return number to given category
def article_type_to_number(y):
    y = convert(y).lower()
    if(y == 'phong thuy'):
        return 1
    elif(y == 'kinh doanh'):
        return 2
    elif(y == 'the thao'):
        return 3
    else:
        return 0

if __name__ == '__main__':
    # client = MongoClient('mongodb://localhost:27017/')
    # db = client['locatefamily']
    # collection = db['articles']
    # rows = collection.find({})

    # max article to crawl
    MAX_ROW = 300

    with open('articles.json') as json_data:
        articles = json.load(json_data)
        count=1
        for article in articles:
            if(count == MAX_ROW+1):
                break

            # make sure the content is clean
            _article = clean_text(article['content'])

            # classify the category and convert it to number
            _article_category = article_type_to_number(unicodedata.normalize('NFKD', article['type']).encode('ascii','ignore'))

            write_file(_article, "document_", count)
            write_file(str(_article_category), "result_", count)
            count=count+1

    X = create_tf_idf(MAX_ROW)
    y = expect_result(MAX_ROW)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # private vs public
    lr = LinearRegression()

    lr.fit(X_train, y_train)

    # convert to int
    tempY = [ int(x) for x in y ]

    # convert to numpy array
    y = array( tempY )

    print(lr.coef_)
    print(lr.intercept_)

    y_pred = lr.predict(X_test)

    df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred } )
    print(df)