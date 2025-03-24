from .models import company_joblist

def parse_list(text):
    """
    Parse a comma-separated string into a set of lowercase trimmed items.
    """
    if text:
        return set([item.strip().lower() for item in text.split(",") if item.strip()])
    return set()

def match_jobs(jobseeker):
    # Function to extract numeric percentage value from string
    def extract_percentage(value):
        try:
            return float(value.strip('%')) if value else 0.0
        except ValueError:
            return 0.0
    # Parse jobseeker skills and qualification
    seeker_skills = parse_list(jobseeker.skills)
    seeker_qual = jobseeker.highest_qualification.strip().lower() if jobseeker.highest_qualification else ""
    seeker_percentage = extract_percentage(jobseeker.percentage) if jobseeker.percentage else 0.0
    # Fetch all jobs (this could be optimized with a filter, but for now we'll do it in Python)
    all_jobs = company_joblist.objects.all()
    matching_jobs = []
    for job in all_jobs:
        job_skills = parse_list(job.skills_required)
        job_percentage_criteria = extract_percentage(job.percent_criteria)
        
        # Check for any common skills
        if not seeker_skills.intersection(job_skills):
            continue
        
        # Check eligibility: if job.highest_qualification exists, see if it matches the seeker qualification
        if job.highest_qualification:
            # Split eligibility criteria if multiple (assuming comma-separated)
            eligibility_set = parse_list(job.highest_qualification)
            if seeker_qual and seeker_qual not in eligibility_set:
                continue
            # Check if jobseeker's percentage meets or exceeds the job's percentage criteria
        if seeker_percentage < job_percentage_criteria:
            continue
        matching_jobs.append(job)
    return matching_jobs