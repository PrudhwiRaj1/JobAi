from django.shortcuts import render
import json
from django.db import models
from django.shortcuts import render
from django.http import HttpResponse
from docx import Document
from django.http.response import JsonResponse

def read_word_document(request):
    content = ""
    if request.method == "POST":
        uploaded_file = request.FILES.get("word_file")
        if uploaded_file:
            try:
                # Read the Word document content
                document = Document(uploaded_file)
                paragraphs = [p.text for p in document.paragraphs if p.text.strip()]
                content = "\n".join(paragraphs)
                json_data = convert_docx_to_json(uploaded_file)
                return JsonResponse(json.loads(json_data)) 
            except Exception as e:
                content = f"Error reading document: {str(e)}"
    # return render(request, "home.html", {"form": form})

    return render(request, "home.html", {"content": content})
def convert_docx_to_json(docx_path):
    """Convert a .docx file to JSON format"""
    document = Document(docx_path)
    data = {"paragraphs": []}

    for para in document.paragraphs:
        data["paragraphs"].append(para.text)

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
    return render(request,'search-job.html')
