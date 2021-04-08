from pyspark import SparkContext, SparkConf, SQLContext
from datetime import datetime, timedelta
import pyspark.sql.functions as F
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.sql import Window
from pymongo import MongoClient
import pandas as pd

appName = "PySpark Extract T24"
master = "local"

conf = SparkConf() \
        .setAppName(appName) \
        .setMaster(master) \
        .set("spark.executor.memory", "8g") \
        .set("spark.driver.memory", "8g")


sc = SparkContext.getOrCreate(conf=conf)
sqlContext = SQLContext(sc)
spark = sqlContext.sparkSession

def process_tweets():
    client = MongoClient('localhost:27017')
    db = client.twitterdb