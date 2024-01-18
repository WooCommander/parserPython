import requests
from bs4 import BeautifulSoup

class WebElement:
    def __init__(
        self,
        tag_: str,
        class_: str,
        attr_: str,
        get_text_: bool = False,
        value_: bool = False,
        idx_: int = None,
        as_list_: bool = False,
        soup_: bs4
    ):
        self.tag = tag_
        self.class_ = class_
        self.get_text = get_text_
        self.attr = attr_
        self.as_list = as_list_
        self.idx = idx_
        self.value = value_
        self.soup= soup_


def get_page_element(params_list:list WebElement ):
    try:
        for params in params_list:
            # Ищем элемент в соответствии с переданными параметрами
            elements = params.soup.find_all(params.tag, class_=params.class_, attrs={params.atribute: params.attribute_value} if params.attribute else None)

            # Возвращаем результат в виде массива или одиночного значения
            if elements:
                if params.as_list or params.idx!=None:
                    if params.idx is not None and 0 <= params.idx < len(elements):
                        return [elements[params.idx].get_text(strip=True) if params.get_text else elements[params.idx].get(params.attribute, '')]
                    else:
                        return [element.get_text(strip=True) if params.get_text else element.get(params.attribute, '') for element in elements]
                elif params.idx is not None and 0 <= params.idx < len(elements):
                    return elements[params.idx].get_text(strip=True) if params.get_text else elements[params.idx].get(params.attribute, '')
                else:
                    return elements[0].get_text(strip=True) if params.get_text else elements[0].get(params.attribute, '')
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

inner_page_params1 = {
    'tag': 'span',
    'index':-2

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
    