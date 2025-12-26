# pulse_coding_assignment
 SaaS Review Scraper

Overview
This project is a Python-based command-line application that scrapes SaaS product reviews from G2 or Capterra for a given company and time range.  
It outputs all collected reviews in a clean, structured JSON file format.

This script was built as part of the Pulse Coding Assignment under a 24-hour implementation limit.

Features
- Command-line interface (CLI) with required arguments:
  - `--company` → Company name (e.g., "HubSpot")
  - `--start-date` and `--end-date` → Time range for review filtering
  - `--source` → `g2` or `capterra`
  - `--output` → Output JSON filename
- JSON output with structured review data:
  - title, review, date, reviewer, rating, source
- Date validation and error handling
- Pagination logic for multi-page scrapes (up to 3 pages)
- Clean modular architecture (`main.py`, `scraper_g2.py`, `scraper_capterra.py`)
- JSON saved locally in `/output` format

Installation
pip install -r requirements.txt

Usage
Example 1 – Scrape G2 reviews:
```
python main.py --company "HubSpot" --start-date 2024-01-01 --end-date 2025-12-31 --source g2 --output hubspot_g2_reviews.json
```
Example 2 – Scrape Capterra reviews:
```
python main.py --company "HubSpot" --start-date 2024-01-01 --end-date 2025-12-31 --source capterra --output hubspot_capterra_reviews.json
```
The script will display status logs and generate a JSON file in the same directory.
Output Format
Each JSON file contains:
```
{
  "company": "HubSpot",
  "source": "g2",
  "start_date": "2024-01-01",
  "end_date": "2025-12-31",
  "reviews": [
    {
      "title": "Excellent CRM platform",
      "review": "HubSpot has transformed our sales process.",
      "date": "2025-12-13",
      "reviewer": "John Doe",
      "rating": "5",
      "source": "g2"
    }
  ]
}
 Limitations
- G2 website uses JavaScript heavily, so static scraping (requests + BS4) may yield 0 reviews without using Playwright/Selenium.
- Limited slug generation (`company-name` format).
- Stops after 3 pages to avoid over-engineering.
- Output structure verified via actual HTML samples from G2.
Sample Output
Check [`sample_output.json`](./sample_output.json) for the demo JSON structure used to validate the output format.
Author:
Developed by: P K Naveen.,B.Tech(CSE-CYBER SECURITY)  
SRM IST- TRICHY CAMPUS
Contact: np3277@srmist.edu.in
