import requests
from bs4 import BeautifulSoup

def get_page_element(tag=None, class_=None, attribute=None, attribute_value=None, get_text=True, as_list=False, index=None, url=None):
    try:
        # Получаем содержимое страницы
        response = requests.get(url)
        response.raise_for_status()

        # Создаем объект BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Ищем элемент в соответствии с переданными параметрами
        elements = soup.find_all(tag, class_=class_, attrs={attribute: attribute_value} if attribute else None)

        # Возвращаем результат в виде массива или одиночного значения
        if elements:
            if as_list:
                if index is not None and 0 <= index < len(elements):
                    return [elements[index].get_text(strip=True) if get_text else elements[index].get(attribute, '')]
                else:
                    return [element.get_text(strip=True) if get_text else element.get(attribute, '') for element in elements]
            elif index is not None and 0 <= index < len(elements):
                return elements[index].get_text(strip=True) if get_text else elements[index].get(attribute, '')
            else:
                return elements[0].get_text(strip=True) if get_text else elements[0].get(attribute, '')
        else:
            return "Элемент не найден."

    except Exception as e:
        return f"Произошла ошибка: {str(e)}"

# Пример использования
outer_params = {
    'tag': 'div',
    'class_': 'outer-container',
    'attribute': 'class',
    'attribute_value': 'outer-container',
    'url': 'https://example.com/outer-page'
}

inner_params = {
    'tag': 'a',
    'class_': 'inner-link',
    'attribute': 'href'
}

inner_page_params = {
    'tag': 'p',
    'class_': 'content',
    'attribute': 'class',
    'attribute_value': 'content'
}

# Получаем URL внутренней страницы из внешнего элемента
inner_page_url = get_page_element(**outer_params, **inner_params)

# Если внутренний URL найден, ищем элементы на внутренней странице
if inner_page_url:
    inner_page_params['url'] = inner_page_url
    result_inner = get_page_element(**inner_page_params, as_list=True)
    print(f"Текст элементов на внутренней странице: {result_inner}")
else:
    print("Внутренний URL не найден.")