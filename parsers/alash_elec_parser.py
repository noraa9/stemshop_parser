import requests
import json
import os

BASE_DIR = r"C:\Users\Lenovo\Desktop\project\parser"
INPUT_FILE = os.path.join(BASE_DIR, "data", "stemshop", "axon.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "competitors","axon", "alash_elec.json")

SEARCH_URL = "https://alash-electronics.kz/search_suggestions"

def search_alash(product_name):
    params = {
        "fields[]": ["price_min", "price_min_available"],
        "account_id": "1229444",
        "hide_items_out_of_stock": "false",
        "locale": "ru",
        "query": product_name
    }
    try:
        r = requests.get(SEARCH_URL, params=params)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Ошибка при запросе {product_name}: {e}")
        return None

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        stemshop_products = json.load(file)

    results = []

    for product in stemshop_products:
        title = product["title"]
        print(f"Searching for ${title}")

        data = search_alash(title)
        if not data or "suggestions" not in data:
            continue

        found_item = None
        for suggestion in data["suggestions"]:
            if title.lower().split()[0] in suggestion["value"].lower():
                found_item = suggestion
                break

        if found_item:
            price = found_item["fields"].get("price_min")
            product_data = {
                "title": found_item["value"],
                "price": str(price) if price else None,
                "url": f"https://alash-electronics.kz/products_by_id/{found_item['data']}.json"
            }

            if product_data not in results:
                results.append(product_data)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(results, file, ensure_ascii=False, indent=2)

        print(f"Ready! Data saved in {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

