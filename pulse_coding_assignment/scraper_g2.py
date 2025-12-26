import requests
from bs4 import BeautifulSoup
from datetime import datetime
class G2Scraper:
    BASE_SEARCH_URL = "https://www.g2.com/products/{slug}/reviews"
    def __init__(self, company_name: str):
        self.company_name = company_name
        self.slug = company_name.lower().replace(" ", "-")
    def _build_url(self, page: int = 1):
        return f"{self.BASE_SEARCH_URL.format(slug=self.slug)}?page={page}"
    def _parse_date(self, date_str: str):
        try:
            return datetime.strptime(date_str.strip(), "%B %d, %Y").date()
        except Exception:
            return None
    def fetch_reviews(self, start_date, end_date):
        reviews = []
        page = 1
        while True:
            url = self._build_url(page=page)
            resp = requests.get(url, timeout=15)
            if resp.status_code != 200:
                break
            soup = BeautifulSoup(resp.text, "html.parser")
            review_cards = soup.select("article")  # adjust to real CSS class later
            if not review_cards:
                break
            for card in review_cards:
                title_el = card.select_one("h3")
                title = title_el.get_text(strip=True) if title_el else ""
                body_el = card.select_one("p")
                body = body_el.get_text(strip=True) if body_el else ""
                date_el = card.select_one("time")
                date_text = date_el.get_text(strip=True) if date_el else ""
                review_date = self._parse_date(date_text)
                if not review_date:
                    continue
                if review_date < start_date or review_date > end_date:
                    continue
                rating_el = card.select_one("[data-test='star-rating']")
                rating = rating_el.get("data-rating") if rating_el else None
                reviewer_el = card.select_one(".user-name")
                reviewer = reviewer_el.get_text(strip=True) if reviewer_el else ""
                reviews.append(
                    {
                        "title": title,
                        "review": body,
                        "date": review_date.isoformat(),
                        "reviewer": reviewer,
                        "rating": rating,
                        "source": "g2",
                    }
                )
            page += 1
            if page > 3:  
                break
        return reviews
