import requests
from bs4 import BeautifulSoup
import json
import os
import time
import random

base_url = "https://3dlife.kz"
search_url = "https://3dlife.kz/site_search"
BASE_DIR = r"C:\Users\Lenovo\Desktop\project\parser"
INPUT_FILE = os.path.join(BASE_DIR, "data", "stemshop", "bambu-lab.json")

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36"
}

def search_product(product_name):
    params = {"search_term": product_name}
    r = requests.get(search_url, params=params, headers=headers)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")
    script_tags = soup.find_all("script", type="application/ld+json")

    results = []
    for script in script_tags:
        try:
            data = json.loads(script.text)
            if data.get("@type") == "Product":
                title = data.get("name")
                price = data.get("offers", {}).get("price")
                currency = data.get("offers", {}).get("priceCurrency")
                rel_url = data.get("offers", {}).get("url")
                url = base_url + rel_url if rel_url else None

                results.append({
                    "title": title,
                    "price": price,
                    "currency": currency,
                    "link": url,
                })
        except Exception:
            continue
    return results


def main():
    # путь к JSON с товарами stemshop
    input_path = r"C:\Users\Lenovo\Desktop\project\parser\data\stemshop\bambu-lab.json"

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        stemshop_products = json.load(file)

    competitor_products = []

    for product in stemshop_products:
        name = product.get("title")
        print(f"🔍 Ищу: {name}")
        if not name:
            continue

        found_products = search_product(name)
        if found_products:
            competitor_products.append(found_products[0])  # берем первый найденный
            print(f"✅ Найдено: {found_products[0]['title']}")
        else:
            print(f"❌ Не найдено: {name}")

        # задержка 1–3 секунды
        time.sleep(random.uniform(1, 3))

    # сохраняем результат
    output_dir = r"C:\Users\Lenovo\Desktop\project\parser\data\competitors\bambu-lab"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "3dlife.json")

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(competitor_products, file, ensure_ascii=False, indent=2)

    print(f"📂 Результаты сохранены в {output_path}")


if __name__ == "__main__":
    main()