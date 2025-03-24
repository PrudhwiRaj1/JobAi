from django.core.mail import send_mail
from django.utils.timezone import now

from .job_matching import match_jobs
from .models import JobApplication

def auto_apply_jobs(jobseeker, max_apply=4):
    today = now().date()
    
    # Get job seeker's preference (convert to lowercase for case-insensitive matching)
    job_preference = jobseeker.job_preference.lower() if jobseeker.job_preference else ""

    # Get applications already made today
    today_applied_jobs = JobApplication.objects.filter(jobseeker=jobseeker, applied_at__date=today)
    today_applied_jobs_count = today_applied_jobs.count()

    # **Enforce max 4 applications upfront**
    if today_applied_jobs_count >= max_apply:
        print(f"⚠️ Jobseeker {jobseeker.id} already applied for {today_applied_jobs_count} jobs today. No more applications allowed.")
        return 0, []

    # Get list of job IDs already applied for today (prevents duplicate applications for the same job)
    applied_job_ids = set(today_applied_jobs.values_list('company_joblist_id', flat=True))

    # Get matching jobs based on skills and eligibility
    matching_jobs = match_jobs(jobseeker)

    # Exclude jobs already applied for today and ensure job is still open
    available_jobs = [
        job for job in matching_jobs 
        if job.id not in applied_job_ids  # Prevent duplicate job applications
        and job.Lastdate >= today  # Ensure job is still open
    ]

    # **Sort jobs based on priority**
    def job_sort_key(job):
        is_preferred = job_preference in job.job_title.job_title.lower()
        return (
            not is_preferred,  # Prioritize job preference
            job.Lastdate,       # Prioritize nearest deadline
            job.dateofpublish or ""  # Prioritize recently published jobs
        )

    sorted_jobs = sorted(available_jobs, key=job_sort_key)

    applications_made = 0
    applied_jobs_list = []

    for job in sorted_jobs:
        # **Strictly enforce max-apply limit**
        if (today_applied_jobs_count + applications_made) >= max_apply:
            print(f"Max applications ({max_apply}) reached. Stopping further applications.")
            break  

        # **Final check before applying**
        if JobApplication.objects.filter(jobseeker=jobseeker, company_joblist=job).exists():
            print(f"Already applied to {job.job_title.job_title} at {job.company.name}. Skipping...")
            continue

        try:
            # Apply for the job
            JobApplication.objects.create(jobseeker=jobseeker, company_joblist=job)
            applications_made += 1  # Track successful applications
            applied_jobs_list.append(job)

            # Add this job to the exclusion list for future checks
            applied_job_ids.add(job.id)
            print(f"Applied to: {job.job_title.job_title} at {job.company.name}")

        except Exception as e:
            print(f"Error applying for {job.job_title.job_title}: {e}")
            continue

    # Send email notification if applications were made
    job_details_html = "".join([
    "<tr>"
    f"<td>🔹 <b>{job.job_title.job_title}</b></td>"
    f"<td>🏢 {job.company.name}</td>"
    f"<td>📍 {job.location}</td>"
    f"<td>🏷️ {job.job_type}</td>"
    f"<td>📅 {today}</td>"
    f"<td>⏳ {job.Lastdate}</td>"
   "</tr>"
    for job in applied_jobs_list
])

    email_body_html = f"""
<p>Dear {jobseeker.name},</p>
<p>You have successfully applied to the following jobs today via <b>JobAi</b>:</p>
<table border='1' cellspacing='0' cellpadding='5' style='border-collapse: collapse; text-align: left; width: 100%;'>
    <tr style='background-color: #f2f2f2;'>
        <th>Job Title</th>
        <th>Company</th>
        <th>Location</th>
        <th>Job Type</th>
        <th>Application Date</th>
        <th>Deadline</th>
    </tr>
    {job_details_html}
</table>
<p>🚀 <b>Next Steps:</b></p>
<ul>
    <li>📌 Check your application status in your <a href='http://127.0.0.1:8000/jobseeker_login/'>JobAi Profile</a>.</li>
    <li>📌 Prepare for interviews with our <b>AI Mock Interview Tool</b>.</li>
</ul>
<p>Thank you for using <b>JobAi</b>. We wish you success!</p>
<p>Best Regards,<br><b>JobAi Team</b><br>📧 support@jobai.com | 🌐 <a href='http://127.0.0.1:8000/jobseeker_login/'>www.jobai.com</a></p>
"""
    if applications_made!=0:
        send_mail(
    subject="Job Application Confirmation – Your Applications for Today",
    message="This is an HTML email. Please enable HTML to view the content properly.",
    from_email="jobai.prksolutions@gmail.com",
    recipient_list=[jobseeker.email],
    fail_silently=False,
    html_message=email_body_html
)
    return applications_made, applied_jobs_list