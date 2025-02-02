from django.shortcuts import render
import os
import re
import json
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from docx import Document
from django.conf import settings


def extract_resume_details(content):
    """Extracts key details like name, skills, address, date of birth, email, and phone number from the resume content."""
    details = {
        "name": "",
        "skills": "",
        "address": "",
        "dob": "",
        "email": "",
        "phone": ""
    }
    
    email_pattern = r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+"
    phone_pattern = r"\+?\d{10,15}"
    dob_pattern = r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"
    skills_keywords = ["Python", "Java", "C++", "Django", "SQL", "Machine Learning", "AI", "React", "JavaScript"]
    
    lines = content.split("\n")
    for line in lines:
        line = line.strip()
        if not details["name"] and re.match(r"^[A-Z][a-z]+\s[A-Z][a-z]+", line):
            details["name"] = line
        if not details["email"] and re.search(email_pattern, line):
            details["email"] = re.search(email_pattern, line).group()
        if not details["phone"] and re.search(phone_pattern, line):
            details["phone"] = re.search(phone_pattern, line).group()
        if not details["dob"] and re.search(dob_pattern, line):
            details["dob"] = re.search(dob_pattern, line).group()
        if "address" in line.lower():
            details["address"] = line
        for skill in skills_keywords:
            if skill.lower() in line.lower():
                details["skills"] += skill + ", "
    
    details["skills"] = details["skills"].rstrip(", ")
    return details

def read_word_document(request):
    content = ""
    if request.method == "POST":
        uploaded_file = request.FILES.get("word_file")
        if uploaded_file:
            # Validate file extension
            if not uploaded_file.name.lower().endswith(('.doc', '.docx')):
                return JsonResponse({"error": "Only .doc and .docx files are allowed."}, status=400)
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
               
                # Extract resume details
                extracted_details = extract_resume_details(content)
                
                # Convert document to JSON and save
                json_data = convert_docx_to_json(file_path, uploaded_file.name)
                return JsonResponse({"document_data":json.loads(json_data), "resume_details": extracted_details})
            except Exception as e:
                return JsonResponse({"error": f"Error reading document: {str(e)}"}, status=500)
    return render(request, "home.html", {"content": content,"resume_details": extracted_details})

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
def username(request):
    firstname="Prudhwi"
    dictionary1={'fname':firstname}
    return dictionary1
def home(request):
    return render(request,'home.html',username(request))
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
    return render(request,'search-job.html',username(request))
