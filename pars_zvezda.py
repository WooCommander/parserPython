import requests
from bs4 import BeautifulSoup as bs
import os
import csv
import datetime
from datetime import datetime
from array import array


class price_item_model:
    """модель записи таблицы"""

    def __init__(
        self,
        id_item: str,
        category: str,
        sub_category: str,
        name: str,
        price: str,
        current_date: str,
    ):
        self.id = id_item
        self.category = category
        self.sub_category = sub_category
        self.name = name
        self.price = price
        self.current_date = current_date


class WebElement:
    def __init__(
        self,
        tag: str = None,
        class_: str = None,
        attr: str = None,
        attr_value: str = None,
        get_text: bool = False,
        idx: int = None,
        as_list: bool = False,
        soup: bs = None,
    ):
        self.tag = tag
        self.class_ = class_
        self.get_text = get_text
        self.attribute = attr
        self.attribute_value = attr_value
        self.idx = idx
        self.as_list = as_list
        self.soup = soup


class WebElements:
    def __init__(self, elements_: [WebElement]):
        self.elements_ = elements_


class parse_const:
    def __init__(
        self,
        soup: bs = None,
        base_url: str = None,
        file: str = None,
        category_url: [WebElement] = None,
        items_html: [WebElement] = None,
        category: [WebElement] = None,
        sub_category: [WebElement] = None,
        id: [WebElement] = None,
        title: [WebElement] = None,
        price: [WebElement] = None,
    ):
        self.base_url = base_url
        self.file = file
        self.categories_url = category_url
        self.items_html = items_html
        self.category = category
        self.sub_category = sub_category
        self.id = id
        self.title = title
        self.price = price
        self.soup = soup

        self.base_url = "https://zvezda.md/shop"
        self.file = "data_zvezda1.csv"
        self.categories_url = [
            WebElement(tag="li", class_="cat-item", soup=soup),
            WebElement(tag="a", attr="href", attr_value=True),
        ]
        self.items_html = [
            WebElement(tag="li", class_="type-product", as_list=True, soup=soup)
        ]
        self.category = [
            WebElement(tag="p", class_="aux-breadcrumbs", soup=soup),
            WebElement(tag="a", idx=-1, get_text=True),
        ]
        self.sub_category = [
            WebElement(tag="h1", class_="page-title", get_text=True, soup=soup)
        ]
        self.id = [
            WebElement(
                tag="a", class_="add_to_cart_button", attr="data-product_id", soup=soup
            )
        ]
        self.title = [
            WebElement(
                tag="h1",
                class_="woocommerce-products-header__title page-title",
                get_text=True,
                soup=soup,
            )
        ]
        self.price = [WebElement(tag="bdi", soup=soup)]


def get_page_element(elements: list[WebElement], soup:bs=None):
    results = []
    # количество входных последовательных наборов
       
    
    # обработка  массива наборов
    for element in elements:
        if len(results) == 0:
            if soup!=None:
                results = [soup]
            else:
                results = [element.soup]
            # print("results",len(results))
        new_results=[]
        len_results = len(results)
        for result in results:
            # print("result",result)
            if result!=None:
                new_result=result.find_all(
                element.tag,
                class_=element.class_,
                attrs={element.attribute: element.attribute_value}
                # WebElement(tag="li", class_="cat-item", soup=soup),
                # WebElement(tag="a", attr="href"),
        
                if element.attribute
                else None)
                # print("new_result",len(new_result))
                if len_results==1:
                    if len(new_result)==1:
                        if element.attribute_value:
                            new_result= new_result[0].get(element.attribute, '')
                        else:
                            new_result=new_result[0].get_text(strip=True)
                        new_results =new_result
                        
                        
                    if len(new_result)>1:
                        if element.idx!=None and len(new_result)>=element.idx:
                            new_results=new_result[element.idx]
                        else:
                            new_results=new_result
                else:
                    if element.attribute_value:
                        new_results.append(new_result[0].get(element.attribute, ''))
                    else:
                        new_results.append(new_result[0].get_text(strip=True))
        
        results=new_results
        
            
            
                
        # for soup in soups:
        #     # всегда ищем массив элементов
        #     found_elements = soup.find_all(
        #         element.tag,
        #         class_=element.class_,
        #         attrs={element.attribute: element.attribute_value}
        #         if element.attribute
        #         else None,
        #     )
        #     print("found_elements",found_elements)

        #     # если ничего не нашли и больше наборов нет, то завершаем перебор
        #     if not found_elements:
        #         results.append("Элемент не найден.")
        #         return

        #     # если нашли и нужен элемент под номером
        #     if element.idx is not None and 0 <= element.idx < len(found_elements):
        #         target_elements = found_elements[element.idx]
        #         # print("target_elements",target_elements)
        #         if len_el > 1:
        #             soup = target_elements
        #             continue
        #         break
        #     else:
        #         target_elements = found_elements
        #         print('target_elements',len(target_elements))
        #         if len_el == 1:
        #             return target_elements
                
        #         soup = target_elements
        #         # if soup_len==1:
        #         #     return 
        #         # break
        #         # for item in target_elements:
        #         #     result = item.get_text(strip=True) if element.get_text else item.get(element.attribute, '')
        #         #     results.append(result)
    return results
    return results if element.as_list else results[0] if results else None


