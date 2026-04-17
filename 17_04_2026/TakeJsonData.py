import json
import requests
from lxml import html

headers = {
    "content-type":"text/html; charset=utf-8",
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
}

data = requests.get("https://www.igus.in/iglidur-ibh/sleeve-bearings/product-details/iglidur-glw-m?artnr=GLWSM-1012-10",headers=headers)

if data.status_code == 200:
   root = html.fromstring(data.text)
   scripts = root.xpath('string(//script[@id="__NEXT_DATA__"]/text())')
   result = json.loads(scripts)

   with open("output.json","w",encoding="utf-8") as f:
        json.dump(result,f)