from django.shortcuts import render
import os
import json
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from docx import Document
from django.conf import settings

def read_word_document(request):
    content = ""
    if request.method == "POST":
        uploaded_file = request.FILES.get("word_file")
        if uploaded_file:
            try:
                # Ensure media directories exist
                documents_dir = os.path.join(settings.MEDIA_ROOT, "documents")
                json_dir = os.path.join(settings.MEDIA_ROOT, "json")
                os.makedirs(documents_dir, exist_ok=True)
                os.makedirs(json_dir, exist_ok=True)
                
                # Save the uploaded file
                fs = FileSystemStorage(location=documents_dir)
                file_path = fs.save(uploaded_file.name, uploaded_file)
                file_path = fs.path(file_path)
                
                # Read the Word document content
                document = Document(file_path)
                paragraphs = [p.text for p in document.paragraphs if p.text.strip()]
                content = "\n".join(paragraphs)
                
                # Convert document to JSON and save
                json_data = convert_docx_to_json(file_path, uploaded_file.name)
                return JsonResponse(json.loads(json_data))
            except Exception as e:
                content = f"Error reading document: {str(e)}"
    
    return render(request, "home.html", {"content": content})

def convert_docx_to_json(docx_path, filename):
    """Convert a .docx file to JSON format and save it to media folder"""
    document = Document(docx_path)
    data = {"paragraphs": []}

    for para in document.paragraphs:
        data["paragraphs"].append(para.text)
    
    json_path = os.path.join(settings.MEDIA_ROOT, "json", filename + ".json")
    
    try:
        with open(json_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
    except Exception as e:
        print(f"Error saving JSON file: {e}")
    
    return json.dumps(data, indent=4)
# Create your views here.
def login(request):
    return render(request,'login.html')
def home(request):
    firstname="User"
    dictionary1={'fname':firstname}
    return render(request,'home.html',dictionary1)
def main(request):
    return render(request,'index.html')
def Register(request):
    return render(request,'register.html')
def Forgot_pwd(request):
    return render(request,'forgot-password.html')
def dashboard(request):
    return render(request, 'dashboard.html')
def base(request):
    return render(request,'base.html')
def search_job(request):
    firstname="User"
    dictionary1={'fname':firstname}
    return render(request,'search-job.html',dictionary1)
