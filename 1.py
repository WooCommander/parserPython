from bs4 import BeautifulSoup

def extract_info(html, tag=None, class_=None, attribute=None, attribute_value=None, index=None, get_text=True):
    soup = BeautifulSoup(html, 'html.parser')

    # Формирование критериев поиска
    search_criteria = {}
    if class_:
        search_criteria['class_'] = class_
    if attribute and attribute_value:
        search_criteria[attribute] = attribute_value

    # Поиск элементов
    if tag:
        elements = soup.find_all(tag, **search_criteria)
    else:
        elements = soup.find_all(**search_criteria)

    # Обработка результатов
    if not elements:
        return None

    if index is not None and index < len(elements):
        chosen_element = elements[index]
    else:
        chosen_element = elements[0]

    # Специальная обработка для цен топлива
    if class_ and class_.startswith('f-') and get_text:
        first_part = chosen_element.find('span', class_='first').get_text(strip=True) if chosen_element.find('span', class_='first') else ""
        last_part = chosen_element.find('span', class_='last').get_text(strip=True) if chosen_element.find('span', class_='last') else ""
        return f"{first_part},{last_part}" if first_part and last_part else "Цена не найдена"

    return chosen_element.get_text(strip=True) if get_text else chosen_element

# Пример использования для товара
html_code_product = """Ваш HTML код для товара здесь"""
print(extract_info(html_code_product, tag='span', class_='woocommerce-Price-amount amount'))

# Пример использования для топлива
html_code_fuel = """Ваш HTML код для топлива здесь"""
print(extract_info(html_code_fuel, class_='f-dte'))

