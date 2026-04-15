import json
import requests
from lxml import html
from db import mydb

mycursor = mydb.cursor()

sql_query = """
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30),
    link VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
"""
mycursor.execute(sql_query)


url = "https://books.toscrape.com/"

headers= {
    "content-type" : "text/html",
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
}

data = requests.get(url,headers=headers)

if data.status_code == 200:
    #print(data.text)
    root = html.fromstring(data.text)

    categoryNames = root.xpath('//ul[contains(@class,"nav-list")]/li/ul/li/a/text()')
    categoryLinks = root.xpath('//ul[contains(@class,"nav-list")]/li/ul/li/a/@href')
    baseUrl = "https://books.toscrape.com/"
  
    FinalData = []
    for i in range(len(categoryNames)):
        temp = categoryNames[i].strip()
        newurl = baseUrl + categoryLinks[i]
        FinalData.append((temp , newurl))
   

print("Table created successfully.")

sql = "INSERT INTO categories (name, link) VALUES (%s, %s)"
val = FinalData

mycursor.executemany(sql, val)
mydb.commit() # Required to make changes permanent
print(mycursor.rowcount, "record inserted.")
mydb.close()