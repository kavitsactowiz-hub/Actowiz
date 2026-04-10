import json
import jmespath
from Pages.firstPage import FinalOutput
from Pages.secondPage import seeAllAmenitiesGroups
from Pages.thirdPage import FinalReviews
from Pages.FourthPage import ProfileDetails

FinalOutput["amenities"] = seeAllAmenitiesGroups
FinalOutput["reviews"] = FinalReviews
FinalOutput["ProfileDetails"] = ProfileDetails

with open("output.json","w",encoding="utf-8") as f:
     json.dump(FinalOutput,f)
