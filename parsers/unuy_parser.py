# import requests
# from lxml import html
#
# # 1. Сначала идём на главную страницу, чтобы получить cookies и токен
# session = requests.Session()
# url_main = "https://www.dns-shop.kz/"
# resp = session.get(url_main, headers={
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
# })
# tree = html.fromstring(resp.text)
#
# # Пытаемся достать csrf_token (если он есть в meta)
# csrf_token = tree.xpath('//meta[@name="csrf-token"]/@content')
# csrf_token = csrf_token[0] if csrf_token else None
#
# print("CSRF Token:", csrf_token)
# print("Cookies:", session.cookies.get_dict())
#
# # 2. Теперь идём на твой API/JSON URL уже с cookies и токеном
# product_url = "https://www.dns-shop.kz/product/microdata/699eac77-2d27-11eb-a211-00155d03332b/"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
#     "Referer": url_main
# }
# if csrf_token:
#     headers["X-CSRF-Token"] = csrf_token
#
# resp2 = session.get(product_url, headers=headers)
# print("Status:", resp2.status_code)
# print("Content:", resp2.text)
#
# #
# # def search_ubuy(product_name):
# #     params = {
# #         "ubuy": "es1",
# #         "dtm": "1",
# #         "ubt": "ubuy",
# #         "cfv": "cf-5",
# #         "docType": "offRHF",
# #         "q": product_name,
# #         "node_id": "",
# #         "page": "1",
# #         "brand": "misumi",
# #         "ufulfilled": "",
# #         "price_range": "",
# #         "sort_by": "",
# #         "s_id": "436",
# #         "lang": "",
# #         "dc": "",
# #         "search_type": "brand",
# #         "skus": "",
# #         "store": "us",
# #         # csrf_token можно попробовать убрать, если без него работает
# #         "csrf_token": "",
# #         "ppcNewurl": "0",
# #         "currency": ""
# #     }
# #     try:
# #         r = requests.get(SEARCH_URL, params=params, headers=HEADERS, timeout=10)
# #         r.raise_for_status()
# #         return r.json()
# #     except Exception as e:
# #         print(f"Ошибка при запросе {product_name}: {e}")
# #         return None
# #
# # def main():
# #     with open(INPUT_FILE, "r", encoding="utf-8") as file:
# #         stemshop_products = json.load(file)
# #
# #     results = []
# #
# #     for product in stemshop_products:
# #         title = product["title"]
# #         print(f"Searching for: {title}")
# #
# #         data = search_ubuy(title)
# #         if not data or "products" not in data:
# #             print(f"❌ No results for {title}")
# #             continue
# #
# #         found_item = None
# #         for item in data["products"]:
# #             if title.lower().split()[0] in item.get("product_title", "").lower():
# #                 found_item = item
# #                 break
# #
# #         if found_item:
# #             product_data = {
# #                 "title": found_item.get("product_title"),
# #                 "price": found_item.get("product_price"),
# #                 "url": found_item.get("seo_url"),
# #             }
# #             if product_data not in results:
# #                 results.append(product_data)
# #         else:
# #             print(f"⚠ No matching product found for {title}")
# #
# #         time.sleep(1)  # задержка чтобы не банили
# #
# #     os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
# #
# #     with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
# #         json.dump(results, file, ensure_ascii=False, indent=2)
# #
# #     print(f"✅ Done! Data saved in {OUTPUT_FILE}")
# #
# # if __name__ == "__main__":
# #     main()
#
#
