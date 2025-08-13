import requests
import json
import os

BASE_DIR = r"C:\Users\Lenovo\Desktop\project\parser\data\stemshop"
os.makedirs(BASE_DIR, exist_ok=True)

brands = [
    "axon",
    "lego-education",
    "lego-classic",
    "robowunderkind",
    "bambu-lab",
    "dobot",
    "misumi",
    "swyft"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

BASE_COLLECTION_URL = "https://www.stemshop.kz/front_api/collection/{brand}?max_filter_items=50&page={page}"
BASE_PRODUCT_URL = "https://www.stemshop.kz/products_by_id/{ids}.json?accessories=true"

def get_all_product_ids(brand):
    """Собираем все product_id для бренда"""
    ids = []
    page = 1
    while True:
        url = BASE_COLLECTION_URL.format(brand=brand, page=page)
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        data = r.json()
        batch = data.get("products_ids", [])
        if not batch:
            break
        ids.extend(batch)
        page += 1
    return list(set(ids))

def get_products_by_ids(ids):
    """Получаем только нужные поля товаров"""
    results = []
    for i in range(0, len(ids), 50):
        chunk = ids[i:i+50]
        url = BASE_PRODUCT_URL.format(ids=",".join(map(str, chunk)))
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        data = r.json()
        for prod in data.get("products", []):
            title = prod.get("title", "")
            sku = None
            price = None
            if prod.get("variants"):
                price = prod["variants"][0].get("price", None)
                sku = prod["variants"][0].get("sku", None)
            link = "https://www.stemshop.kz" + prod.get("url", "")
            results.append({
                "title": title,
                "sku": sku,
                "price": price,
                "url": link
            })
    return results

def parse_brand(brand):
    print(f"Парсим бренд: {brand}")
    ids = get_all_product_ids(brand)
    print(f"  Найдено товаров: {len(ids)}")
    if not ids:
        return
    products = get_products_by_ids(ids)
    file_path = os.path.join(BASE_DIR, f"{brand}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    print(f"  Сохранено в {file_path}")


def main():
    for b in brands:
        parse_brand(b)

if __name__ == "__main__":
  main()


