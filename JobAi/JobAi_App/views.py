from operator import contains
from django.shortcuts import render,redirect,get_object_or_404
import os
import re
import json
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from docx import Document
from django.conf import settings
from .models import *
from django.contrib import messages

def username(request):
    firstname = "Prudhwi Raj"
    dictionary1 = {'fname':firstname}
    return dictionary1

def extract_resume_details(content):
    """Extracts key details like name, skills, address, highest_qualification, job_preference, university name, date of birth, email, and phone number from the resume content."""
    details = {
        "name": "",
        "skills": "",
        "address": "",
        "highest_qualification": "",
        "job_preference": "",
        "university": "",
        "dob": "",
        "email": "",
        "phone": ""
    }
    
    email_pattern = r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+"
    phone_pattern = r"\+?\d{10,15}"
    dob_pattern = r"\b(\d{1,2}[-/ ](?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[-/ ]\d{2,4}|\d{1,2}[-/]\d{1,2}[-/]\d{2,4})\b"
    qualification_keywords = ["Bachelor's Degree", "MCA", "Master of Computer Application", "PhD", "B.Sc", "M.Sc", "B.Tech Computer Science", "M.Tech Computer Science", "MBA"]
    job_preferences_keywords = ["Software Engineer", "Data Scientist", "Backend Developer", "Frontend Developer", "Project Manager"]
    university_keywords = ["University", "Institute", "College"]
    skills_keywords = ["Python", "Java", "C++", "Django", "SQL", "Machine Learning", "Artificial Intelligence", "React", "JavaScript", "HTML", "CSS", "Git"]
    address_keywords = ["State", "Country", "District"]
    indian_states = ["Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"]
    
    resume_data = {}  # Dictionary to store extracted details
    
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
        
        if any(keyword.lower() in line.lower() for keyword in address_keywords) or any(state.lower() in line.lower() for state in indian_states):
            details["address"] = line
        
        for qualification in qualification_keywords:
            if qualification.lower() in line.lower():
                details["highest_qualification"] = qualification
                break
                
        for job in job_preferences_keywords:
            if job.lower() in line.lower():
                details["job_preference"] = job
                break
                
        for university in university_keywords:
            if university.lower() in line.lower():
                details["university"] = line
                break
                
        for skill in skills_keywords:
            if skill.lower() in line.lower():
                details["skills"] += skill + ", "
    
    details["skills"] = details["skills"].rstrip(", ")
    resume_data.update(details)  # Storing extracted details in the list
    
    return details


# def read_word_document(request):
#     content = ""
#     alert_message=""
#     extracted_details = None
#     if request.method == "POST":
#         uploaded_file = request.FILES.get("word_file")
#         resume=request.POST.get("word_file")
#         jobseeker_resumeobj=jobseeker_resume()
#         jobseeker_resumeobj.resume=resume
#         jobseeker_resumeobj.save()
#         if uploaded_file:
#             # Validate file extension
#             if not uploaded_file.name.lower().endswith(('.doc', '.docx')) and not uploaded_file.name.lower().contains("Resume","CV"):
#                 return JsonResponse({"error": "Only Resumes with .doc and .docx files are allowed."}, status=400)
#                 return redirect("jobseeker_home")
#             try:
#                 # Ensure media directories exist
#                 documents_dir = os.path.join(settings.MEDIA_ROOT, "documents")
#                 json_dir = os.path.join(settings.MEDIA_ROOT, "json")
#                 os.makedirs(documents_dir, exist_ok=True)
#                 os.makedirs(json_dir, exist_ok=True)
                
#                 # Save the uploaded file
#                 fs = FileSystemStorage(location=documents_dir)
#                 file_path = fs.save(uploaded_file.name, uploaded_file)
#                 file_path = fs.path(file_path)
                
#                 # Read the Word document content
#                 document = Document(file_path)
#                 paragraphs = [p.text for p in document.paragraphs if p.text.strip()]
#                 content = "\n".join(paragraphs)
               
#                 # Extract resume details
#                 extracted_details = extract_resume_details(content)
#                 # resume_details = ResumeDetails.objects.create(**extracted_details)

#                 # Check if essential details are missing
#                 if not extracted_details.get("name") or not extracted_details.get("email") or not extracted_details.get("phone"):
#                     alert_message = "*Failed to extract your resume.Check your file and try again."
#                     jobseeker_resumeobj.delete()
#                 else:
#                     # Convert document to JSON and save
#                     json_data = convert_docx_to_json(file_path, uploaded_file.name)
#                     messages.success(request, "Resume uploaded successfully!")                    
#             except Exception as e: 
#                 messages.error(request, f"Error reading document: {str(e)}")
#     return render(request, "jobseeker_home.html",{"resume_details": extracted_details,"alert_message": alert_message})
    
    

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


