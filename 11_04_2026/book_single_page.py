import json
import requests
from lxml import html
from urllib.parse import urljoin

url = "https://books.toscrape.com/catalogue/security_925/index.html"
data = requests.get(url)

root = html.fromstring(data.text)

imageurl = root.xpath('//div[@class="carousel-inner"]/div[contains(@class,"item")]/img/@src')

finalimageurl = urljoin(url,imageurl[0])
title = root.xpath('//div[contains(@class,"product_main")]/h1/text()')[0]
price = float((root.xpath('//div[contains(@class,"product_main")]/p[@class="price_color"]/text()')[0])[2:])
instock_availability = int(root.xpath('//div[contains(@class,"product_main")]/p[@class="instock availability"]/text()')[1].strip().split("(")[1].split(" ")[0])
star_rating = int(len(root.xpath('//div[contains(@class,"product_main")]/p[@class="star-rating Two"]/i')))
product_description = root.xpath('//div[@id="product_description"]/following-sibling::p/text()')[0]

products_keys = root.xpath('//table[@class="table table-striped"]/tr/th/text()')
products_values = root.xpath('//table[@class="table table-striped"]/tr/td/text()')

products_information = {} 

for i in range(len(products_keys)):
    if "\u00c2\u00a3" in products_values[i]:
        products_information[products_keys[i]] = float(products_values[i][2:])
    else:
        products_information[products_keys[i]] = products_values[i]


finaloutput= {
    "name" : title,
    "image_url" : finalimageurl,
    "price" : price,
    "instock_availability" : instock_availability,
    "star_rating" : star_rating,
    "product_description" : product_description,
    "products_information" : products_information
}

with open("output.json","w",encoding="utf-8") as f:
    json.dump(finaloutput,f)

