from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse
from docx import Document

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
            except Exception as e:
                content = f"Error reading document: {str(e)}"

    return render(request, "home.html", {"content": content})

# Create your views here.
def login(request):
    return render(request,'login.html')
def home(request):
    return render(request,'home.html')
def main(request):
    return render(request,'index.html')
def Register(request):
    return render(request,'register.html')
def Forgot_pwd(request):
    return render(request,'forgot-password.html')
def dashboard(request):
    return render(request, 'dashboard.html')
