import json
import requests
from lxml import html
from db import mydb

mycursor = mydb.cursor()

sql_query = """
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    link VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
"""
mycursor.execute(sql_query)
print("Table created successfully.")

baseurl = "https://books.toscrape.com/catalogue/"
data = requests.get("https://books.toscrape.com/")
if data.status_code == 200:
    root = html.fromstring(data.text)
    total_str = root.xpath('//ul[@class="pager"]/li[@class="current"]/text()')
    total = int(str(total_str[0]).strip().split("of")[1])

    FinalBooks=[]
    for i in range(1,total+1):
        newurl = baseurl + f"page-{i}.html"
        data = requests.get(newurl)
        
        if data.status_code == 200:
            root = html.fromstring(data.text)
            bookName = root.xpath('//div/ol/li/article[@class="product_pod"]/h3/a/@title')
            bookLink = root.xpath('//div/ol/li/article[@class="product_pod"]/h3/a/@href')

            for i in range(len(bookName)):
                newurl = baseurl + bookLink[i]
                FinalBooks.append((bookName[i],newurl))
                sql = "INSERT INTO books (name, link) VALUES (%s, %s)"
                val = (bookName[i],newurl)
                mycursor.execute(sql, val)
                mydb.commit() 


    mydb.close()
