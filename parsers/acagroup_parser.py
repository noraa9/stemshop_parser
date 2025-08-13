import requests
from bs4 import BeautifulSoup
import os
import json
import time

BASE_DIR = r"C:\Users\Lenovo\Desktop\project\parser"
INPUT_FILE = os.path.join(BASE_DIR, "data", "stemshop", "lego-education.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "competitors", "lego-education", "acagroup.json")

BASE_URL = "https://acagroup.kz"
CATEGORY_URL = "https://acagroup.kz/p70083006-konstruktor-lego-education.html"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}


def find_acagroup_product(sku):
    search_url = f"{BASE_URL}/site_search?search_term={sku}"
    r = requests.get(search_url, headers=HEADERS, timeout=10)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "lxml")
    results = []

    for card in soup.find_all("div", class_="b-product-gallery__header"):
        title_tag = card.find("a", class_="b-product-gallery__title")
        price_tag = card.find("span", class_="b-product-gallery__current-price")

        title = title_tag.text.strip() if title_tag else None
        price = price_tag.text.strip() if price_tag else None
        url = BASE_URL + title_tag["href"] if title_tag and title_tag.has_attr("href") else None
        results.append({
            "title": title,
            "price": price,
            "url": url
        })

    return results


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        stemshop_prod = json.load(file)

    my_skus = [
        str(p["sku"]).lower()
        for p in stemshop_prod
        if p.get("sku")  # пропускаем, если sku нет или None
    ]

    results = []
    for my_sku in my_skus:
        print(f"Searching for {my_sku}")
        prod_list = find_acagroup_product(my_sku)
        print(prod_list)
        for prod in prod_list:
            results.append(prod)
        time.sleep(2)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(results, file, ensure_ascii=False, indent=2)

    print(f"Готово! Найдено {len(results)} совпадений. Сохранено в {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