def get_catalogs_url(url_base: str) -> array:
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


def get_html_soup(url) -> bs:
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
    fields = ["#", "catalog", "sub category", "Name", "Price", "date"]
    print("Парсинг завершен.")
    print("Начато сохранение")
    with open(file_name, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fields)
        for el in data_arr:
            writer.writerow(
                [
                    el.id,
                    el.category,
                    el.sub_category,
                    el.name,
                    el.price,
                    el.current_date,
                ]
            )
    print("Сохранение завершено, спасибо за работу.")


def get_category(soup: bs) -> str:
    category_element = (
        soup.find("p", {"class": "aux-breadcrumbs"}).find_all("a")[-1].text
    )
    category = category_element if category_element else ""
    return category


def get_sub_category(soup: bs) -> str:
    sub_category_element = soup.find("h1", {"class": "page-title"}).text
    sub_category = sub_category_element if sub_category_element else ""

    return sub_category


def get_row(item, category, sub_category) -> price_item_model:
    """
    Получение строки данных из html карточки товара
    :param item:
    :return: price_item
    """
    id_element = item.find("a", class_="add_to_cart_button")
    id = id_element["data-product_id"] if id_element else " non"
    # print("id:", id)

    title_element = item.find("h2", class_="woocommerce-loop-product__title")
    title: str = title_element.text if title_element else "no title"
    # print("title", title)

    price_element = item.find("bdi")
    price: str = price_element.text.replace("р.", "") if price_element else "0"
    # print("price:",price)

    current_date: str = datetime.now().strftime("%d.%m.%Y")

    res = price_item_model(
        id,
        category if category else "",
        sub_category if sub_category else "",
        title,
        price,
        current_date,
    )
    # print("res:",res)
    return res


def get_items(soup: bs, tag_: str, class_: str):
    """Получение массива товаров
    Returns:
        _type_: _description_
    """
    items = []
    items = soup.find_all(tag_, class_=class_)
    print("количество:", len(items))
    return items


# ----------------------------------------------------------------------------------------------------------------
def main(base_url: str):
    """
    Основная программа
    :param base_url:
    """
    os.system("cls")
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
                category = get_category(soup)
                sub_category = get_sub_category(soup)

            try:
                items = get_items(soup, tag_="li", class_="type-product")
                if len(items) == 0:
                    break

                for item in items:
                    row = get_row(item, category, sub_category)
                    rows.append(row)
                page += 1
            except:
                print("Ошибка поиска карточки")
                break

    # print(rows)
    save_to_csv("data_zvezda2.csv", rows)


# main(base_url="https://zvezda.md/shop")


# Пример использования
response = requests.get(
    "https://zvezda.md/product-category/baguettes-and-ceiling-tiles/%d0%bf%d0%be%d1%82%d0%be%d0%bb%d0%be%d1%87%d0%bd%d1%8b%d0%b5-%d0%b1%d0%b0%d0%b3%d0%b5%d1%82%d1%8b/"
)
soup = bs(response.content, "html.parser")

name = WebElement(
    tag="h2", class_="woocommerce-loop-product__title", get_text=True, soup=soup
)

price = WebElement(tag="bdi", get_text=True, soup=soup)
items = WebElement(tag="li", class_="type-product", as_list=True, soup=soup)
item = WebElement(tag="li", class_="type-product", as_list=True, idx=4, soup=soup)

x = parse_const(soup=soup)


# result = get_page_element([item])
# category = get_page_element(x.title)
# name = get_page_element([ name ],result[0])
# price = get_page_element([ price ],result[0])
# print(f"Результаты: {category}----{name}:{price}")




# result = get_page_element([item, name ])

# result = get_page_element([item, name ])
# print(f"Результаты: {result}")

# result = get_page_element([item, price ])
# print(f"Результаты: {result}")


# print("target_elements",x.categories_url)
# result = get_page_element(x.categories_url)

# result = get_page_element(x.items_html)
result = get_page_element(x.category)


# result = get_page_element(x.title)


print(f"Результаты: {result}")


