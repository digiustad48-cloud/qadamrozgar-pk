from apscheduler.schedulers.blocking import BlockingScheduler
from scraper import scrape_all
from cleaner_agent import clean_and_translate
import json, os
from datetime import datetime

DB_FILE = "jobs_db.json"

def run_agent_cycle():
    print(f"[{datetime.now()}] Agent cycle start...")
    raw = scrape_all()
    print(f"Raw jobs found: {len(raw)}")
    cleaned = clean_and_translate(raw)
    print(f"Verified jobs: {len(cleaned)}")
    # Save to DB
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)
    print(f"Updated {DB_FILE}")
    # Yahan aap WhatsApp API (Twilio / WhatsApp Cloud) call laga sakte hain

import sys
if __name__ == "__main__":
    run_agent_cycle()
    if "--once" in sys.argv:
        print("Once mode - GitHub ke liye done")
        exit()
    # Scheduler har 30 min baad
    sched = BlockingScheduler()
    sched.add_job(run_agent_cycle, 'interval', minutes=30)
    print("Agent scheduler active - har 30 min me update hoga. Ctrl+C to stop.")
    sched.start()
