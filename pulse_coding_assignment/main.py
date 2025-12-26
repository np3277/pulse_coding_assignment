import argparse
import json
from datetime import datetime

from scraper_g2 import G2Scraper
from scraper_capterra import CapterraScraper


def parse_args():
    parser = argparse.ArgumentParser(description="Scrape SaaS reviews from G2 or Capterra.")
    parser.add_argument("--company", required=True, help="Company name as on G2/Capterra")
    parser.add_argument("--start-date", required=True, help="Start date in YYYY-MM-DD")
    parser.add_argument("--end-date", required=True, help="End date in YYYY-MM-DD")
    parser.add_argument("--source", required=True, choices=["g2", "capterra"],
                        help="Review source: g2 or capterra")
    parser.add_argument("--output", default="reviews_output.json", help="Output JSON filename")
    return parser.parse_args()


def validate_dates(start_str, end_str):
    try:
        start = datetime.strptime(start_str, "%Y-%m-%d").date()
        end = datetime.strptime(end_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Dates must be in YYYY-MM-DD format")

    if start > end:
        raise ValueError("start-date cannot be after end-date")

    return start, end


def main():
    args = parse_args()

    try:
        start_date, end_date = validate_dates(args.start_date, args.end_date)
    except ValueError as e:
        print(f"[ERROR] {e}")
        return

    if args.source == "g2":
        scraper = G2Scraper(company_name=args.company)
    else:
        scraper = CapterraScraper(company_name=args.company)

    try:
        reviews = scraper.fetch_reviews(start_date=start_date, end_date=end_date)
    except Exception as e:
        print(f"[ERROR] Failed to fetch reviews: {e}")
        return

    data = {
        "company": args.company,
        "source": args.source,
        "start_date": args.start_date,
        "end_date": args.end_date,
        "reviews": reviews,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[OK] Saved {len(reviews)} reviews to {args.output}")


if __name__ == "__main__":
    main()
