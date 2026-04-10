import json
import jmespath

data = ""
with open("airbnb_review.json","r",encoding="utf-8") as f:
    data = json.load(f)

StartPart = jmespath.search("data.presentation.stayProductDetailPage.reviews",data)

reviewsNames = jmespath.search("reviews[].reviewer.firstName",StartPart)
reviewsDates = jmespath.search("reviews[].localizedDate",StartPart)
reviewsRating = jmespath.search("reviews[].rating",StartPart)
reviewsComments = jmespath.search("reviews[].commentV2",StartPart)

FinalReviews = []

for i in range(len(reviewsNames)) :
    temp = {
        "name" : reviewsNames[i],
        "rating" : reviewsRating[i],
        "date" : reviewsDates[i],
        "Comments" :reviewsComments[i]
    } 
    FinalReviews.append(temp)
