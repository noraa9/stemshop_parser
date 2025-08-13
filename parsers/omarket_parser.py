# import requests
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from bs4 import BeautifulSoup
#
# options = Options()
# options.add_argument("--headless")
#
# driver = webdriver.Chrome(options=options)
# driver.get("https://omarket.kz/catalog/search?query=AXON")
#
# import time
# time.sleep(5)
#
# html = driver.page_source
# driver.quit()
#
# soup = BeautifulSoup(html, "html.parser")
# product_cards = soup.select("div.-m-3")
#
# for pro in product_cards:
#     print(pro.text)
#
# # url = "https://omarket.kz/catalog/search"
# # params = {
# #     "query": "AXON"
# # }
# #
# # headers = {
# #     "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36"
# # }
# #
# # r = requests.get(url, params=params, headers=headers, timeout=15)
# # r.raise_for_status()
# # html = r.text
# #
# # with open("page.html", "w", encoding="utf-8") as f:
# #     f.write(html)
# # soup = BeautifulSoup(html, "html.parser")
# #
# # product_cards = soup.find_all("div", class_=lambda classes: classes and "-m-3" in classes.split())
# # for pro in product_cards:
# #     print(pro.text)
# #
#
