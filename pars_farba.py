import requests
from bs4 import BeautifulSoup as bs
import os
import csv
import datetime
# "Komplektujuschie","2873", "Kompjuternaja-mebel","bytovaya","ohrannye-sistemy","svet-i-jelektrika","uslugi","avtojelektronika","rashodnye-materialy","Подарочные сертификаты","Programmnoe-obespechenie"
# "Komplektujuschie", "2873", "Kompjuternaja-mebel", "bytovaya", "ohrannye-sistemy", "svet-i-jelektrika",          "uslugi", "avtojelektronika", "rashodnye-materialy",
razdel = ["kamen-4082","novogodnij-dekor-4092","suxie-stroitelnye-smesi-i-gidroizolyaciya-2263","teploizolyaciya-i-shumoizolyaciya-3919"]
# Python3 code here creating class


class price_item:
    def __init__(self, id, category, sub_category, name, price, current_date):
        self.id = id
        self.category = category
        self.sub_category = sub_category
        self.name = name
        self.price = price
        self.current_date = current_date

## catalogs_element
def get_catalogs(url_base):
    catalogs=[]
    try:

        response = requests.get(url_base)

        soup = bs(response.text, "html.parser")

        catalogs_element = soup.find_all("li",{"class":"cat-item"})
        # print(catalogs_element)
        for catalog_element in catalogs_element:
            # print(catalog_element)
            catalog = catalog_element.find("a")
            # print(catalog)
            catalog_text=catalog.get("href")
            # print(catalog_text)
            catalogs.append(catalog_text)
            # print(catalog)
        return catalogs
    except:
        print("Ошибка получения списка какталогов")
    
    
    
os.system('cls')
base_url = "http://www.farba.md"
# ['https://hi-tech.md/kompyuternaya-tehnika/page-2/']
razdel = get_catalogs("http://www.farba.md/category")
# field names
fields = ['#', 'catalog', 'sub category','Name', 'Price','date']
rows = []

now = datetime.datetime.now().strftime('%d.%m.%Y')
pages = 2
category = ""
current_date = now
print("Парсинг начат ...")
for cat in razdel:
    url = base_url+cat+"/"
    i = 1
    while True:
        response = ""
        # if pages < i:
        #     break
        if i > 1:
            try:
                test_url = url+"?page="+str(i)+"&orderbyf=date&grid_mode=False"
                print("Обрабатывается страница: ", test_url)
                response = requests.get(test_url)  
                soup = bs(response.text, "html.parser")
            except:
                break
        else:
            print(url)
            response = requests.get(url)
            soup = bs(response.text, "html.parser")

            try:
                category = soup.find("h3",{"class":"breadcrumb"}).find_all("span")[-1].text
                print("Категория:", category, " Cтраница:", i)
            except:
                print("Все просмотрели")
                break
                # print(response)

        try:

            items =soup.find_all("li", {"class": "product-small"})

            for item in items:

                id_element = item.find("div", {"class": "quick-view"})

                title_element = (
                    item.find("p", {"class": "view-prod-name"}))

                price_element = item.find("span", {"class": "woocommerce-Price-amount"})
                sub_category_element =  item.find("p",{"class":"view-prod-category"})
                sub_category =  sub_category_element.text if sub_category_element else "none"
                id = id_element.get('data-prod') if id_element else " non"
                title = title_element.get_text(separator=' ', strip=True) if title_element else "no title"
                price = price_element.text if price_element else "0"

                print(id, category, sub_category, title, price, current_date)

                # print (id,title, price)

                rows.append(price_item(id, category, sub_category, title, price, current_date))
            if len(items)==0:
                break
            i = i+1
        except:
            print("Ошибка поиска карточки")
            break
print("Парсинг завершен.")
print("Начато сохранение")
with open('data_farba.csv', 'w',newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(fields)
    for el in rows:
        writer.writerow([el.id, el.category, el.sub_category, el.name, el.price,el.current_date])
print("Сохранение завершено, спасибо за работу.")
