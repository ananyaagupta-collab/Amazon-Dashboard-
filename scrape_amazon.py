#!/usr/bin/env python3
"""
Daily Amazon ratings scraper.
Run automatically by GitHub Actions every day at 9am IST.
Updates trends_data.json and competitors_data.json, then GitHub pushes
to the repo so Streamlit Cloud redeploys with fresh data.
"""
import json, os, re, time, random, datetime
import requests
from bs4 import BeautifulSoup

BASE = os.path.dirname(os.path.abspath(__file__))
TODAY = datetime.date.today().isoformat()

NATIVE_PRODUCTS = [
    {"id": "m0",        "label": "M0",        "url": "https://www.amazon.in/dp/B0FB3L3FSH"},
    {"id": "m1",        "label": "M1",         "url": "https://www.amazon.in/dp/B0D79G62J3"},
    {"id": "m1pro",     "label": "M1 Pro",     "url": "https://www.amazon.in/dp/B0GWQFXMTY"},
    {"id": "m2pro",     "label": "M2 Pro",     "url": "https://www.amazon.in/dp/B0G4CHKBGP"},
    {"id": "lockpro",   "label": "Lock Pro",   "url": "https://www.amazon.in/dp/B0DJH6Q2XQ"},
    {"id": "lockultra", "label": "Lock Ultra", "url": "https://www.amazon.in/dp/B0H2MVF2L2"},
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-IN,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

def scrape(url):
    """Return (rating, review_count) from an Amazon product page."""
    try:
        time.sleep(random.uniform(3, 7))
        r = requests.get(url, headers=HEADERS, timeout=25)
        soup = BeautifulSoup(r.text, "html.parser")

        # ── Rating ────────────────────────────────────────────────────────
        rating = None
        el = soup.select_one("#acrPopover")
        if el and el.get("title"):
            m = re.search(r"([\d.]+)\s+out of", el["title"])
            if m:
                rating = float(m.group(1))
        if not rating:
            el = soup.select_one("span.a-icon-alt")
            if el:
                m = re.search(r"([\d.]+)", el.text)
                if m:
                    rating = float(m.group(1))

        # ── Review / rating count ─────────────────────────────────────────
        count = None
        el = soup.select_one("#acrCustomerReviewText")
        if el:
            m = re.search(r"([\d,]+)", el.text)
            if m:
                count = int(m.group(1).replace(",", ""))

        # ── Star histogram (not always available without JS) ──────────────
        stars = {}
        hist = soup.select("table#histogramTable tr") or soup.select("[data-hook='rating-out-of-text']")
        for s in range(1, 6):
            pct_el = soup.select_one(f"[aria-label='{s} stars represent']") or \
                     soup.select_one(f"[aria-label='{s} star represents']")
            if pct_el:
                m = re.search(r"([\d.]+)%", pct_el.get("aria-label",""))
                if m:
                    stars[s] = float(m.group(1))

        return rating, count, stars
    except Exception as e:
        print(f"  ERROR scraping {url}: {e}")
        return None, None, {}


def update_trends(trends, product_id, label, rating, count, stars):
    """Append today's entry to trends[product_id], carrying forward star %s if not scraped."""
    if product_id not in trends:
        trends[product_id] = {"label": label, "daily": []}

    existing = trends[product_id]["daily"]

    # skip if we already have today's entry
    if existing and existing[-1]["d"] == TODAY:
        print(f"  {label}: already has today's entry, skipping")
        return

    if rating is None or count is None:
        print(f"  {label}: scrape failed, skipping")
        return

    # carry forward star percentages from last known entry if not freshly scraped
    last = existing[-1] if existing else {}
    p5 = stars.get(5, last.get("p5", 0))
    p4 = stars.get(4, last.get("p4", 0))
    p3 = stars.get(3, last.get("p3", 0))
    p2 = stars.get(2, last.get("p2", 0))
    p1 = stars.get(1, last.get("p1", 0))

    entry = {
        "d":  TODAY,
        "r":  round(rating, 2),
        "t":  count,
        "p5": round(p5, 1), "p4": round(p4, 1), "p3": round(p3, 1),
        "p2": round(p2, 1), "p1": round(p1, 1),
        "c5": round(count * p5 / 100),
        "c4": round(count * p4 / 100),
        "c3": round(count * p3 / 100),
        "c2": round(count * p2 / 100),
        "c1": round(count * p1 / 100),
    }
    existing.append(entry)
    print(f"  {label}: {rating} ★  {count:,} reviews  → added")


def update_competitor(comp_data, key, rating, count, stars):
    """Append today's entry to competitors_data[key].daily."""
    if key not in comp_data:
        return
    cv = comp_data[key]
    existing = cv.setdefault("daily", [])

    if existing and existing[-1]["d"] == TODAY:
        print(f"  {cv.get('label', key)}: already updated, skipping")
        return

    if rating is None or count is None:
        print(f"  {cv.get('label', key)}: scrape failed, skipping")
        return

    last = existing[-1] if existing else {}
    p5 = stars.get(5, last.get("p5", 0))
    p4 = stars.get(4, last.get("p4", 0))
    p3 = stars.get(3, last.get("p3", 0))
    p2 = stars.get(2, last.get("p2", 0))
    p1 = stars.get(1, last.get("p1", 0))

    entry = {
        "d": TODAY, "r": round(rating, 2), "t": count,
        "p5": round(p5,1), "p4": round(p4,1), "p3": round(p3,1),
        "p2": round(p2,1), "p1": round(p1,1),
        "c5": round(count*p5/100), "c4": round(count*p4/100),
        "c3": round(count*p3/100), "c2": round(count*p2/100),
        "c1": round(count*p1/100),
    }
    existing.append(entry)
    print(f"  {cv.get('label', key)}: {rating} ★  {count:,} reviews  → added")


def main():
    print(f"\n=== Amazon scraper — {TODAY} ===\n")

    # load existing data
    with open(os.path.join(BASE, "trends_data.json"))      as f: trends    = json.load(f)
    with open(os.path.join(BASE, "competitors_data.json")) as f: comp_data = json.load(f)
    with open(os.path.join(BASE, "live_snapshot.json"))    as f: snapshot  = json.load(f)

    # ── Native products ───────────────────────────────────────────────────
    print("Native products:")
    for p in NATIVE_PRODUCTS:
        print(f"  Scraping {p['label']}...")
        rating, count, stars = scrape(p["url"])
        update_trends(trends, p["id"], p["label"], rating, count, stars)

        # also update live snapshot so the Live Ratings tab shows fresh numbers
        if rating is not None and count is not None:
            prev = snapshot["products"].get(p["id"], {})
            snapshot["products"][p["id"]] = {
                "rating":       rating,
                "review_count": count,
                "monthly_buys": prev.get("monthly_buys"),
            }

    snapshot["updated"] = TODAY

    # ── Competitors ───────────────────────────────────────────────────────
    print("\nCompetitors:")
    for key, cv in comp_data.items():
        url = cv.get("url", "")
        if not url:
            continue
        print(f"  Scraping {cv.get('label', key)}...")
        rating, count, stars = scrape(url)
        update_competitor(comp_data, key, rating, count, stars)

    # ── Save ──────────────────────────────────────────────────────────────
    with open(os.path.join(BASE, "trends_data.json"),      "w") as f: json.dump(trends,    f)
    with open(os.path.join(BASE, "competitors_data.json"), "w") as f: json.dump(comp_data, f)
    with open(os.path.join(BASE, "live_snapshot.json"),    "w") as f: json.dump(snapshot,  f, indent=2)

    print("\n✓ Data files saved.")


if __name__ == "__main__":
    main()
