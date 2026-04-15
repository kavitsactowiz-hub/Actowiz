import json
import requests
from lxml import html
from db import mydb
from urllib.parse import urljoin

mycursor = mydb.cursor()

sql_query = """
CREATE TABLE IF NOT EXISTS book_category (
    bookid INT AUTO_INCREMENT PRIMARY KEY,
    categoryid INT REFERENCES categories(id),
    categoryname VARCHAR(255),
    name VARCHAR(255),
    link VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
"""
mycursor.execute(sql_query)

query = "SELECT name, link from categories"
mycursor.execute(query)
categories = mycursor.fetchall()

baseurl = "https://books.toscrape.com/catalogue/"

FinalBooks=[]
def bookcategory(url,categoryname,category_id):
    data = requests.get(url)
    if data.status_code == 200:

        root = html.fromstring(data.text)
        bookName = root.xpath('//div/ol/li/article[@class="product_pod"]/h3/a/@title')
        bookLink = root.xpath('//div/ol/li/article[@class="product_pod"]/h3/a/@href')

        nexturl = root.xpath('//ul[@class="pager"]/li[@class="next"]/a/@href')

        for j in range(len(bookName)):
            newurl = urljoin(url,bookLink[j])
            FinalBooks.append((category_id,bookName[j],newurl))
            sql = """
            INSERT INTO book_category (categoryid, categoryname, name, link)
            VALUES (%s, %s, %s, %s)
            """
            val =(category_id,categoryname,bookName[j],newurl)
            mycursor.execute(sql,val)
            mydb.commit()

        if nexturl:
            tempurl = list(categories[i])[1].replace("index.html","")
            newnexturl = tempurl + nexturl[0]
            bookcategory(newnexturl,categoryname,category_id)


for i in range(0,len(categories)):
    url = list(categories[i])[1]
    category_id = i + 1
    categoryname = list(categories[i])[0]
    bookcategory(url,categoryname,category_id)
          
mydb.close()