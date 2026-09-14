name: Auto Update Jobs

on:
  schedule:
    - cron: '*/5 * * * *'
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - run: pip install requests beautifulsoup4 lxml
      - run: |
          cd naukrinow-pk-agent || true
          python scraper.py || python ../naukrinow-pk-agent/scraper.py
      - run: |
          if [ -f "naukrinow-pk-agent/jobs_db.json" ]; then cp naukrinow-pk-agent/jobs_db.json jobs_db.json; fi
          if [ -f "jobs_db.json" ]; then cp jobs_db.json naukrinow-pk-agent/jobs_db.json || true; fi
          python3 -c "import json; print(f"Total jobs: {len(json.load(open('jobs_db.json')))}")"
      - run: |
          git config --global user.name 'Bot'
          git config --global user.email 'bot@qadamrozgar.com'
          git add jobs_db.json naukrinow-pk-agent/jobs_db.json || git add jobs_db.json
          git diff --staged --quiet || (git commit -m "Update jobs - $(date)" && git push)
