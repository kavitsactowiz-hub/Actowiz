import json
import requests
from lxml import html

headers ={

   "content-type" : "text/html",
   "user-agent" :"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
}

data = requests.get("https://www.maggi.in/en/product/maggi-2-minute-special-masala-instant-noodles/",headers=headers)

finalObject = {}
if data.status_code == 200:
    root = html.fromstring(data.text)
    tablestart = root.xpath('//tbody/tr[@class="scroll-section__row"]')
    tableheading = root.xpath('//th[contains(@class,"heading")]/text()')
    
    for item in tablestart:
        tdlist = item.xpath('td[@class="table-cell"]/text()')
        d1={}
        keylist = tableheading
        i=0
        for eachtd in tdlist:
            if i == 0:
                 pass
            else:   
                if i < 3:
                        d1[keylist[i-1]] = float(eachtd.strip())
                else:
                        d1[keylist[i-1]] = eachtd.strip()
           
            i=i+1
        cname = tdlist[0].strip()
        if cname[0] == "-":
            cname = cname[1:]
       
        finalObject[cname] = d1
        
       # print(d1)
maggiefinalobject = {
    "Nutrition_information" : finalObject
}
with open("output.json","w",encoding="utf-8") as f:
    json.dump(maggiefinalobject,f)