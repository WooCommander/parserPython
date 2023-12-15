import requests
from bs4 import BeautifulSoup as bs
import os
import csv
# "Komplektujuschie","2873", "Kompjuternaja-mebel","bytovaya","ohrannye-sistemy","svet-i-jelektrika","uslugi","avtojelektronika","rashodnye-materialy","Подарочные сертификаты","Programmnoe-obespechenie"
# "Komplektujuschie", "2873", "Kompjuternaja-mebel", "bytovaya", "ohrannye-sistemy", "svet-i-jelektrika",          "uslugi", "avtojelektronika", "rashodnye-materialy",
razdel = ["transport"]
# Python3 code here creating class


class price_item:
    def __init__(self, id, category, name, price):
        self.id = id
        self.category = category
        self.name = name
        self.price = price


os.system('cls')
base_url = "https://makler.md/ru/transnistria/"
# https://makler.md/ru/transnistria/transport?page=302

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
        if 2 < i:
            break
        if i > 1:
            try:
                test_url = url+"?page="+str(i)
                print("Обрабатывается страница: ", test_url)
                response = requests.get(test_url)  
                soup = bs(response.text, "html.parser")
            except:
                break
        else:
            response = requests.get(url)
            soup = bs(response.text, "html.parser")
            # pagination = soup.find("div", {"class": "module-pagination"})

            # pages = int(pagination.find_all(
            #     "a", {"class": "dark_link"})[-1].text) if pagination else 1
            # print(pages)
            try:
                category = soup.find("div",id="contentWrapper").find_all("nav")[0].find_all("li", {"class":"pl"})[-1].get_text(separator=' ', strip=True)
                print("Категория:", category)
            except:
                print("Все просмотрели")
                break
                # print(response)

        try:
            items= soup.find("div",id="contentWrapper").find_all("article")
            # print(items[0])
            if not items: 
                # если нет блока объявлений
               break 
            for item in items:
                id_element = item.get("id")
                # print(id_element)
                title_element = (
                    item.find("div", {"class": "subfir"}))
                # print(title_element)
                # price_element = item.find('br', string='Цена:').find_next_sibling(text=True, strip=True)
                price_element = item.find("span", {"class":"ls-detail_price"})
                id = id_element
                title = title_element.get_text(separator=' ', strip=True) if title_element else "no title"
                # title = f'"{title}"'
                price = price_element.text if price_element else "0"
                print(id, title,price)
                # print(id,category,title, price)

                # print (id,title, price)

                rows.append(price_item(id, category, title, price))
            i = i+1
        except:
            print("Ошибка поиска карточки")
print("Парсинг завершен.")
print("Начато сохранение")
with open('data_makler.csv', 'w',newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter='^')

    csv_writer.writerow(fields)
    for el in rows:
        csv_writer.writerow([el.id, el.category, el.name, el.price])
print("Сохранение завершено, спасибо за работу.")
