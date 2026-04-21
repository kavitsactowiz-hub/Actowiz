import json
import requests
from lxml import html
from requestToPage import getPageData, extractJsonData
import jmespath
from db import mydb

cursor = mydb.cursor()

BaseUrl = "https://www.rottentomatoes.com/browse/movies_in_theaters/sort:newest"

finalLinkList=[]
def getPageLink(url,i=0):
    pageData = getPageData(url)
    if pageData:
        jsonExtractData = extractJsonData(pageData)
        if i == 0:
            root = html.fromstring(pageData)
            pageinfodata = root.xpath('string(//script[@id="pageInfo"]/text())')
            pageinfo = json.loads(pageinfodata)
    
            jsonExtract = json.loads(jsonExtractData)
            for link in jsonExtract.get("itemListElement").get("itemListElement"):
                  temp = {
                        "name" : link.get("name"),
                        "url" : link.get("url")
                  }
                  finalLinkList.append(temp)
        else:
            extracteddata = json.loads(pageData)
            for link in extracteddata.get("grid").get("list"):
                  mainurl = "https://www.rottentomatoes.com"
                  temp = {
                        "name" : link.get("title"),
                        "url" : mainurl + link.get("mediaUrl")
                  }
                  finalLinkList.append(temp)
            pageinfo = extracteddata.get("pageInfo")

        
        if pageinfo:
              value = pageinfo.get("endCursor")
              newurl = f"https://www.rottentomatoes.com/cnapi/browse/movies_in_theaters/sort:newest?after={value}"
            #   print(newurl)
              i=i+1
              getPageLink(newurl,i)
       


# print(len(finalLinkList))
# with open("fulllinks.json","w",encoding="utf-8") as f:
#              json.dump(finalLinkList,f)

with open("fulllinks.json","r",encoding="utf-8") as f:
     finalLinkList = json.load(f)

finalObject=[]

