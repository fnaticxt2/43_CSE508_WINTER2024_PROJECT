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

class UploadPDF(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        csv_file_path = os.path.join(os.path.dirname(__file__), '08-03-2023.csv')

        if not request.FILES.get('resume'):
            return JsonResponse({'error': 'No file attached'}, status=400)

        pdf_file = request.FILES['resume']

        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ''
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
            text = text.replace("\n", " ")

            with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                jobdata = list(reader)
                job_descriptions = [row[7] for row in jobdata]
                
                # Preprocess job descriptions
                processed_job_descriptions = []
                for desc in job_descriptions:
                    processed_desc = self.preprocess_text(desc)
                    processed_job_descriptions.append(processed_desc)
                
                # Tokenize the processed job descriptions
                tokenized_job_descriptions = [desc.split() for desc in processed_job_descriptions]
                
                # Create BM25 object
                bm25 = BM25Okapi(tokenized_job_descriptions)
                
                # Tokenize user resume and remove stopwords, punctuations, and specified characters
                processed_resume = self.preprocess_text(text)
                tokenized_resume = processed_resume.split()
                print(tokenized_resume)
                # Get BM25 scores
                bm25_scores = bm25.get_scores(tokenized_resume)
                print(bm25_scores)
                # Get indices of top 10 scores
                top10_indices = heapq.nlargest(10, range(len(bm25_scores)), key=bm25_scores.__getitem__)
                
                finaldata = []
                for i in top10_indices:
                    jobdata[i].append(bm25_scores[i])
                    finaldata.append(jobdata[i])
                
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