def jobseeker_login(request):
    if request.method=="POST":
        Email=request.POST.get("email")
        Password=request.POST.get("password")
        try:
            jobseeker = Jobseeker_Registration.objects.get(email=Email, password=Password)
            messages.success(request, "Login Successfully")
            return redirect('home')  # Redirect to a dashboard or home page after login
        except Jobseeker_Registration.DoesNotExist:
            messages.error(request, "Invalid Email or Password")
    return render(request, 'jobseeker_login.html')


def jobseeker_home(request):
    content = ""
    alert_message=""
    extracted_details = None
    if request.method == "POST":
        uploaded_file = request.FILES.get("word_file")
        resume=request.POST.get("word_file")
        jobseeker_resumeobj=jobseeker_resume()
        jobseeker_resumeobj.resume=resume
        jobseeker_resumeobj.save()
        if uploaded_file:
            # Validate file extension
            if not uploaded_file.name.lower().endswith(('.doc', '.docx')) and not uploaded_file.name.lower().contains("Resume","CV"):
                return JsonResponse({"error": "Only Resumes with .doc and .docx files are allowed."}, status=400)
                return redirect("jobseeker_home")
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
                # resume_details = ResumeDetails.objects.create(**extracted_details)

                # Check if essential details are missing
                if not extracted_details.get("name") or not extracted_details.get("email") or not extracted_details.get("phone"):
                    alert_message = "*Failed to extract your resume.Check your file and try again."
                    jobseeker_resumeobj.delete()
                else:
                    # Convert document to JSON and save
                    json_data = convert_docx_to_json(file_path, uploaded_file.name)
                    messages.success(request, "Resume uploaded successfully!")                    
            except Exception as e: 
                messages.error(request, f"Error reading document: {str(e)}")
    context={
        "resume_details": extracted_details,
        "alert_message": alert_message,
        "fname":'Prudhwi Raj'
    }   
    return render(request, "jobseeker_home.html",context)

def main(request):
    return render(request, 'index.html')

def base(request):
    return render(request,'base.html')

def Register(request):
    name=""
    email=""
    password=""
    if request.method == "POST":   
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        if Jobseeker_Registration.objects.filter(name=name).exists() and Jobseeker_Registration.objects.filter(email=email).exists():
            messages.error(request, "A Jobseeker with this name and/or email already exists. Please use different details.")
        else:
            jobseeker_obj=Jobseeker_Registration()
            jobseeker_obj.name=name
            jobseeker_obj.email=email
            jobseeker_obj.password=password
            jobseeker_obj.save()
            messages.success(request, "Jobseeker registered successfully!.Email will be your Username")
            return render(request,'jobseeker_register.html')
    return render(request, 'jobseeker_register.html')


def Forgot_pwd(request):
    return render(request, 'forgot-password.html')


def user_base(request):
    return render(request, 'base.html')


def search_job(request):
    return render(request, 'search-job.html', username(request))


def coverletter(request):
    return render(request, 'cover-letter.html', username(request))


def settings_view(request):
    return render(request, 'settings_view.html', username(request))


def support(request):
    return render(request, 'support.html', username(request))


def mockinterview(request):
    return render(request, 'mock-interview.html', username(request))


def autoapply(request):
    return render(request, 'auto-apply.html', username(request))

def user_type(request):
    return render(request,'user-type.html')

def company_login(request):
    if request.method=="POST":
        Email=request.POST.get("email")
        Password=request.POST.get("password")
        try: 
            company=Company.objects.get(email=Email,password=Password) 
            messages.success(request, "Login Successfully")
            return redirect('company_dashboard')  # Redirect to a dashboard or home page after login
        except Company.DoesNotExist:
            messages.error(request, "Invalid Email or Password")
    return render(request, 'company_login.html')

def company_registration(request):
    if request.method == "POST":
        name=request.POST.get('company_name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        company_type = request.POST.get("CompanyType")  # This returns a string
        company_address=request.POST.get('Address')
        # Check if a company with the same name or email already exists
        if Company.objects.filter(name=name).exists() and Company.objects.filter(email=email).exists():
            messages.error(request, "A company with this name or email already exists. Please use different details.")
        else:
            # Create and save the company
            companyobj=Company()
            companyobj.name=name
            companyobj.password=password
            companyobj.email=email
            companyobj.company_type_id=company_type
            companyobj.address=company_address
            companyobj.save()
            messages.success(request, "Company registered successfully!.Email will be your Username")
            return redirect('company_registration')
    company=Company_Type_Master.objects.all()
    context={
        'company':company
    }
    return render(request,'company_registration.html',context)

def company_type(request):
    if request.method == "POST":
        company_type=request.POST.get('ctype')
        company_typeobj=Company_Type_Master()
        company_typeobj.company_type=company_type
        company_typeobj.save()
        messages.success(request, "Company type registered successfully!")
        return render(request,'company_type.html')
    return render(request,'company_type.html')
    
def company_forgot_password(request):
    return render(request,'company_forgot_pwd.html')

def company_dashboard(request):
    return render(request,'company_dashboard.html')
def company_settings(request):
    return render(request,'company_settings_view.html')
def company_jobs(request):
    return render(request,'company_jobs.html')
def company_postjob(request):
    return render(request,'company_postjob.html')