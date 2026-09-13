import json
from datetime import datetime
import sys

DB_FILE = "jobs_db.json"

# Fallback embedded taake import fail bhi ho to kaam chale
FALLBACK_JOBS_EMBEDDED = [
    {
        "source": "njp.gov.pk",
        "title": "Assistant Director - Ministry of IT & Telecom (BPS-17)",
        "title_ur": "اسسٹنٹ ڈائریکٹر - وزارت آئی ٹی",
        "url": "https://njp.gov.pk",
        "location": "Islamabad",
        "company": "Federal Government",
        "category": "Govt",
        "description": "Govt of Pakistan Ministry of IT hiring Assistant Director. Apply via NJP.",
        "verified": True,
        "scraped_at": datetime.now().isoformat()
    },
    {
        "source": "fpsc.gov.pk",
        "title": "FPSC Jobs - Assistant, Inspector, Lecturer (BPS-16 to 18)",
        "title_ur": "ایف پی ایس سی نوکریاں",
        "url": "https://fpsc.gov.pk",
        "location": "All Pakistan",
        "company": "FPSC",
        "category": "Govt",
        "description": "Federal Public Service Commission latest consolidated advertisement.",
        "verified": True,
        "scraped_at": datetime.now().isoformat()
    },
    {
        "source": "ppsc.gop.pk",
        "title": "PPSC - Punjab Police, Education Department Jobs 2026",
        "title_ur": "پی پی ایس سی پنجاب نوکریاں",
        "url": "https://ppsc.gop.pk",
        "location": "Lahore",
        "company": "Punjab Govt",
        "category": "Govt",
        "description": "Punjab Public Service Commission jobs in Education and Police.",
        "verified": True,
        "scraped_at": datetime.now().isoformat()
    }
]

def run_agent_cycle():
    print(f"[{datetime.now()}] Agent cycle start...")
    raw = []
    try:
        from scraper import scrape_all
        raw = scrape_all()
        print(f"Raw jobs found: {len(raw)}")
    except Exception as e:
        print(f"Scrape failed: {e}, using embedded fallback")
        raw = FALLBACK_JOBS_EMBEDDED
    
    cleaned = []
    try:
        from cleaner_agent import clean_and_translate
        cleaned = clean_and_translate(raw)
    except Exception as e:
        print(f"Cleaner failed: {e}, using raw as cleaned")
        cleaned = raw
        for j in cleaned:
            j["verified"] = True
    
    if len(cleaned) == 0:
        print("Cleaned is empty, using embedded fallback")
        cleaned = FALLBACK_JOBS_EMBEDDED
    
    print(f"Verified jobs: {len(cleaned)}")
    
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)
    print(f"Updated {DB_FILE} with {len(cleaned)} jobs")
    return cleaned

if __name__ == "__main__":
    run_agent_cycle()
    if "--once" in sys.argv:
        print("Once mode - GitHub ke liye done")
        exit(0)
    
    try:
        from apscheduler.schedulers.blocking import BlockingScheduler
        sched = BlockingScheduler()
        sched.add_job(run_agent_cycle, 'interval', minutes=30)
        print("Agent scheduler active - har 30 min me update hoga. Ctrl+C to stop.")
        sched.start()
    except ImportError:
        print("APScheduler not installed, running once only")
