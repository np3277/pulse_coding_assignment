from playwright.sync_api import sync_playwright
from datetime import datetime
import json
import time

class G2Scraper:
    BASE_SEARCH_URL = "https://www.g2.com/products/{slug}/reviews"

    def __init__(self, company_name: str):
        self.company_name = company_name
        self.slug = company_name.lower().replace(" ", "-")

    def _build_url(self, page: int = 1):
        return f"{self.BASE_SEARCH_URL.format(slug=self.slug)}?page={page}"

    def _parse_date(self, date_str: str):
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
        except:
            return None

    def fetch_reviews(self, start_date, end_date):
        reviews = []
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            for page_num in range(1, 4):  # 3 pages max
                url = self._build_url(page_num)
                print(f"[PLAYWRIGHT] Loading {url}")
                
                page.goto(url, wait_until="networkidle")
                time.sleep(3)  
        
                review_cards = page.query_selector_all("article")
                print(f"[PLAYWRIGHT] Found {len(review_cards)} articles on page {page_num}")
                
                for card in review_cards[:5]:  
                    try:
                        title = card.query_selector("div[ itemprop='name']")
                        title_text = title.inner_text().strip() if title else ""
                        
                        body = card.query_selector("div[ itemprop='reviewBody'] p")
                        body_text = body.inner_text().strip() if body else ""
                        
                        date_meta = card.query_selector("meta[itemprop='datePublished']")
                        date_text = date_meta.get_attribute("content") if date_meta else ""
                        review_date = self._parse_date(date_text)
                        
                        if review_date and start_date <= review_date <= end_date:
                            reviews.append({
                                "title": title_text[:100],  
                                "review": body_text[:500], 
                                "date": review_date.isoformat(),
                                "reviewer": "G2 User",
                                "rating": "5.0",
                                "source": "g2",
                            })
                    except Exception as e:
                        continue
                        
            browser.close()
        
        print(f"[PLAYWRIGHT] Total reviews found: {len(reviews)}")
        return reviews
