
# import json
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# from pathlib import Path
#
#
# def load_json(path):
#     with open(path, encoding="utf-8") as file:
#         return json.load(file)
#
# def parse_price(price_str):
#     try:
#         price_float = float(price_str.replace(",", "."))
#         return int(price_float)
#     except Exception:
#         return None
#
# def load_all_jsons(folder: Path):
#     all_data = []
#     for json_file in folder.rglob("*.json"):
#         try:
#             data = load_json(json_file)
#             source_name = json_file.stem
#             if isinstance(data, list):
#                 for item in data:
#                     if isinstance(item, dict):
#                         item['competitor_source'] = source_name
#                 all_data.extend(data)
#             elif isinstance(data, dict):
#                 data['competitor_source'] = source_name
#                 all_data.append(data)
#         except Exception as e:
#             print(f"Ошибка при загрузке {json_file}: {e}")
#     return all_data
#
#
# def compare_prices(our_products, competitor_products):
#     comparison = []
#     seen = set()
#     for our in our_products:
#         our_title_first_word = our.get("title", "").split()[0].lower() if our.get("title") else ""
#         our_price_str = our.get("price", "")
#         try:
#             our_price = int(''.join(filter(str.isdigit, our_price_str)))
#         except:
#             our_price = None
#         for comp in competitor_products:
#             comp_title = comp.get("title", "").lower()
#             comp_price_str = comp.get("price", "")
#             try:
#                 comp_price = int(''.join(filter(str.isdigit, comp_price_str)))
#             except:
#                 comp_price = None
#
#             comp_link = comp.get("url") or comp.get("link") or ""
#
#             # Проверяем условие совпадения по первому слову названия
#             if our_title_first_word and our_title_first_word in comp_title:
#                 key = (our.get("title"), comp.get("title"))
#                 if key in seen:
#                     continue
#                 diff = None
#                 if our_price is not None and comp_price is not None:
#                     diff = our_price - comp_price
#
#                 competitor_source = comp.get("competitor_source", "unknown")
#
#                 comparison.append([
#                     our.get("title"),
#                     our_price,
#                     comp.get("title"),
#                     comp_price,
#                     diff,
#                     competitor_source,
#                     comp_link
#                 ])
#                 seen.add(key)
#     return comparison
#
#
# def upload_to_sheets(data):
#     scope = ["https://spreadsheets.google.com/feeds",
#              "https://www.googleapis.com/auth/spreadsheets",
#              "https://www.googleapis.com/auth/drive.file",
#              "https://www.googleapis.com/auth/drive"]
#
#     creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
#     client = gspread.authorize(creds)
#
#     sheet = client.open("Price Comparison").sheet1
#     sheet.clear()
#
#     # Заголовки
#     sheet.append_row(["Our Product", "Our Price", "Competitor Product", "Competitor Price", "Difference", "Competitor", "Competitor Link"])
#
#     # Добавляем сразу все данные пачкой
#     sheet.append_rows(data, value_input_option='USER_ENTERED')
#
#
# if __name__ == "__main__":
#     BASE_DIR = Path("data")
#     our_folder = BASE_DIR / "stemshop"
#     competitors_folder = BASE_DIR / "competitors"
#
#     print("Загружаем наши товары...")
#     our_products = load_all_jsons(our_folder)
#
#     all_results = []
#
#     # Проходим по всем папкам конкурентов
#     for competitor_subfolder in competitors_folder.iterdir():
#         if competitor_subfolder.is_dir():
#             competitor_name = competitor_subfolder.name
#             print(f"Загружаем товары конкурента: {competitor_name}")
#             competitor_products = load_all_jsons(competitor_subfolder)
#             print(f"Сравниваем с товарами конкурента {competitor_name}...")
#             comparison = compare_prices(our_products, competitor_products)
#             all_results.extend(comparison)
#
#     print(f"Итого найдено сравнений: {len(all_results)}")
#     print("Загружаем результаты в Google Sheets...")
#     upload_to_sheets(all_results)
#     print("✅ Данные обновлены в Google Sheets")

import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
from datetime import datetime


# -------------------- Загрузка JSON --------------------
def load_json(path):
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def load_all_jsons(folder: Path):
    all_data = []
    for json_file in folder.rglob("*.json"):
        try:
            data = load_json(json_file)
            source_name = json_file.stem
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):  # только словари
                        item['competitor_source'] = source_name
                        all_data.append(item)
                    else:
                        print(f"[ОШИБКА] {json_file} — элемент не словарь: {item!r}")
            elif isinstance(data, dict):
                data['competitor_source'] = source_name
                all_data.append(data)
            else:
                print(f"[ОШИБКА] {json_file} — данные не список и не словарь")
        except Exception as e:
            print(f"[ОШИБКА] При загрузке {json_file}: {e}")
    return all_data


# -------------------- Парсинг цены --------------------
def parse_price(price_str):
    try:
        digits = ''.join(filter(lambda c: c.isdigit() or c=='.', price_str))
        return int(float(digits)) if digits else None
    except:
        return None


# -------------------- Сравнение названий --------------------
def title_match(our_title, comp_title, min_overlap=0.5):
    our_words = set(our_title.lower().split())
    comp_words = set(comp_title.lower().split())
    if not our_words:
        return False
    overlap = len(our_words & comp_words) / len(our_words)
    return overlap >= min_overlap


# -------------------- Сравнение цен --------------------
def compare_prices(our_products, competitor_products):
    comparison = []
    seen = set()
    for our in our_products:
        our_title = our.get("title", "")
        our_price = parse_price(str(our.get("price", "")))

        for comp in competitor_products:
            comp_title = comp.get("title", "")
            comp_price = parse_price(str(comp.get("price", "")))
            comp_link = comp.get("url") or comp.get("link") or ""
            competitor_source = comp.get("competitor_source", "unknown")

            if title_match(our_title, comp_title):
                key = (our_title, comp_title)
                if key in seen:
                    continue
                diff = None
                if our_price is not None and comp_price is not None:
                    diff = our_price - comp_price

                comparison.append([
                    our_title,
                    our_price,
                    comp_title,
                    comp_price,
                    diff,
                    competitor_source,
                    comp_link,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ])
                seen.add(key)
    return comparison



# -------------------- Загрузка в Google Sheets --------------------
def upload_to_sheets(data):
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file",
             "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open("Price Comparison").sheet1
    sheet.clear()
    sheet.append_row(["Our Product", "Our Price", "Competitor Product", "Competitor Price",
                      "Difference", "Competitor", "Competitor Link", "Timestamp"])
    sheet.append_rows(data, value_input_option='USER_ENTERED')


# -------------------- Главный блок --------------------


if __name__ == "__main__":
    BASE_DIR = Path("data")
    our_folder = BASE_DIR / "stemshop"
    competitors_folder = BASE_DIR / "competitors"

    print("Загружаем наши товары...")
    our_products = load_all_jsons(our_folder)

    all_results = []

    # Проходим по всем папкам конкурентов
    for competitor_subfolder in competitors_folder.iterdir():
        if competitor_subfolder.is_dir():
            competitor_name = competitor_subfolder.name
            print(f"Загружаем товары конкурента: {competitor_name}")
            competitor_products = load_all_jsons(competitor_subfolder)
            print(f"Сравниваем с товарами конкурента {competitor_name}...")
            comparison = compare_prices(our_products, competitor_products)
            all_results.extend(comparison)

    print(f"Итого найдено сравнений: {len(all_results)}")
    print("Загружаем результаты в Google Sheets...")
    upload_to_sheets(all_results)
    print("✅ Данные обновлены в Google Sheets")
