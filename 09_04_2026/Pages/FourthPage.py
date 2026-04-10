import json
import jmespath

data = ""
with open("air_bnb.json","r",encoding="utf-8") as f:
    data = json.load(f)

StartPart = jmespath.search("niobeClientData[0][1].data.presentation.stayProductDetailPage.sections.sections[5].section",data)

ProfileView = jmespath.search("cardData.{ host_name : name , details : stats[].{counting : value, detail: label} }",StartPart)
