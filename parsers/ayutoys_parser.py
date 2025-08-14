import requests
from bs4 import BeautifulSoup
import json
import os
import time

BASE_DIR = r"C:\Users\Lenovo\Desktop\project\parser"
INPUT_FILE = os.path.join(BASE_DIR, "data", "stemshop", "lego-classic.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "competitors", "lego-classic", "ayutoys.json")
SEARCH_URL = "https://ayutoys.kz/site_search"
BASE_URL = "https://ayutoys.kz"

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36"
}

def search_product(sku):
    params = {"search_term": sku}
    r = requests.get(SEARCH_URL, params=params, headers=headers)
    r.raise_for_status()
    html = r.text
    soup = BeautifulSoup(html, "lxml")
    scripts = soup.find_all("script", type="application/ld+json")

    results = []
    for script in scripts:
        try:
            data = json.loads(script.text)
            if data.get("@type") == "Product":
                title = data.get("name")
                sku = data.get("sku")
                offers = data.get("offers", {})
                price = offers.get("price")
                rel_url = offers.get("url")
                url = BASE_URL + rel_url if rel_url else None

                results.append({
                    "title": title,
                    "price": price,
                    "link": url,
                    "sku": sku
                })
        except Exception as e:
            print(f"Error {e}")
            continue
    return results

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        stemshop_prod = json.load(file)

    competitor_prod = []

    for prod in stemshop_prod:
        name = prod.get("title")
        sku = prod.get("sku")
        print(f"Searching for {name}")
        if not sku:
            continue

        found_prod = search_product(sku)
        if found_prod :
            competitor_prod.append(found_prod[0])
        time.sleep(1)

    print(f'Найдено {len(competitor_prod)} товаров')
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(competitor_prod, file, ensure_ascii=False, indent=2)

    print(f"📂 Результаты сохранены в {OUTPUT_FILE}")

if __name__ == "__main__":
    main()