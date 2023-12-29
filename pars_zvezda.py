import requests
from bs4 import BeautifulSoup as bs
import os
import csv
import datetime
from datetime import datetime

# "Komplektujuschie","2873", "Kompjuternaja-mebel","bytovaya","ohrannye-sistemy","svet-i-jelektrika","uslugi","avtojelektronika","rashodnye-materialy","Подарочные сертификаты","Programmnoe-obespechenie"
# "Komplektujuschie", "2873", "Kompjuternaja-mebel", "bytovaya", "ohrannye-sistemy", "svet-i-jelektrika",          "uslugi", "avtojelektronika", "rashodnye-materialy",
razdel = ["kamen-4082", "novogodnij-dekor-4092", "suxie-stroitelnye-smesi-i-gidroizolyaciya-2263",
          "teploizolyaciya-i-shumoizolyaciya-3919"]


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


def get_row(item):
    """
    Получение строки данных из html карточки товара
    :param item:
    :return: price_item
    """
    id_element = item.find("div", {"class": "quick-view"})
    title_element = (item.find("p", {"class": "view-prod-name"}))
    price_element = item.find("span", {"class": "woocommerce-Price-amount"})
    sub_category_element = item.find("p", {"class": "view-prod-category"})
    sub_category = sub_category_element.text if sub_category_element else "none"
    id: str = id_element.get('data-prod') if id_element else " non"
    title: str = title_element.get_text(separator=' ', strip=True) if title_element else "no title"
    price: str = price_element.text if price_element else "0"
    current_date: str = datetime.datetime.now().strftime('%d.%m.%Y')
    return price_item(id, "category", sub_category, title, price, current_date)


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

    pages = 2
    category = ""
    current_date =  datetime.now()
    print("Парсинг начат ...")
    for cat in razdel:
        url = cat
        i = 1
        while True:
            response = ""
            # if pages < i:
            #     break
            if i > 1:
                try:
                    test_url = url + "?page/" + str(i)

                    
                except:
                    break
            else:
                test_url=url
                
            print("Обрабатывается страница: ", test_url)
            response = requests.get(test_url)
            soup = bs(response.text, "html.parser")
          

            try:
                category = soup.find("h1", {"class": "page-title"}).text
                print("Категория:", category, " Cтраница:", i)
            except:
                print("Все просмотрели")
                break
                # print(response)

            try:
                items = soup.find_all("li", {"class": "product-small"})
                print(items)
                for item in items:
                    rows.append(get_row(item))

                if len(items) == 0:
                    break
                i = i + 1
            except:
                print("Ошибка поиска карточки")
                break

    save_to_csv("data_zvezda.csv", rows)


main(base_url="https://zvezda.md")
