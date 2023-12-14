import requests
from bs4 import BeautifulSoup as bs
import os
import csv
# "Komplektujuschie","2873", "Kompjuternaja-mebel","bytovaya","ohrannye-sistemy","svet-i-jelektrika","uslugi","avtojelektronika","rashodnye-materialy","Подарочные сертификаты","Programmnoe-obespechenie"
# "Komplektujuschie", "2873", "Kompjuternaja-mebel", "bytovaya", "ohrannye-sistemy", "svet-i-jelektrika",          "uslugi", "avtojelektronika", "rashodnye-materialy",
razdel = ["Komplektujuschie", "2873", "Kompjuternaja-mebel", "bytovaya", "ohrannye-sistemy", "svet-i-jelektrika",
          "uslugi", "avtojelektronika", "rashodnye-materialy", "Подарочные сертификаты", "Programmnoe-obespechenie"]
# Python3 code here creating class


class price_item:
    def __init__(self, id, category, name, price):
        self.id = id
        self.category = category
        self.name = name
        self.price = price


os.system('cls')
base_url = "https://tiraet.com/catalog/"
# ['https://hi-tech.md/kompyuternaya-tehnika/page-2/']

# field names
fields = ['#', 'catalog', 'Name', 'Price']
rows = []


# try:
#     response = requests.get(base_url)
#     soup_base = bs(response.text,"html.parser")
#     category= soup.find("h1").find("span").text

# except:
#     print("Ошибка получения главной страницы:"+ base_url)
#            # перебор подкатегорий
# ty-subcategories__item
# sub_categorys= soup.find_all("li", {"class": "ty-subcategories__item"})
# for sub_category in  sub_categorys:
#     sub_link = sub_category.find("a").get("href")
#     sub_title=sub_category.find("span").text
#     print(sub_title, sub_link )
#
pages = 2
category = ""
print("Парсинг начат ...")
for cat in razdel:
    url = base_url+cat+"/"
    i = 1
    while True:
        response = ""
        if pages < i:
            break
        if i > 1:
            try:
                test_url = url+"?PAGEN_1="+str(i)
                print("Обрабатывается страница: ", test_url)
                response = requests.get(test_url)  # ?PAGEN_1=2
                soup = bs(response.text, "html.parser")
            except:
                break
        else:
            response = requests.get(url)
            soup = bs(response.text, "html.parser")
            pagination = soup.find("div", {"class": "module-pagination"})

            pages = int(pagination.find_all(
                "a", {"class": "dark_link"})[-1].text) if pagination else 1
            # print(pages)
            try:
                category = soup.find("h1").text
                print("Категория:", category, " Cтраниц:", pages)
            except:
                print("Все просмотрели")
                break
                # print(response)

        try:
            for item in soup.find_all("div", {"class": "catalog-block-view__item"}):
                id_element = item.find("div", {"class": "article_block"})
                title_element = (
                    item.find("a", {"class": "js-notice-block__title"}))
                price_element = item.find("span", {"class": "price_value"})

                id = id_element.get('data-value') if id_element else " non"
                title = title_element.text if title_element else "no title"
                price = price_element.text if price_element else "0"

                # print(id,category,title, price)

                # print (id,title, price)

                rows.append(price_item(id, category, title, price))
            i = i+1
        except:
            print("Ошибка поиска карточки")
print("Парсинг завершен.")
print("Начато сохранение")
with open('data_tiraet.csv', 'w',) as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(fields)
    for el in rows:
        writer.writerow([el.id, el.category, el.name, el.price])
print("Сохранение завершено, спасибо за работу.")
