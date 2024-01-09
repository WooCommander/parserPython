import requests
from bs4 import BeautifulSoup as bs
import os
import csv
import datetime
from datetime import datetime

# "Komplektujuschie","2873", "Kompjuternaja-mebel","bytovaya","ohrannye-sistemy","svet-i-jelektrika","uslugi","avtojelektronika","rashodnye-materialy","Подарочные сертификаты","Programmnoe-obespechenie"
# "Komplektujuschie", "2873", "Kompjuternaja-mebel", "bytovaya", "ohrannye-sistemy", "svet-i-jelektrika",          "uslugi", "avtojelektronika", "rashodnye-materialy",
# razdel = ["kamen-4082", "novogodnij-dekor-4092", "suxie-stroitelnye-smesi-i-gidroizolyaciya-2263",
#           "teploizolyaciya-i-shumoizolyaciya-3919"]


# Python3 code here creating class

# модель записи таблицы
class price_item_model:
    def __init__(self, id_item: str, category: str, sub_category: str, name: str, price: str, current_date: str):
        self.id = id_item
        self.category = category
        self.sub_category = sub_category
        self.name = name
        self.price = price
        self.current_date = current_date


## catalogs_element
def get_catalogs(url_base):
    """
    Получение списка каталогов
    :param url_base:
    :return:
    """
    catalogs = []
    try:
        response = requests.get(url_base)
        soup = bs(response.text, "html.parser")
        catalogs_element = soup.find_all("li", {"class": "cat-item"})
        # print(catalogs_element)
        for catalog_element in catalogs_element:
            # print(catalog_element)
            catalog = catalog_element.find("a")
            # print(catalog)
            catalog_text = catalog.get("href")
            # print(catalog_text)
            catalogs.append(catalog_text)
            # print(catalog)
        return catalogs
    except:
        print("Ошибка получения списка какталогов")

class parse_const():
    base_url="https://zvezda.md"
    id_element=""
    id=""
    name_element=""

def save_to_csv(file_name, data_arr: [price_item_model]):
    """
    Сохранение данных в файл csv
    :param file_name: имя файла
    :param data_arr: массив строк
    :return:
    """
    fields = ['#', 'catalog', 'sub category', 'Name', 'Price', 'date']
    print("Парсинг завершен.")
    print("Начато сохранение")
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fields)
        for el in data_arr:
            writer.writerow([el.id, el.category, el.sub_category, el.name, el.price, el.current_date])
    print("Сохранение завершено, спасибо за работу.")


def get_row(item, category,sub_category):
    """
    Получение строки данных из html карточки товара
    :param item:
    :return: price_item
    """
    id_element = item.find("a",class_= "add_to_cart_button")
    # print("id_element",id_element)
    id: str = id_element['data-product_id'] if id_element else " non"
    # print("id:", id)
    
    title_element = (item.find("h2", class_="woocommerce-loop-product__title"))
    title: str = title_element.text if title_element else "no title"
    # print("title", title)
    
    price_element = item.find("bdi")
    
    price: str = price_element.text.replace("р.", "") if price_element else "0"
    # print("price:",price)   

    # sub_category_element = item.find("p", {"class": "view-prod-category"})
    # category = "category"
    # sub_category = category if category else "category"

    # print("sub category",sub_category)
    
 
    
    current_date: str = datetime.now().strftime('%d.%m.%Y')
    # print("current_date1",current_date)
    
    res = price_item_model(id, category if category else "", sub_category if sub_category else "", title, price, current_date)
    # print("res:",res)
    return res


def main(base_url):
    """
    Основная программа
    :param base_url:
    :return:
    """
    os.system('cls')

    razdel = get_catalogs(base_url + "/shop")
    # field names
    
    rows = []

    
    category = ""
    sub_category=""
    count=0
    print("Парсинг начат ...")
    for cat in razdel:
        # print(len(razdel))
        count =count + 1
        url = cat
        i = 1
        while True:
            response = ""
            # if pages < i:
            #     break
            if i > 1:
                try:
                    test_url = url + "page/" + str(i)
                   
                except:
                    break
            else:
                test_url=url
                
            print("Обрабатывается страница: ", test_url)
            response = requests.get(test_url)
            soup = bs(response.text, "html.parser")
          
            try:
                sub_category = soup.find("h1", {"class": "page-title"}).text
                # print("Категория:", category, " Cтраница:", i)
            except:
                print("Все просмотрели")
                break
                # print(response)

            try:
                items = soup.find_all("li", class_="type-product")
                print("количество", len(items))
                
                if(len(items)==0):
                    category=sub_category
                
                for item in items:
                    r= get_row(item,category,sub_category)
                    rows.append(r)

                if len(items) == 0:
                    break
                i = i + 1
            except:
                print("Ошибка поиска карточки")
                break

    # print(rows)
    save_to_csv("data_zvezda.csv", rows)


main(base_url="https://zvezda.md")
