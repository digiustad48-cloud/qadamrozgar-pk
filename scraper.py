import requests
from bs4 import BeautifulSoup
import time, random, json
from datetime import datetime

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NaukriNow.pk Agent"}

def scrape_mustakbil(city="karachi", pages=2):
    jobs = []
    for page in range(1, pages+1):
        url = f"https://www.mustakbil.com/jobs/{city}?page={page}"
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(r.text, "lxml")
            # Generic selectors - Mustakbil structure changes, so fallback
            cards = soup.select("div.job-item, div.job_listing, li.job")
            for c in cards[:20]:
                title = c.get_text(strip=True)[:120]
                link = c.find("a")
                jobs.append({
                    "source": "mustakbil.com",
                    "title": title,
                    "url": link["href"] if link and link.has_attr("href") else url,
                    "location": city.title(),
                    "scraped_at": datetime.now().isoformat()
                })
            time.sleep(random.uniform(2,4))
        except Exception as e:
            print(f"Mustakbil error {e}")
    return jobs

def scrape_rozee(query="developer", pages=1):
    jobs = []
    # Rozee blocks direct scraping, so we use JSearch fallback + Google trick
    # For demo, this returns structure - replace with your JSearch API key if you have
    url = f"https://www.rozee.pk/job/jsearch/q/{query}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "lxml")
        cards = soup.select("div.jobs-con, .job-box")
        for c in cards[:20]:
            jobs.append({
                "source": "rozee.pk",
                "title": c.get_text(strip=True)[:120],
                "url": url,
                "location": "Pakistan",
                "scraped_at": datetime.now().isoformat()
            })
    except Exception as e:
        print(f"Rozee error {e}")
    return jobs

def scrape_all():
    all_jobs = []
    all_jobs += scrape_mustakbil("karachi", 2)
    all_jobs += scrape_mustakbil("lahore", 2)
    all_jobs += scrape_mustakbil("islamabad", 2)
    all_jobs += scrape_rozee("government jobs", 1)
    # Deduplicate by title+url
    seen = set()
    clean = []
    for j in all_jobs:
        key = j["title"]+j["url"]
        if key not in seen:
            seen.add(key)
            clean.append(j)
    return clean

if __name__ == "__main__":
    print(json.dumps(scrape_all(), indent=2, ensure_ascii=False))
