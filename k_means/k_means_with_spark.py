from __future__ import print_function
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
# from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import math
import json
import re
import sys
import string
import os.path
import unicodedata
import pandas as pd

from pyspark.mllib.clustering import KMeans
from numpy import array, random
from math import sqrt
from pyspark import SparkConf, SparkContext
from sklearn.preprocessing import scale

from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.feature import HashingTF, Tokenizer
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

# apple 0, samsung 1, xiaomi 2, google 3, other 4

X = []
y = []
# create if-tdf vector
vectorizer = TfidfVectorizer(use_idf=True, min_df=1, stop_words='english', sublinear_tf=True, encoding='utf-8')

def getOnlyLetter(input_text):
    output_text = " ".join(re.findall("[a-zA-Z]+", input_text))
    return output_text

def getInputData():
    # input must be list of string
    text = ["Samsung is number one, galaxy s9 awesome"]
    result = vectorizer.fit_transform(text).toarray()
    return result

def createClusteredData():
    READ_DIR = './json/'

    count = 0
    for subdir, dirs, files in os.walk(READ_DIR):   # walks through whole directory
        print(len(files))

        for file in files:
            filepath = os.path.join(subdir, file)  # path to the file

            with open(filepath) as f:
                # read the json file
                data = json.loads(f.read())

                # get description
                description = data['description']

                result = data['result']

                # clean data
                description = getOnlyLetter(description)

                # check if contain not null
                if(description != ''):
                    # all description in single array
                    X.append(description)
                    y.append(result)
                    
    # apply to current array
    words = vectorizer.fit_transform(X).toarray()

    return words

def get_distance(clusters):
    def get_distance_map(record):
        cluster = clusters.predict(record)
        centroid = clusters.centers[cluster]
        dist = np.linalg.norm(record - centroid)
        return (dist, record)
    return get_distance_map

def main():

    K=5

    # Boilerplate Spark stuff:
    conf = SparkConf().setMaster("local").setAppName("SparkKMeans")
    sc = SparkContext(conf = conf)

    data = sc.parallelize(scale(createClusteredData()))

    # split train vs test data 
    #train_data, test_data = data.randomSplit([2, 3], 17)

    # Build the model (cluster the data)
    clusters = KMeans.train(data, K, maxIterations=10,
            runs=10, initializationMode="random")

    # Print out the cluster assignments
    resultRDD = data.map(lambda point: clusters.predict(point)).cache()

    print("Cluster assignments:")
    results = resultRDD.collect()

    for idx, row in enumerate(results):
        print(str(idx) + ": / Kmeans predict: " + str(row) + "/ Actual: " + str(y[idx]) + "/ Short document " + str(X[idx])[0:50])

    #print(results)

if(__name__== "__main__"):
    main()