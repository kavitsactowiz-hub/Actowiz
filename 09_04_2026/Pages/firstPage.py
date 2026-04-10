import json
import jmespath

data = ""
with open("air_bnb.json","r",encoding="utf-8") as f:
    data = json.load(f)

with open("air_bnb2.json","r",encoding="utf-8") as f2:
    data2 = json.load(f2)


StartPart = jmespath.search("niobeClientData[0][1].data.presentation.stayProductDetailPage.sections",data)
hotelName = jmespath.search("sections[21].section.listingTitle",StartPart).split("|")[2].strip() 
niobeClientData = jmespath.search("sbuiData.sectionConfiguration.root",StartPart)
FirstPart = jmespath.search("sections[0].sectionData",niobeClientData)
SecondPart = jmespath.search("sections[1].sectionData",niobeClientData)
ThirdPart = jmespath.search("sections[17].section",StartPart)

title = FirstPart.get("title")
capacityStrList = jmespath.search("overviewItems[*].title",FirstPart)
capacityList = {}
for i in capacityStrList:
    d = i.split(" ")
    capacityList[f"{d[1]}"]=int(d[0])
  
rating = float(jmespath.search("reviewData.ratingText",FirstPart))
review = int(jmespath.search("reviewData.reviewCountText",FirstPart).split(" ")[0])

profile_name = SecondPart.get("title")
profile_year = jmespath.search("overviewItems[0].title",SecondPart)
profile_url = jmespath.search("hostAvatar.avatarImage.baseUrl",SecondPart)

profile = {
    "profile_name" : profile_name,
    "year_of_expreience" : profile_year,
    "profile_url" : profile_url
}

highlights = jmespath.search("highlights[].{ title: title, subtitle: subtitle}",ThirdPart)

description = jmespath.search("sections[18].section.htmlDescription.htmlText",StartPart).split("<br /><br />")
description = f"{description[0]}\n\n{description[1]}"

firstPart_bnb2 = jmespath.search("data.presentation.stayProductDetailPage.sections.sections[1].section.structuredDisplayPrice.primaryLine",data2)
paymentDetails = {"currency":'INR',"discounted_price":int(firstPart_bnb2.get("discountedPrice")[1:].replace(',', '')),"original_price":int(firstPart_bnb2.get("originalPrice")[1:].replace(',', '')),"price_type":firstPart_bnb2.get("qualifier")}

FinalOutput = {
    "restaurant_name" : hotelName,

    "details":{
        "title" : title,
        "capacity" : capacityList,
        "rating" : rating,
        "review" : review,
        "profile" : profile,
        "highlights" : highlights,
        "description": description
    },
    "paymentDetails" : paymentDetails

}
