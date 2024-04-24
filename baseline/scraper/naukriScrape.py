import requests
import json
from datetime import datetime, timedelta
import time

import pandas as pd
import requests
from urllib.parse import urlparse
import nltk
import re
import string
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import StandardScaler
from bs4 import BeautifulSoup
import mysql.connector
import os
from rank_bm25 import BM25Okapi
import warnings

warnings.filterwarnings("ignore", category=UserWarning, message="MarkupResemblesLocatorWarning")
"""
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
"""
def lowercase_text(text):
    return text.lower()

def removeHTML(text):    
    try:
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text()
    except:
        return text

def tokenize_text(text):   
    return word_tokenize(text)

def remove_stopwords(tokens):
    return [word for word in tokens if word not in stopwords.words('english')]

def remove_punctuations(tokens):  
    pattern = re.compile(f'[{re.escape(string.punctuation)}]')
    return [word for word in tokens if not pattern.search(word)]

def remove_blank_tokens(tokens):  
    return [word for word in tokens if word.strip()]


def lemmatize_tokens(tokens):   
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word) for word in tokens]

def preprocess_text_pipeline(text):
    if not isinstance(text, str):
        return [] 

    text = lowercase_text(text)
    text = removeHTML(text)
    tokens = tokenize_text(text)
    tokens = remove_stopwords(tokens)
    tokens = remove_punctuations(tokens)
    tokens = remove_blank_tokens(tokens)
    tokens = lemmatize_tokens(tokens)
    return tokens

servername = "localhost"
username = "root"
password = ""
database = "ir_job"

conn = mysql.connector.connect(
    host=servername,
    user=username,
    passwd=password,
    database=database
)

if not conn.is_connected():
    print("Error: Not Connected to MySQL database")

folder_path = '../backend/jobfinder/processed'
file_names = os.listdir(folder_path)
date_list = []
for file_name in file_names:
    base_name, extension = os.path.splitext(file_name)
    date_list.append(str(base_name))

cursor = conn.cursor()
sql_query = "SELECT * FROM jobs ORDER BY posted_on DESC"
cursor.execute(sql_query)
results = cursor.fetchall()
allprocesseddata = {}
for row in results:
    processed_tokens = preprocess_text_pipeline(f"{row[4]} {row[5]} {row[6]}")
    date = row[9].date()
    if str(date) in date_list:
        continue
    if str(date) not in allprocesseddata:
        allprocesseddata[str(date)] = []
    allprocesseddata[str(date)].append(processed_tokens)
for date, tokens_list in allprocesseddata.items():
    pickle.dump(tokens_list, open(folder_path+"/"+date+".pkl", "wb"))

cursor.close()
conn.close()