i=0
for link in finalLinkList:
     fullpagedata = getPageData(link.get("url"))
     if fullpagedata:
          root = html.fromstring(fullpagedata)
          movieName = root.xpath('string(//media-hero/rt-text[@slot="title"]/text())')
          posterimage = root.xpath('string(//div[contains(@class,"media-scorecard")]//rt-img[contains(@alt,"poster")]/@src)')
          tomatometer = root.xpath('string(//div[contains(@class,"media-scorecard")]//rt-text[@slot="critics-score"]/text())')
          reviews = (root.xpath('string(//rt-link[@slot="critics-reviews"]/text())')).strip()
          description = (root.xpath('string(//drawer-more/rt-text[@slot="content"]/text())')).strip()
          whatToknow = root.xpath('//section[@aria-labelledby="what-to-know-label"]')
          whatToknowObj={}
          if whatToknow:
               whatToknowTitle = (root.xpath('string(.//div[@id="critics-consensus"]/rt-text/text())')).strip()
               whatToknowDescription = (root.xpath('string(.//div[@id="critics-consensus"]/p//text())')).strip()
               whatToknowObj["title"] = whatToknowTitle
               whatToknowObj["description"] = whatToknowDescription

          movie_query = """
               INSERT INTO movies 
               (movie_name, poster_image, tomatometer, reviews_summary, description,
                    what_to_know_title, what_to_know_desc)
               VALUES (%s, %s, %s, %s, %s, %s, %s)
               """
          movie_values = (
               movieName,
               posterimage,
               tomatometer,
               reviews,
               description,
               whatToknowObj.get("title"),
               whatToknowObj.get("description")
           )
          
          cursor.execute(movie_query, movie_values)
          movie_id = cursor.lastrowid

          castandCrewlink = root.xpath('string(//section[@aria-labelledby="cast-and-crew-label"]//rt-button[@data-qa="view-all-link"]/@href)')
          castnewlink = "https://www.rottentomatoes.com" + castandCrewlink
          castandcrewpagedata = getPageData(castnewlink)
          castandcrewroot = html.fromstring(castandcrewpagedata)
          castcrewmainpath = castandcrewroot.xpath('//div[@data-castandcrewmanager="mediaContainer"]/cast-and-crew-card')
          castandCrewlist=[]
          for castandcrewitem in castcrewmainpath:
              casttempdata = {
                "castimage" : castandcrewitem.xpath('string(.//rt-img[@slot="poster"]/@src)'),
                "casttitle" : castandcrewitem.xpath('string(.//rt-text[@slot="title"]/text())'),
                "castcharacters" : castandcrewitem.xpath('string(.//rt-text[@slot="characters"]/text())'),
                "castcredits" : castandcrewitem.xpath('string(.//rt-text[@slot="credits"]/text())')
              }
              cursor.execute("""
               INSERT INTO cast_and_crew
               (movie_id, castimage, casttitle, castcharacters, castcredits)
               VALUES (%s, %s, %s, %s, %s)
               """, (
                    movie_id,
                    casttempdata.get("castimage"),
                    casttempdata.get("casttitle"),
                    casttempdata.get("castcharacters"),
                    casttempdata.get("castcredits")
               ))
              #castandCrewlist.append(casttempdata)
              
          

          videoslink = root.xpath('string(//rt-button[@data-qa="videos-view-all-link"]/@href)')
          videonewlink = "https://www.rottentomatoes.com" + videoslink
          videopagedata = getPageData(videonewlink)
          videoroot = html.fromstring(videopagedata)
          videomainpath = videoroot.xpath('//div[contains(@class,"video-item")]')
          videolist=[]
          for videoitem in videomainpath:
               video_link = videoitem.xpath('string(.//a[@class="titlethumbnail"]/@href)')
               new_video_link = "https://www.rottentomatoes.com" + video_link
               videotempdata = {
                    "thumbnail_title":(videoitem.xpath('string(.//a[@class="titlethumbnail"]/text())')).strip(),
                    "thumbnail_url":videoitem.xpath('string(.//img[@class="thumbnail"]/@srcset)'),
                    "video_link":new_video_link
               }
               cursor.execute("""
               INSERT INTO videos
               (movie_id, thumbnail_title, thumbnail_url, video_link)
               VALUES (%s, %s, %s, %s)
               """, (
                    movie_id,
                    videotempdata.get("thumbnail_title"),
                    videotempdata.get("thumbnail_url"),
                    videotempdata.get("video_link")
               ))
               # videolist.append(videotempdata)
        
        
           
          reviewList=[]
          reviewsdata = root.xpath('string(//section[@aria-labelledby="critics-reviews-label"]//rt-button[@data-qa="view-all-link"]/@href)')
          if reviewsdata:
               reviewlink = "https://www.rottentomatoes.com" + reviewsdata
               reviewpagedata = getPageData(reviewlink)
               reviewroot = html.fromstring(reviewpagedata)

               reviewjsondatastr = reviewroot.xpath('string(//script[@data-json="props"]/text())')
               if reviewjsondatastr:
                    review_jsondata = json.loads(reviewjsondatastr)
                    media_id = review_jsondata.get("media").get("emsId")
                    newurl = f"https://www.rottentomatoes.com/napi/rtcf/v1/movies/{media_id}/reviews?after=&before=&pageCount=20&topOnly=false&type=critic&verified=false"
                    while True:
                        reviewfinaljsondata = json.loads(getPageData(newurl))
                        # print(reviewfinaljsondata)
                        for reviewitem in reviewfinaljsondata.get("reviews"):    
                         
                            try:
                                name = reviewitem.get("critic").get("displayName")
                            except Exception as e :
                                name = ""
                            try:                   
                                subtitle = reviewitem.get("publication").get("name")
                            except Exception as e:
                                subtitle="" 

                            tempreviewdata = {
                                    "name": name,
                                    "subtitle":subtitle,
                                    "description":reviewitem.get("reviewQuote")
                            }
                         #    reviewList.append(tempreviewdata)
                            cursor.execute("""
                                   INSERT INTO reviews
                                   (movie_id, reviewer_name, reviewer_source, review_text)
                                   VALUES (%s, %s, %s, %s)
                                   """, (
                                        movie_id,
                                        tempreviewdata.get("name"),
                                        tempreviewdata.get("subtitle"),
                                        tempreviewdata.get("description")
                                   ))
                            
                        if reviewfinaljsondata.get("pageInfo").get("endCursor"):
                            value = reviewfinaljsondata.get("pageInfo").get("endCursor")
                            newurl = f"https://www.rottentomatoes.com/napi/rtcf/v1/movies/{media_id}/reviews?after={value}&before=&pageCount=20&topOnly=false&type=critic&verified=false"
                        else:
                            break

        

          finalObject.append(
               {
                    "movieName" : movieName,
                    "posterimage":posterimage,
                    "tomatometer":tomatometer,
                    "reviews":reviews,
                    "description":description,
                    "whatToknow" : whatToknowObj,
                    "castandCrewlist" : castandCrewlist,
                    "reviewsList":reviewList,
                    "videolist":videolist
               }
          )
          

          # i = i +1 
          # if i == 2:
          #   break
mydb.commit()
mydb.close()


# print(finalObject)    

# with open("finalOutputbyself.json","w",encoding="utf-8") as f:
#      json.dump(finalObject,f)