import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import os
import numpy
import csv


import numpy as np
# URL_TEMPLATE = "https://www.work.ua/ru/jobs-odesa/?page=2"
# FILE_NAME = "test.csv"


# def parse(url = URL_TEMPLATE):
#     result_list = {'href': [], 'title': [], 'about': []}
#     r = requests.get(url)
#     soup = bs(r.text, "html.parser")
#     vacancies_names = soup.find_all('h2', class_='add-bottom-sm')
#     vacancies_info = soup.find_all('p', class_='overflow')
#     for name in vacancies_names:
#         result_list['href'].append('https://www.work.ua'+name.a['href'])
#         result_list['title'].append(name.a['title'])
#     for info in vacancies_info:
#         result_list['about'].append(info.text)
#     return result_list

# data=parse()
# df = pd.DataFrame(data)
# df.to_csv(FILE_NAME)


# Python3 code here creating class
class price_item:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price
        
        
os.system('cls')
url = 'https://hi-tech.md/kompyuternaya-tehnika/'
# ['https://hi-tech.md/kompyuternaya-tehnika/page-2/']

# field names 
fields = ['#', 'Name', 'Price'] 
rows=[]

i=1
while 4>i:
    response=""
    if i>1:
        try:
            response = requests.get(url+"page-"+str(i))
        except:
            break    
    else:
        response = requests.get(url)
    
    # print(response)

    soup = bs(response.text,"html.parser")
    print(soup.find("h1").find("span").text)

    try:
        
        for item in soup.find_all("div", {"class": "col-tile"}):
            id = item.find("span",{"class":"ty-control-group__item"}).text
            title= (item.find("a",{"class": "product-title"})).get('title')
            price= item.find("span",{"class": "ty-price-num"}).text

            # print (id,title, price)
            rows.append(price_item(id,title, price))
    except:
        i = i+1
# print(rows)

with open('data.csv', 'w',) as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(fields)
    for el in rows:
        writer.writerow([el.id,el.name, el.price])