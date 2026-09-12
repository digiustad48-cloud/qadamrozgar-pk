import re
from datetime import datetime

FAKE_KEYWORDS = ["earn 50k daily", "without investment", "whatsapp only", "simple typing work"]
def is_fake(job):
    desc = (job.get("title","") + " " + job.get("description","")).lower()
    return any(k in desc for k in FAKE_KEYWORDS)

def clean_and_translate(jobs):
    cleaned = []
    for job in jobs:
        if is_fake(job):
            job["verified"] = False
            job["fake_reason"] = "Vague / Spam pattern"
            continue
        job["verified"] = True
        # Auto add Urdu title (basic)
        job["title_ur"] = job["title"] # yahan aap Gemini Translation API laga sakte hain
        job["category"] = "Govt" if "government" in job["title"].lower() or "fpsc" in job["title"].lower() else "Private"
        job["posted_ago"] = "2 min pehle" if True else "abhi"
        cleaned.append(job)
    return cleaned
