import requests
from bs4 import BeautifulSoup as bs
import os
import csv
import datetime
from datetime import datetime


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

class parse_const():
    base_url="https://zvezda.md/shop"
    file="data_zvezda1.csv"
    id_element=""
    id=""
    name_element=""
    

def get_catalogs_url(url_base: str):
    """
    Получение массива с url каталогов
    :param url_base: главная страница где есть список каталогов
    :return: str[]
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
        print("количество каталогов:", len(catalogs))
        return catalogs
    except:
        print("Ошибка получения списка какталогов")

def get_html_soup(url):
    response = requests.get(url)
    soup = bs(response.text, "html.parser")
    return soup

def save_to_csv(file_name, data_arr):
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

def get_category(soup):

    category_element = soup.find("h1", {"class": "page-title"}).text
    category= category_element if  category_element else ""
    
    return category

def get_sub_category(soup):

    sub_category_element = soup.find("h1", {"class": "page-title"}).text
    sub_category=sub_category_element if sub_category_element else ""
    
    return sub_category

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


def get_items(soup, tag_, class_):
    """Получение массива товаров

    Args:
        soup (_type_): _description_
        tag_ (_type_): _description_
        class_ (_type_): _description_

    Returns:
        _type_: _description_
    """
    items=[]
    items = soup.find_all(tag_, class_=class_)
    print("количество:", len(items))
    return items


#----------------------------------------------------------------------------------------------------------------
def main(base_url):
    """
    Основная программа
    :param base_url:
    :return:
    """
    os.system('cls')
    catalogs = get_catalogs_url(base_url)
    rows = []
    
    print("Парсинг начат ...")

    for cat_url in catalogs:
      
        page_url = cat_url
        page = 1
        while True:
            
            print("Обрабатывается страница: ", page_url)
            if page > 1:
                try:
                    page_url = cat_url + "page/" + str(page)
                    soup = get_html_soup(page_url)   
                except:
                    break
            else:
                soup = get_html_soup(page_url)
                category =  get_category(soup)
                sub_category = get_sub_category(soup)
                  
            try:
                items = get_items(soup,tag_="li", class_="type-product")
                if len(items) == 0:
                    break
                                        
                for item in items:
                    row = get_row(item,category,sub_category)
                    rows.append(row)


                page +=1
            except:
                print("Ошибка поиска карточки")
                break

    # print(rows)
    save_to_csv("data_zvezda1.csv", rows)


main(base_url="https://zvezda.md/shop")
