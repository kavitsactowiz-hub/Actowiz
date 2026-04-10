import json
import jmespath
from Pages.firstPage import FirstImageData
from Pages.secondPage import SecondPageData
from Pages.thirdPage import FinalReviews
from Pages.FourthPage import ProfileView

FinalData = {
   "FirstImageData" : FirstImageData,
   "SecondImageData" : SecondPageData,
   "ThirdImageData" : FinalReviews,
   "FourthImageData" : ProfileView
}

with open("output.json","w",encoding="utf-8") as f:
     json.dump(FinalData,f)
