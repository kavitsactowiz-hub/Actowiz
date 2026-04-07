import json
import math

FinalProducts = []
ProductLink = "https://www.bonkerscorner.com/products/"

with open("bonker.json","r",encoding="utf-8") as f:
    d1 = json.load(f)
    products = d1["products"]

    
    for i in range(len(d1["products"])):
        ProductName = products[i]["variants"][0]["name"].split("-")[0].strip()
        vendor = products[i]["vendor"]
        handel = products[i]["handle"]
        productUrl = ProductLink + handel
        productPrice = products[i]["variants"][0]["price"] / 100
        variantCount = len(products[i]["variants"])
        optionValues=[]
        variants = []
        for j in range(variantCount):
            optionValues.append(products[i]["variants"][j]["public_title"])
            temp={
                "variantName" : products[i]["variants"][j]["public_title"],
                "variantId" : products[i]["variants"][j]["id"],
                "variantUrl" : f"{ProductLink}{handel}?variant={products[i]['variants'][j]['id']}",
                "variantPrice" : products[i]["variants"][j]["price"] / 100,
            }
            variants.append(temp)

        variantOptions=[
            {
                "optionName" : "Size",
                "optionValues" : optionValues
            }
        ]

        p1 = {
            "ProductName" : ProductName,
            "vendor" : vendor,
            "productUrl" : productUrl,
            "productPrice" : productPrice,
            "variantCount" : variantCount, 
            "optionValues" : variantOptions,
            "variants" : variants
        }
        FinalProducts.append(p1)


with open("result.json","w",encoding="utf-8") as f:
    json.dump(FinalProducts,f)


