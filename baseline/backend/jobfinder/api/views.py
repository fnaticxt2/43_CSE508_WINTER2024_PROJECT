from django.shortcuts import render
import PyPDF2

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
import pytesseract
from PIL import Image
import csv
from django.shortcuts import render
from django import forms
import spacy
import os
import heapq

nlp = spacy.load("en_core_web_md")

class UploadCSVForm(forms.Form):
    csv_file = forms.FileField()
    
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
            print(text)

            user_resume_doc = nlp(text)

            with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                jobdata = list(reader)
                job_descriptions = [row[7] for row in jobdata]
                job_description_docs = [nlp(job_desc) for job_desc in job_descriptions]
                similarity_scores = [user_resume_doc.similarity(job_desc) for job_desc in job_description_docs]
                print(similarity_scores)
                top3_indices = heapq.nlargest(10, range(len(similarity_scores)), key=similarity_scores.__getitem__)
                finaldata = []
                for i in top3_indices:
                    jobdata[i].append(similarity_scores[i])
                    finaldata.append(jobdata[i])
                
                return JsonResponse({'data': finaldata}, status=200)

            entities = [{'text': ent.text, 'label': ent.label_} for ent in doc.ents]
            return JsonResponse({'entities': entities})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            

def process_csv(csv_file):
    data = []
    reader = csv.reader(csv_file)
    next(reader, None)
    for row in reader:
        data.append(row)
    return data