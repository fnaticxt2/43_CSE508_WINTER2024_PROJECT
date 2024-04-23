from django.shortcuts import render
import PyPDF2
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
import csv
import os
import heapq
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

lemmatizer = WordNetLemmatizer()



class UploadPDF(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):

        if not request.FILES.get('resume'):
            return JsonResponse({'error': 'No file attached'}, status=400)

        pdf_file = request.FILES['resume']

        today = datetime.now().date()
        date_list = []
        for i in range(7):
            date = today - timedelta(days=i)
            date_list.append(date.strftime('%Y-%m-%d'))

        folder_path = 'processed'
        pickle_files = [file for file in os.listdir(folder_path) if file.endswith('.pkl') and file[:10] in date_list]
        pickle_files = sorted(pickle_files, key=lambda x: datetime.strptime(x[:10], '%Y-%m-%d'), reverse=True)

        merged_tokens = []
        for file_name in pickle_files:
            with open(os.path.join(folder_path, file_name), 'rb') as f:
                bm25_object = pickle.load(f)
                merged_tokens.extend(bm25_object)
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ''
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
                text += page.extract_text()
            text = text.replace("\n", " ")
            iteration = 1
            while iteration <= 10:
                print("Trying request "+str(iteration))
                token_raw = self.llm_api_request(text)
                iteration = iteration + 1
                if token_raw:
                    break
            print(token_raw)
            tokens_str = token_raw["choices"][0]["message"]["content"]
            print(tokens_str)
            json_data = json.loads(tokens_str)
            print(json_data)
            #match = re.search(r'\{[^{}]+\}', tokens_str)
            resume_string=""
            for key, value in json_data.items():
                if value:
                    value_str = " ".join(value)
                    resume_string += value_str+" , "
            print(resume_string)
            with connection.cursor() as cursor:
                sql_query = "SELECT * FROM jobs WHERE DATE(posted_on) IN ({}) ORDER BY posted_on DESC".format(', '.join(['%s'] * len(date_list)))
                cursor.execute(sql_query, date_list)
                jobdata = cursor.fetchall()
                start_time = time.time()
                bm25 = BM25Okapi(merged_tokens)
                end_time = time.time()

                execution_time = end_time - start_time

                print("BM25Okapi constructor took {:.2f} seconds to execute.".format(execution_time))
                
                tokenized_resume = self.preprocess_text_pipeline(resume_string)
                #tokenized_resume = processed_resume.split()
                start_time = time.time()
                bm25_scores = bm25.get_scores(tokenized_resume)
                end_time = time.time()
                execution_time = end_time - start_time
                print("bm25_scores took {:.2f} seconds to execute.".format(execution_time))
                print(bm25_scores)
                top10_indices = heapq.nlargest(10, range(len(bm25_scores)), key=bm25_scores.__getitem__)
                
                print(top10_indices)
                finaldata = []
                for i in top10_indices:
                    print(jobdata[i])
                    jobrow = list(jobdata[i])
                    jobrow.append(bm25_scores[i])
                    finaldata.append(jobrow)
                print(finaldata)
                
                return JsonResponse({'data': finaldata}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def preprocess_text(self, text):
        stop_words = set(stopwords.words('english'))
        punctuation_chars = set(string.punctuation)
        specified_chars = {'.', ';',':','-'," "}
        processed_text = ' '.join([word.lower() for word in text.split() if word.lower() not in stop_words and word.lower() not in punctuation_chars and word.lower() not in specified_chars])
        return processed_text
  
    def llm_api_request(self, text):
        llama = LlamaAPI(config('API_KEY'))
        api_request_json = {
            "model": "llama3-70b",
            "messages": [
                {"role": "user", "content": text+" Extract skill tokens, form this resume text that should follow the format. 1) Atmost 20 and atleast 2 tokens for primary skills. 2) Atmost 8 tokens secondary skill. 3) Atmost 6 and atleast 1 educational background degree and college. 4) Atmost 6 latest sentences for past experience. 5) Atleast 2 and Atmost 5 soft skills. 6) Atmost 2 location token of candidate city. 7) Atmost 5 token for hobbies. 8) Atmost 4 tokens for explaining the users personality or uniqueness. Response Format: {'primary_skills': ['Token 1','Token 2',..],'secondary_skills': ['Token 3','Token 4',..],'latest_education': ['Token 5'], 'past_experience': ['Token 6',...],'soft_skills': ['Token 7',...],'location': ['Token 8',...],'hobbies': ['Token 9',...],  'personality_uniqueness': ['Token 10',...]}. Note: if the tokens do not exist then return None this should be returned in a non changeable json format for sake of uniformity, so any more resume text that i give should be returned in this format only. And most important Just send JSON data in response no other text. Just give JSON response in pain text no object and no other text"},
            ]
        }
        try:
            response = llama.run(api_request_json)
            print(response.json())
            return response.json()
        except Exception as e:
            print("An error occurred:", e)
        
        return False

    
    def lowercase_text(self, text):
        return text.lower()

    def removeHTML(self, text):    
        try:
            soup = BeautifulSoup(text, "html.parser")
            return soup.get_text()
        except:
            return text

    def tokenize_text(self, text):   
        return word_tokenize(text)

    def remove_stopwords(self, tokens):
        return [word for word in tokens if word not in stopwords.words('english')]

    def remove_punctuations(self, tokens):  
        pattern = re.compile(f'[{re.escape(string.punctuation)}]')
        return [word for word in tokens if not pattern.search(word)]

    def remove_blank_tokens(self, tokens):  
        return [word for word in tokens if word.strip()]


    def lemmatize_tokens(self, tokens):   
        return [lemmatizer.lemmatize(word) for word in tokens]

    def preprocess_text_pipeline(self, text):
        if not isinstance(text, str):
            return [] 

        text = self.lowercase_text(text)
        text = self.removeHTML(text)
        tokens = self.tokenize_text(text)
        tokens = self.remove_stopwords(tokens)
        tokens = self.remove_punctuations(tokens)
        tokens = self.remove_blank_tokens(tokens)
        tokens = self.lemmatize_tokens(tokens)
        return tokens