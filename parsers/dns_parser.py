# # import requests
# # import json
# # import os
# # import urllib.parse
# #
# # BASE_DIR = r"C:\Users\Lenovo\Desktop\project\parser"
# # INPUT_FILE = os.path.join(BASE_DIR, "data", "stemshop", "bambu-lab.json")
# # OUTPUT_FILE = os.path.join(BASE_DIR, "data", "competitors", "dns", "bambu-lab.json")
# #
# # SEARCH_URL = "https://restapi.dns-shop.kz/v1/get-presearch"
# #
# # HEADERS = {
# #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
# #     "Accept": "application/json, text/plain, */*",
# #     "Referer": "https://www.dns-shop.kz/",
# # }
# #
# # def search_dns(product_name):
# #     params = {"query": product_name}
# #     try:
# #         r = requests.get(SEARCH_URL, params=params, headers=HEADERS, timeout=10)
# #         r.raise_for_status()
# #         return r.json()
# #     except Exception as e:
# #         print(f"Ошибка при запросе '{product_name}': {e}")
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
# #         data = search_dns(title)
# #         if not data or "data" not in data:
# #             print(f"❌ No results for {title}")
# #             continue
# #
# #         found_item = None
# #         for suggestion in data["data"]:
# #             if title.lower().split()[0] in suggestion.get("name", "").lower():
# #                 found_item = suggestion
# #                 break
# #
# #         if found_item:
# #             product_data = {
# #                 "title": found_item.get("name"),
# #                 "price": found_item.get("price"),
# #                 "url": urllib.parse.urljoin("https://www.dns-shop.kz", found_item.get("url", "")),
# #             }
# #             if product_data not in results:
# #                 results.append(product_data)
# #         else:
# #             print(f"⚠ No matching product found for {title}")
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
# import requests
# import json
#
# url = "https://www.dns-shop.kz/product/microdata/699eac77-2d27-11eb-a211-00155d03332b/"
#
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
# }
#
# response = requests.get(url, headers=headers)
# data = response.json()
#
# product = data.get("data", {})
#
# title = product.get("name")
# price = product.get("offers", {}).get("price")
# product_url = product.get("offers", {}).get("url")
#
# print(f"Название: {title}")
# print(f"Цена: {price} KZT")
# print(f"URL: {product_url}")
