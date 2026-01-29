import requests
import re
import json
import time
import random
import pandas as pd

BASE_URL = "https://dir.indiamart.com/impcat/fly-ash-brick-making-machine.html"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-IN,en;q=0.9",
    "Referer": "https://www.indiamart.com/"
}


#This Code Helps us to get the HTML Code
def fetch_page(url):
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    return response.text

### I have downloaded HTML Code and Validated the data within the Website 
### the actual data is stored inside window\.__INITIAL_STATE__ block
### Sample HTML Code attached to verify
def extract_initial_state(html):
    pattern = r"window\.__INITIAL_STATE__\s*=\s*(\{.*?\})\s*;"
    match = re.search(pattern, html, re.DOTALL)

    if not match:
        raise ValueError("window.__INITIAL_STATE__ not found")

    json_text = match.group(1)
    return json.loads(json_text)


### Extarcting the data from the JSON
def normalize_products(state):
    rows = []

    products = state.get("data", [])

    for p in products:
        row = {
            "product_id": p.get("disp_id"),
            "product_name": p.get("p_nm") or p.get("f_nm"),
            "price_in_rupees": p.get("pr").replace("₹ ","").strip(),
            "supplier_name": p.get("CMP"),
            "supplier_website": p.get("s_url"),
            "city": p.get("city"),
            "address": p.get("ad"),
            "state": p.get("g_s"),
            "country": p.get("g_c"),
            "rating": p.get("wt_avg"),
            "review_count": p.get("tr_c"),
            "trust_badge": p.get("g_cn"),
            "gst_verified": bool(p.get("gst_v")),
            "years_experience": p.get("m_sn"),
            "response_rate": p.get("PF")
        }

        rows.append(row)

    return pd.DataFrame(rows)


### Main function that enters the pages and extracts that data
def crawl_indiamart(max_pages=6):
    all_dfs = []

    for page in range(1, max_pages + 1):
        print(f"Scraping page {page}...")

        url = f"{BASE_URL}?page={page}" if page > 1 else BASE_URL
        html = fetch_page(url)

        state = extract_initial_state(html)
        df_page = normalize_products(state)

        all_dfs.append(df_page)

        time.sleep(random.uniform(2, 6))

    return pd.concat(all_dfs, ignore_index=True)


### Main function that executes all the above funcions
if __name__ == "__main__":
    df = crawl_indiamart(max_pages=6)
    df.to_csv("data/indiamart_flyash_data.csv",index=False)
    print(f"Collected {len(df)} products")
