import requests
from bs4 import BeautifulSoup as bs
import os
import csv

razdel = ["televizory-i-elektronika","bytovaya-tehnika", "kompyuternaya-tehnika","mebel-tekstil","odezhda-i-aksessuary","tovary-dlya-doma","instrumenty-i-oborudovanie","sport-i-otdyh" ]
# Python3 code here creating class
class price_item:
    def __init__(self, id, category, name, price):
        self.id = id
        self.category=category
        self.name = name
        self.price = price
       
os.system('cls')
base_url= "https://hi-tech.md/"
# ['https://hi-tech.md/kompyuternaya-tehnika/page-2/']

# field names 
fields = ['#', 'Name', 'Price'] 
rows=[]


# try:
#     response = requests.get(base_url)
#     soup_base = bs(response.text,"html.parser")
#     category= soup.find("h1").find("span").text
    
# except:
#     print("Ошибка получения главной страницы:"+ base_url)
#            # перебор подкатегорий
            # ty-subcategories__item
            # sub_categorys= soup.find_all("li", {"class": "ty-subcategories__item"})
            # for sub_category in  sub_categorys:
            #     sub_link = sub_category.find("a").get("href")
            #     sub_title=sub_category.find("span").text
            #     print(sub_title, sub_link )
#

for cat in razdel:
    url = base_url+cat+"/"
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
            soup = bs(response.text,"html.parser")


        # print(response)

        soup = bs(response.text,"html.parser")
        category=""
        try:
            category= soup.find("h1").find("span").text
            print(category)
        except: 
            print("Все просмотрели")
            break   
        try:
                       
            for item in soup.find_all("div", {"class": "col-tile"}):
                id = item.find("span",{"class":"ty-control-group__item"}).text
                title= (item.find("a",{"class": "product-title"})).get('title')
                price= item.find("span",{"class": "ty-price-num"}).text

                # print (id,title, price)
                rows.append(price_item(id,category,title, price))
        except:
            i = i+1
    # print(rows)

with open('data.csv', 'w',) as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(fields)
    for el in rows:
        writer.writerow([el.id,el.category, el.name, el.price])