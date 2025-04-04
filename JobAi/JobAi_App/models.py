from django.db import models
# from fields import ComparableMixin

class Jobseeker_Registration(models.Model):
    name=models.CharField(max_length=255,default="Unknown")
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=255)
    phone=models.CharField(max_length=20, blank=True, null=True)
    last_login = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.name

class jobseeker_profile(models.Model):    
    user = models.OneToOneField(Jobseeker_Registration, on_delete=models.CASCADE, related_name='profile',null=True)  # ForeignKey to Jobseeker_Registration
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_img=models.ImageField(upload_to='images/',blank=True,null=True)
    dob = models.DateField(max_length=20,blank=True,null=True) 
    highest_qualification = models.CharField(max_length=255, blank=True, null=True)
    percentage=models.TextField(blank=True,null=True)
    passoutyear=models.TextField(blank=True,null=True)
    job_preference = models.CharField(max_length=255, blank=True, null=True)
    university = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='documents/', blank=True, null=True)

    def __str__(self):
        return self.name if self.name else "Unnamed Jobseeker"

class jobseeker_resume(models.Model): 
    user = models.ForeignKey(Jobseeker_Registration, on_delete=models.CASCADE, null=True, blank=True)  # user is required, cannot be null
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Document uploaded by {self.user.username} on {self.uploaded_at}"
class Company_Type_Master(models.Model):
    company_type=models.CharField(max_length=50)
    def __str__(self):
        return self.name if self.name else "Unnamed Company"
    
class Company(models.Model):
    password=models.CharField(max_length=255)
    # Links to Django's built-in User model
    name = models.CharField(max_length=255)
    description=models.CharField(max_length=12000,null=True)
    email = models.EmailField(unique=True)
    company_type = models.ForeignKey(Company_Type_Master,on_delete=models.CASCADE,default=None)
    address = models.CharField(max_length=255)
    profile_img=models.ImageField(upload_to='company_images/',blank=True,null=True)

    def __str__(self):
        return self.name
class job_title(models.Model):
    job_title=models.CharField(max_length=250,blank=True,null=True)
    def __str__(self):
        return self.name 
    
class company_joblist(models.Model):
    company=models.ForeignKey(Company,on_delete=models.CASCADE,default=None)
    job_title = models.ForeignKey(job_title,on_delete=models.CASCADE,default=None)
    # job_number = models.CharField(max_length=100)
    job_description = models.CharField(max_length=12000, blank=True, null=True)
    job_type = models.CharField(max_length=255, blank=True, null=True)
    location=models.CharField(max_length=200,null=True)
    highest_qualification = models.CharField(max_length=255, blank=True, null=True)
    percent_criteria=models.TextField(blank=True,null=True)
    skills_required = models.TextField(blank=True, null=True)
    dateofpublish=models.DateField(max_length=20,null=True)
    Lastdate=models.DateField(max_length=20,null=True) 
    

class JobNotification(models.Model):
    jobseeker_profile = models.ForeignKey(jobseeker_profile, on_delete=models.CASCADE, related_name='notifications')
    company_job = models.ForeignKey(company_joblist, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.jobseeker.name} - {self.company_job.job_title}"


class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
### **New Job Application Table**
class JobApplication(models.Model):
    jobseeker = models.ForeignKey(jobseeker_profile, on_delete=models.CASCADE, related_name='applications')
    company_joblist = models.ForeignKey(company_joblist, on_delete=models.CASCADE, related_name='applications')
    applied_at = models.DateTimeField(auto_now_add=True)  # Tracks when applied
    ats_score = models.IntegerField(null=True, blank=True)  # Store ATS score
    status=models.TextField(blank=False,null=False,default="Applied")
    class Meta:
        unique_together = ('jobseeker', 'company_joblist')  # Ensures unique applications per jobseeker-job

    def __str__(self):
        return f"{self.jobseeker.name} applied for {self.job.job_title} at {self.job.company.name}"
