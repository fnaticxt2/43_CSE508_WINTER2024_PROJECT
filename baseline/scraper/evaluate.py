import PyPDF2
import csv
import os
from rank_bm25 import BM25Okapi
import string
from nltk.corpus import stopwords
import requests
import re 
import json 
from django.db import connection
import time
from datetime import datetime, timedelta
import pickle
from rank_bm25 import BM25Okapi
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from llamaapi import LlamaAPI
from decouple import config
import mysql.connector
import pandas as pd
import heapq
import time

lemmatizer = WordNetLemmatizer()

today = datetime.now().date()
date_list = []
for i in range(7):
    date = today - timedelta(days=i)
    date_list.append(date.strftime('%Y-%m-%d'))

folder_path = '../backend/jobfinder/processed'
pickle_files = [file for file in os.listdir(folder_path) if file.endswith('.pkl') and file[:10] in date_list]
pickle_files = sorted(pickle_files, key=lambda x: datetime.strptime(x[:10], '%Y-%m-%d'), reverse=True)
merged_tokens = []
for file_name in pickle_files:
    with open(os.path.join(folder_path, file_name), 'rb') as f:
        bm25_object = pickle.load(f)
        merged_tokens.extend(bm25_object)

bm25 = BM25Okapi(merged_tokens)

connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='ir_job'
    )


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


def llm_api_request(text):
    llama = LlamaAPI("LL-oanhxM5VqtkyRqeSwAJnUbitkD0Psq6KPBy0VLsLATxm84d2KHU7tAjy5XtMzdVL")
    api_request_json = {
        "model": "llama3-70b",
        "messages": [
            {"role": "user", "content": text+" Extract skill tokens, form this resume text that should follow the format. 1) Atmost 20 and atleast 2 tokens for primary skills. 2) Atmost 8 tokens secondary skill. 3) Atmost 6 and atleast 1 educational background degree and college. 4) Atmost 6 latest sentences for past experience. 5) Atleast 2 and Atmost 5 soft skills. 6) Atmost 2 location token of candidate city. 7) Atmost 5 token for hobbies. 8) Atmost 4 tokens for explaining the users personality or uniqueness. Response Format: {'primary_skills': ['Token 1','Token 2',..],'secondary_skills': ['Token 3','Token 4',..],'latest_education': ['Token 5'], 'past_experience': ['Token 6',...],'soft_skills': ['Token 7',...],'location': ['Token 8',...],'hobbies': ['Token 9',...],  'personality_uniqueness': ['Token 10',...]}. Note: if the tokens do not exist then return None this should be returned in a non changeable json format for sake of uniformity, so any more resume text that i give should be returned in this format only. And most important Just send JSON data in response no other text. Just give JSON response in pain text no object and no other text. Don't give None insted give blank str '' token"},
        ]
    }
    try:
        response = llama.run(api_request_json)
        print(response.json())
        return response.json()
    except Exception as e:
        print("An error occurred:", e)
    
    return False

df = pd.read_csv("random_records4.csv")
df[f'processed'] = ""
for i in range(1, 11):
    df[f'job_{i}'] = ""
if connection.is_connected():
    print("Connected to MySQL database")


    with connection.cursor() as cursor:
        sql_query = "SELECT * FROM jobs WHERE DATE(posted_on) IN ({}) ORDER BY posted_on DESC".format(', '.join(['%s'] * len(date_list)))
        cursor.execute(sql_query, date_list)
        jobdata = cursor.fetchall()
        for rowindex, row in df.iterrows():
            print("Row "+str(rowindex+1))
            Resumetext = row['Resume']

            iteration = 1
            while iteration <= 10:
                print("Trying request "+str(iteration))
                token_raw = llm_api_request(Resumetext)
                iteration = iteration + 1
                if token_raw:
                    break
                time.sleep(2)
            if not token_raw:
                print(Resumetext)
                continue
            tokens_str = token_raw["choices"][0]["message"]["content"]
            match = re.search(r'\{[^{}]+\}', tokens_str)
            json_data_str = match.group()
            json_data = json.loads(json_data_str)

            resume_string=""
            for key, value in json_data.items():
                if value:
                    value_str = " ".join(value)
                    resume_string += value_str+" , "
            tokenized_resume = preprocess_text_pipeline(resume_string)
            bm25_scores = bm25.get_scores(tokenized_resume)
            top10_indices = heapq.nlargest(10, range(len(bm25_scores)), key=bm25_scores.__getitem__)

            finaldata = []
            colno = 1
            df.loc[rowindex, 'processed'] = " ".join(tokenized_resume)
            for i in top10_indices:
                #print(jobdata[i])
                jobrow = list(jobdata[i])
                df.loc[rowindex, f'job_{colno}'] = jobrow[7] + ", skills: " + jobrow[4] + ", jd: " + jobrow[5] + ", others: " + jobrow[4]
                colno = colno + 1

df.to_csv('evaluation4.csv', index=False)