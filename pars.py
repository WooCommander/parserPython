import requests
from bs4 import BeautifulSoup as bs
import os
import csv


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
while True:
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
    try:
        print(soup.find("h1").find("span").text)
    except: 
        break   
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