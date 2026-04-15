import json
import requests
from lxml import html
from db import mydb
from datetime import date,datetime

mycursor = mydb.cursor()

sql_query = """
CREATE TABLE IF NOT EXISTS musiclist (
    id INT AUTO_INCREMENT PRIMARY KEY,
    musicname VARCHAR(255),
    artistname VARCHAR(255),
    imageurl VARCHAR(255),
    Lw VARCHAR(5),
    Peak INT,
    weeks INT,
    DebutPosition INT,
    DebutChartDate VARCHAR(255),
    PeakChartDate VARCHAR(255),
    Awards VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
"""
mycursor.execute(sql_query)

url = "https://www.billboard.com/charts/hot-100/"
data = requests.get(url)
MusicDataList= []
if data.status_code == 200:
    root = html.fromstring(data.text)
    musiclist = root.xpath('//div[contains(@class,"chart-results-list")]/div[@class="o-chart-results-list-row-container"]')
    for item in musiclist:
        eachitem = item.xpath('ul[contains(@class,"o-chart-results-list-row")]/li')
        imageurl = eachitem[1].xpath('div/div/img/@src')[0]
        songName = eachitem[3].xpath('ul/li/h3/text()')[0].strip()
        artistName = eachitem[3].xpath('ul/li/span/text()')[0].strip()
        if artistName == "" or artistName == None:
            artistName = eachitem[3].xpath('ul/li/span/a/text()')[0].strip()

        rightsection = eachitem[3].xpath('ul/li/ul/div[@class="lrv-u-flex"]/li/span/text()')
        lw = rightsection[0].strip()
        peak = int(rightsection[1].strip())
        weeks = int(rightsection[2].strip())
        itemExpand= item.xpath('div/div[@class="charts-results-item-detail-inner // "]/div')
        debutPosition = itemExpand[0].xpath('div[@class="o-chart-position-stats__debut"]/div/span/text()')[0].strip()
        debutChartDate = itemExpand[0].xpath('div[@class="o-chart-position-stats__debut"]/div/div/span/a/text()')[0].strip()
        peakChartDate = itemExpand[0].xpath('div[@class="o-chart-position-stats__peak"]/div[@class="o-chart-position-stats__number"]/div/span/a/text()')[0].strip()
        awardLists = itemExpand[1].xpath('div[@class="o-chart-awards-list"]/div')
        finalawardList = []
        if awardLists:
            for award in awardLists:
                awardname = award.xpath('p/text()')[0]
                finalawardList.append(awardname)

        awardListsData = ", ".join(finalawardList)
        # debutChartDate = datetime.strptime(debutChartDate, "%d/%m/%y").date()
        # peakChartDate = datetime.strptime(peakChartDate, "%m/%d/%y").date()

        musicData = {
            "imageurl" : imageurl,
            "songName" : songName,
            "artistName" : artistName,
            "lw" : lw,
            "peak": peak,
            "weeks" :weeks,
            "debutPosition" : debutPosition,
            "debutChartDate" : debutChartDate,
            "peakChartDate" : peakChartDate,
            "awardLists" : awardListsData

        }
        MusicDataList.append(musicData)
        sql = """
            INSERT INTO musiclist (musicname, artistname, imageurl, Lw, Peak, weeks,  DebutPosition, DebutChartDate, PeakChartDate, Awards)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
        val =(songName,artistName,imageurl,lw,peak,weeks,debutPosition,debutChartDate,peakChartDate,awardListsData)
        mycursor.execute(sql,val)
        mydb.commit()

    #    break
    #    print(musicData)

#print(MusicDataList)
with open("output.json","w",encoding="utf-8") as f:
    json.dump(MusicDataList,f)        
#print(MusicDataList)