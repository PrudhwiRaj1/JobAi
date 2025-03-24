import re
def extract_resume_details(content):
    """Extracts key details like name, skills, address, highest_qualification, job_preference, university name, date of birth, email, and phone number from the resume content."""
    details = {
        "name": "",
        "skills": "",
        "address": "",
        "highest_qualification": "",
        "passout_year": "",
        "percentage": "",
        "job_preference": "",
        "university": "",
        "dob": "",
        "email": "",
        "phone": ""
    }

    # Define patterns and keywords
    email_pattern = r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+"
    phone_pattern = r"\+?\d{10,15}"
    # passout_year_pattern = r"\b(19\d{2}|20\d{2})\b"
    percentage_pattern = r"(\d{1,2}\.\d{1,2}|\d{1,2})%"
    dob_patterns = [
        r"\b(\d{1,2})[-/ ](\d{1,2})[-/ ](\d{2,4})\b",  # Formats like DD/MM/YYYY, DD-MM-YYYY
        r"\b(\d{1,2})[-/ ](Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[-/ ](\d{2,4})\b"  # Formats with month names
    ]
    qualification_keywords = ["Bachelor's Degree","Integrated MCA","MCA", "Master of Computer Application", "PhD", "B.Sc", "M.Sc", "B.Tech Computer Science", "M.Tech Computer Science", "MBA"]
    job_preferences_keywords = ["Software Engineer", "Data Scientist", "Backend Developer", "Frontend Developer", "Project Manager"]
    university_keywords = ["University", "Institute", "College"]
    skills_keywords = ["Python", "Java", "C++", "Django", "SQL", "Machine Learning", "Artificial Intelligence", "React", "JavaScript", "HTML", "CSS", "Git", "Data Analytics"]
    address_keywords = ["State", "Country", "District"]
    indian_states = ["Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"]

    # Use a set for skills to prevent duplicates
    skills_found = set()

    # Process content line-by-line
    lines = content.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Extract name: assume first occurrence of two or more capitalized words is the candidate's name
        if not details["name"]:
            name_match = re.match(r"^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)", line)
            if name_match:
                details["name"] = name_match.group(1)

        # Extract email
        if not details["email"]:
            email_match = re.search(email_pattern, line)
            if email_match:
                details["email"] = email_match.group()

        # Extract phone
        if not details["phone"]:
            phone_match = re.search(phone_pattern, line)
            if phone_match:
                details["phone"] = phone_match.group()

        # # Extract date of birth
        # if not details["dob"]:
        #     dob_match = re.search(dob_patterns, line, flags=re.IGNORECASE)
        #     if dob_match:
        #         details["dob"] = dob_match.group(1)
        # Extract date of birth and format to YYYY-MM-DD (for HTML date input)
        if not details["dob"]:
            for pattern in dob_patterns:
                dob_match = re.search(pattern, line, flags=re.IGNORECASE)
                if dob_match:
                    try:
                        if len(dob_match.groups()) == 3:
                            day, month, year = dob_match.groups()
                            if month.isdigit():
                                formatted_date = f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
                            else:
                                month_num = {
                                    "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
                                    "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
                                }.get(month[:3].capitalize(), "")
                                if month_num:
                                    formatted_date = f"{int(year):04d}-{month_num}-{int(day):02d}"
                                else:
                                    continue
                            details["dob"] = formatted_date
                            break
                    except ValueError:
                        continue

        # Extract address if line contains address-related keywords or Indian states
        if not details["address"]:
            if any(kw.lower() in line.lower() for kw in address_keywords) or any(state.lower() in line.lower() for state in indian_states):
                details["address"] = line

        # Extract highest qualification
        if not details["highest_qualification"]:
            for qualification in qualification_keywords:
                if qualification.lower() in line.lower():
                    details["highest_qualification"] = qualification
                    break

        # Extract percentage
        if not details["percentage"]:
            percentage_match = re.search(percentage_pattern, line)
            if percentage_match:
                details["percentage"] = percentage_match.group()

        # Extract job preference
        if not details["job_preference"]:
            for job in job_preferences_keywords:
                if job.lower() in line.lower():
                    details["job_preference"] = job
                    break

        # Extract university: store the entire line if it contains any keyword
        if not details["university"]:
            for uni_kw in university_keywords:
                if uni_kw.lower() in line.lower():
                    details["university"] = line
                    break

        # Accumulate skills from the line
        for skill in skills_keywords:
            if skill.lower() in line.lower():
                skills_found.add(skill)

    details["skills"] = ", ".join(sorted(skills_found))
    return details