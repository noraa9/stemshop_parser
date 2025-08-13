import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

def main():
    BASE_DIR = r"C:\Users\Lenovo\Desktop\project\parser"
    OUTPUT_FILE = os.path.join(BASE_DIR, "data", "competitors", "bambu-lab", "dbn.json")
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36"
    }

    url = "https://dbn.kz/3d-printery/q1-pro/"
    r = requests.get(url, headers=headers, timeout=15)
    # Қателерге
    r.raise_for_status()

    # html = r.text
    # with open("dbn_page.html", "w", encoding="utf-8") as file:
    #     file.write(html)

    soup = BeautifulSoup(r.text, "html.parser")

    products = soup.find_all("div", class_="main__item-info")

    parsed_data = []

    for product in products:
        title_tag = product.find("a", class_="main__item-title")
        price_tag = product.find("div", class_="main__item-price")

        title = title_tag.text.strip() if title_tag else "No Title"
        link = title_tag["href"] if title_tag and title_tag.has_attr("href") else "No Link"
        price = price_tag.text.strip() if price_tag else "No Price"

        parsed_data.append({
            "title": title,
            "price": price,
            "link": link,
        })

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        import json
        json.dump(parsed_data, file, ensure_ascii=False, indent=2)

    print(f"[{datetime.now()}] Парсинг завершён, найдено {len(parsed_data)} товаров")

if __name__ == "__main__":
    main()