import json
import jmespath

data = ""
with open("air_bnb.json","r",encoding="utf-8") as f:
    data = json.load(f)

StartPart = jmespath.search("niobeClientData[0][1].data.presentation.stayProductDetailPage.sections.sections[5].section",data)

title = jmespath.search("cardData.name",StartPart)
counting = jmespath.search("cardData.stats[].value",StartPart)
review = jmespath.search("cardData.stats[].label",StartPart)
ProfileReview={}
for i in range(len(counting)):
    if '.' in counting[i]:
        ProfileReview[f"{review[i]}"] = float(counting[i])
    else:
        ProfileReview[f"{review[i]}"] = int(counting[i])

ProfileDetails = {
    "name" : title,
    "details" : ProfileReview
}
