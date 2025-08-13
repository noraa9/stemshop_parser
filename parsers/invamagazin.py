# import requests
# from bs4 import BeautifulSoup
# import json
# import os
# import time
#
# BASE_DIR = r"C:\Users\Lenovo\Desktop\project\parser"
# INPUT_FILE = os.path.join(BASE_DIR, "data", "stemshop", "dobot.json")
# OUTPUT_DIR = os.path.join(BASE_DIR, "data", "competitors", "dobot")
# OUTPUT_FILE = os.path.join(OUTPUT_DIR, "invamagazin.json")
#
# BASE_URL = "https://invamagazin.kz"
# SEARCH_URL = BASE_URL + "/site_search"
#
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                   "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
# }
#
# def search_prod():
#     params = {"search_term": "dobot"}
#     r = requests.get(SEARCH_URL, params=params, headers=headers)
#     r.raise_for_status()
#     soup = BeautifulSoup(r.text, "lxml")
#
#     results = []
#     script_tags = soup.find_all("script", type="application/ld+json")
#
#     for script in script_tags:
#         try:
#             data = json.loads(script.string.strip())
#             if isinstance(data, dict) and data.get("@type") == "Product":
#                 name = data.get("name", "")
#                 if "dobot" in name.lower():
#                     offers = data.get("offers", {})
#                     price = offers.get("price")
#                     rel_url = offers.get("url")
#                     url = BASE_URL + rel_url if rel_url else None
#
#                     results.append({
#                         "title": name,
#                         "price": price,
#                         "link": url
#                     })
#         except Exception as e:
#             print(f"Error parsing product: {e}")
#             continue
#
#     return results
#
#
#
# def main():
#     inva_products = search_prod()  # всего один запрос
#
#     os.makedirs(OUTPUT_DIR, exist_ok=True)
#     with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
#         json.dump(inva_products, file, ensure_ascii=False, indent=2)
#
#     print(f"Найдено {len(inva_products)} товаров")
#     print(f"Результаты сохранены в {OUTPUT_FILE}")
#
# if __name__ == "__main__":
#     main()
