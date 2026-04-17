import json
import requests
import jmespath
from lxml import html


with open("output.json","r",encoding="utf-8") as f:
    data = json.load(f)


root = jmespath.search('props.pageProps',data)
images_main = jmespath.search('akeneoProductData.assets',root)

imagekeylist = ["drawing_01","product_teaser_image"]
imageObject={}
i=0

urlstartpart="https://"
for asset in images_main:
    if asset.get("key") in imagekeylist:
        imageObject[imagekeylist[i]] = urlstartpart + str(jmespath.search('sources[0].uri',asset)).lstrip('/')
        i=i+1

part_number = root.get("articleNumber").strip()
Material= jmespath.search("articleData.material.name",root).strip()

Shape = jmespath.search('_nextI18Next.userConfig.resources.en."bearing-hub/bearingHub".SHAPES.S.TITLE',root)
Dimensions = jmespath.search("articleData.dimensions",root)
DimensionsObject = {}
for k,v in Dimensions.items():
    DimensionsObject[k] = f"{v} mm"

manufacturing_method = jmespath.search('_nextI18Next.userConfig.resources.en."bearing-hub/bearingHub".PRODUCTION_METHODS.MOLD_INJECTION',root)

material_properties_str_list = html.fromstring(str(jmespath.search("akeneoProductData.attributes.attr_USP.value",root)).strip())
material_properties = material_properties_str_list.xpath("//li/text()")

total_price = round(float(jmespath.search("articleData.totalPrice.value",root)),2)

product_description = html.fromstring(jmespath.search("akeneoProductData.attributes.attr_description.value",root))
product_description = " ".join(product_description.xpath(".//text()"))

technicalDataCategories = jmespath.search("technicalDataCategories",root)

technicalDataCategorieslist={}
for item in technicalDataCategories:
   atributeobject={}
   for attribute in item.get("attributes"):
       key=attribute.get("description").strip()
       value=attribute.get("value") 
       atributeobject[key] = value
    
   technicalDataCategorieslist[item.get("name")] = atributeobject
    

finalObject = {
    "images": imageObject,
    "part_number": part_number,
    "material" : Material,
    "shape" : Shape,
    "dimensions" : DimensionsObject,
    "properites" : material_properties,
    "total_price" : total_price, 
    "product_description" : product_description,
    "technical_data" : technicalDataCategorieslist
}   

with open("finaloutput.json","w",encoding="utf-8") as f:
    json.dump(finalObject,f)
