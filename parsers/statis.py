import requests
from bs4 import BeautifulSoup
import json
import os

BASE_DIR = r"C:\Users\Lenovo\Desktop\project\parser"
INPUT_FILE = os.path.join(BASE_DIR, "data", "stemshop", "dobot.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "competitors", "dobot", "statis.json")
BASE_URL = "https://statis.kz"

CATEGORY_URL = "https://statis.kz/search?search=DOBOT"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}

def parse_machineryline():
    r = requests.get(CATEGORY_URL, headers=HEADERS)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")

    products = []
    descriptions = soup.find_all("article", class_="product-card")

    for description in descriptions:
        # Название и ссылка
        title_tag = description.find("div", class_="product-card__title")
        a_tag = description.find("a", class_="product-card__content")
        price_tag = description.find("div", class_="product-card__price")

        title = title_tag.text.strip() if title_tag else None
        price = price_tag.text.strip() if price_tag else None
        link = BASE_URL + a_tag["href"] if a_tag else None


        products.append({
            "title": title,
            "price": price,
            "url": link
        })

    return products

def main():
    # Загружаем свои товары
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        my_products = json.load(file)
    my_titles = [p["title"].lower() for p in my_products]

    # Парсим сайт
    parsed_products = parse_machineryline()

    # Сверка
    results = []
    # Сверка с отладкой
    for prod in parsed_products:
        for my_title in my_titles:
            keywords = my_title.split()
            if all(word in prod["title"].lower() for word in keywords) and prod not in results:
                print(f"Точное совпадение: {my_title} -> {prod['title']}")
                results.append(prod)
                break

    # Сохраняем результат
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(results, file, ensure_ascii=False, indent=2)

    print(f"Готово! Найдено {len(results)} товаров. Данные сохранены в {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
