import json
import jmespath
from validation import ZomatoDataValidation

with open("Zomato.json","r",encoding="utf-8") as f:
    data = json.load(f)

sections = data.get('page_data').get('sections')
SECTION_BASIC_INFO = sections.get('SECTION_BASIC_INFO')
SECTION_RES_CONTACT = sections.get('SECTION_RES_CONTACT')
SECTION_RES_HEADER_DETAILS = sections.get('SECTION_RES_HEADER_DETAILS')
menus = data.get('page_data').get('order').get('menuList').get('menus')


restaurant_id  = SECTION_BASIC_INFO.get('res_id')
restaurant_name = SECTION_BASIC_INFO.get('name')
restaurant_url = data.get("page_info").get("canonicalUrl")
restaurant_contact = SECTION_RES_CONTACT.get('phoneDetails').get('phoneStr')
fssai_licence_number = ""
full_address =  SECTION_RES_CONTACT.get('address')
region = SECTION_RES_CONTACT.get('country_name')
city =  SECTION_RES_CONTACT.get('city_name')
pincode =  SECTION_RES_CONTACT.get('zipcode')
state = ""
cuisines = []

for item in SECTION_RES_HEADER_DETAILS.get('CUISINES'):
    temp = {
        'name':item.get('name'),
        'url': item.get('url')
    }
    cuisines.append(temp)

fulltimes = SECTION_BASIC_INFO.get('timing').get('customised_timings').get('opening_hours')[0].get('timing')
fulltimes = fulltimes.split("–")
op = fulltimes[0]
cl = fulltimes[1]

timings={
    "monday":{
        'open': op,
        'close': cl
    },
    "tuesday":{
        'open': op,
        'close': cl
    },
    "wednesday":{
        'open': op,
        'close': cl
    },
    "thursday":{
        'open': op,
        'close': cl
    },
    "friday":{
        'open': op,
        'close': cl
    },
    "saturday":{
        'open': op,
        'close': cl
    },
    "sunday":{
        'open': op,
        'close': cl
    }
}

menu_categories=[]
for item in menus:
    categories = item.get('menu').get('categories')  
    items = []
    for category in categories:
        for subitem in category.get('category').get('items'):
            nesteditem=subitem.get('item')
            temp={
                    "item_id": nesteditem.get('id'),
                    "item_name": nesteditem.get('name'),
                    "item_slugs": nesteditem.get('tag_slugs'),
                    "item_url": '',
                    "item_description": nesteditem.get('desc'),
                    "item_price": '',
                    "is_veg": True if nesteditem.get('dietary_slugs')[0] == "veg" else False 
             }
            items.append(temp)
    

    categories={
        "category_name": item.get('menu').get('name'),
        "items":items
    }
    menu_categories.append(categories)

#print(menu_categories)

ZomatoData = {
    "restaurant_id":restaurant_id,
    "restaurant_name":restaurant_name,
    "restaurant_url":restaurant_url,
    "restaurant_contact":restaurant_contact,
    "fssai_licence_number":fssai_licence_number,
    "address_info":{
        "full_address":full_address,
        "region":region,
        "city":city,
        "pincode":pincode,
        "state":state
    },
    "cuisines":cuisines,
    "timings":timings,
    "menu_categories":menu_categories
}

try:
    validate = ZomatoDataValidation(**ZomatoData)
    print("Validate Successfully")
    with open("finaldata.json","w",encoding="utf-8") as f:
        data = json.dump(ZomatoData,f)
except Exception as e:
    print(f"Error : {e}")
    

