from bs4 import BeautifulSoup
import requests

class WebElement:
    def __init__(
        self,
        tag: str,
        class_: str,
        attribute: str = None,
        attribute_value: str = None,
        get_text: bool = False,
        idx: int = None,
        as_list: bool = False,
        soup: BeautifulSoup = None
    ):
        self.tag = tag
        self.class_ = class_
        self.get_text = get_text
        self.attribute = attribute
        self.attribute_value = attribute_value
        self.idx = idx
        self.as_list = as_list
        self.soup = soup

def get_page_element(elements: list[WebElement]):
    results = []
    for element in elements:
        found_elements = element.soup.find_all(element.tag, class_=element.class_, attrs={element.attribute: element.attribute_value} if element.attribute else None)

        if not found_elements:
            results.append("Элемент не найден.")
            continue

        if element.idx is not None and 0 <= element.idx < len(found_elements):
            target_elements = [found_elements[element.idx]]
        else:
            target_elements = found_elements

        for item in target_elements:
            result = item.get_text(strip=True) if element.get_text else item.get(element.attribute, '')
            results.append(result)

    return results if element.as_list else results[0] if results else None

# Пример использования
response = requests.get('https://example.com/outer-page')
soup = BeautifulSoup(response.content, 'html.parser')

outer_element = WebElement(
    tag='div',
    class_='outer-container',
    get_text=True,
    soup=soup
)

inner_element = WebElement(
    tag='a',
    class_='inner-link',
    attribute='href',
    get_text=True,
    soup=soup
)

result = get_page_element([outer_element, inner_element])
print(f"Результаты: {result}")
