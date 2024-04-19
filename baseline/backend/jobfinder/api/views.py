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

class UploadPDF(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
#        csv_file_path = os.path.join(os.path.dirname(__file__), '08-03-2023.csv')

        if not request.FILES.get('resume'):
            return JsonResponse({'error': 'No file attached'}, status=400)

        pdf_file = request.FILES['resume']

        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ''
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
                text += page.extract_text()
            text = text.replace("\n", " ")
            print(text)
            print("GPT")
            token_raw = self.llm_api_request(text)
            print(token_raw)
            print(token_raw["results"])
            print(token_raw["results"][0])
            print(token_raw["results"][0]["generated_text"])
            tokens_str = token_raw["results"][0]["generated_text"]
            print("After")
            match = re.search(r'\{[^{}]+\}', tokens_str)
            print(match)
            resume_string=""
            if match:
                print("Test2")
                json_data_str = match.group()
                print("Test3")
                print(json_data_str)
                json_data = json.loads(json_data_str)
                print(json_data)
                for key, value in json_data.items():
                    print(key)
                    #resume_string += key + ": "
                    if value:
                        value_str = " ".join(value)
                        resume_string += value_str+" , "
            else:
                print("JSON object not found in the provided string.")
                return JsonResponse({'error': "Object not found in the provided string."}, status=400)
            print("\n\n"+resume_string+"\n\n")
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM jobs")
                jobdata = cursor.fetchall()
                job_descriptions = [row[12] for row in jobdata]
                
                # Preprocess job descriptions
                processed_job_descriptions = []
                for desc in job_descriptions:
                    processed_job_descriptions.append(desc)
                
                # Tokenize the processed job descriptions
                tokenized_job_descriptions = [desc.split() for desc in processed_job_descriptions]
                start_time = time.time()
                # Create BM25 object
                bm25 = BM25Okapi(tokenized_job_descriptions)
                end_time = time.time()

                execution_time = end_time - start_time

                print("BM25Okapi constructor took {:.2f} seconds to execute.".format(execution_time))
                
                # Tokenize user resume and remove stopwords, punctuations, and specified characters
                processed_resume = self.preprocess_text(resume_string)
                tokenized_resume = processed_resume.split()
                print(tokenized_resume)
                # Get BM25 scores
                bm25_scores = bm25.get_scores(tokenized_resume)
                print(bm25_scores)
                # Get indices of top 10 scores
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
        # Remove stopwords, punctuations, and specified characters
        stop_words = set(stopwords.words('english'))
        punctuation_chars = set(string.punctuation)
        specified_chars = {'.', ';',':','-'," "}
        processed_text = ' '.join([word.lower() for word in text.split() if word.lower() not in stop_words and word.lower() not in punctuation_chars and word.lower() not in specified_chars])
        return processed_text
  
    def llm_api_request(self, text):
        api_url = 'https://api.deepinfra.com/v1/inference/mistralai/Mixtral-8x7B-Instruct-v0.1'
        data = {
            "input": "[INST] "+text+" Extract skill tokens, form this resume text that should follow the format. 1) Atmost 20 and atleast 2 tokens for primary skills. 2) Atmost 8 tokens secondary skill. 3) Atmost 6 and atleast 1 educational background degree and college. 4) Atmost 6 latest sentences for past experience. 5) Atleast 2 and Atmost 5 soft skills. 6) Atmost 2 location token of candidate city. 7) Atmost 5 token for hobbies. 8) Atmost 4 tokens for explaining the users personality or uniqueness. Response Format: {'primary_skills': ['Token 1','Token 2',..],'secondary_skills': ['Token 3','Token 4',..],'latest_education': ['Token 5'], 'past_experience': ['Token 6',...],'soft_skills': ['Token 7',...],'location': ['Token 8',...],'hobbies': ['Token 9',...],  'personality_uniqueness': ['Token 10',...]}. Note: if the tokens do not exist then return None this should be returned in a non changeable json format for sake of uniformity, so any more resume text that i give should be returned in this format only. And most important Just send JSON data in response no other text. Just give JSON response in pain text no object and no other text [/INST] "
        }

        # Headers to be included in the request
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eAYc9lZHAZfnRcngYxSRnx18nMrabzJk'
            # Add any other headers as needed
        }

        try:
            # Making a POST request to the API endpoint with headers
            response = requests.post(api_url, json=data, headers=headers)

            # Checking if the request was successful (status code 200)
            if response.status_code == 200:
                print(response.json())
                return response.json()
            else:
                return False
                print(f"Request failed with status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            return False
            # Handle exceptions if the request fails
            print(f"Request failed: {e}")