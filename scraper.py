"""
Responsible for scraping web data for news, NBA scores, and weather.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import config

def weather():
    key = "" #API KEY HERE
    lat = "" #LATITUDE HERE
    lon = "" #LONGITUDE HERE
    units = "imperial"
    
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=" + lat + "&lon=" + lon + "&units=" + units + "&appid=" + key
    
    response = requests.get(url).json()
    
    ret = []
    
    for i in response["daily"]:
       
        day = datetime.fromtimestamp(i["dt"]).strftime("%A")[:3]
        temp = int(round(i["temp"]["day"]))
        icon = i["weather"][0]["icon"]
        ret.append([day, temp, icon])
    
    currenttemp = response["current"]["temp"]
    currentid = response["current"]["weather"][0]["icon"]
    
    ret[0] = ["Now", int(round(currenttemp)), currentid]
    
    config.weather_list = ret

def headlines():
    url = "https://news.google.com/news/rss"
    
    r = requests.get(url)
    
    soup = BeautifulSoup(r.content, "xml")
    
    lst = []
    count = 0
    for i in soup.findAll("item"):
        if count < 4:
            lst.append(i.title.text)
            count = count + 1
        else:
            break
    config.news_list = lst
    
    
def basketball():
    url = 'https://www.basketball-reference.com/boxscores'
    
    r = requests.get(url)
    
    soup = BeautifulSoup(r.content, "html.parser")
    
    winners = soup.findAll("tr", {"class": "winner"})
    
    winlist = []
    
    for team in winners:
        b = (team.findAll("td"))
        temp = []
        for j in b:
            
            filter = j.getText().strip()
            if(len(filter) > 0):
                temp.append(filter)
                
            else:
                temp.append("")
        winlist.append(temp)
        
    losers = soup.findAll("tr", {"class": "loser"})
    
    losslist = []
    for team in losers:
        b = (team.findAll("td"))
        temp = []
        for j in b:
            
            filter = j.getText().strip()
            
            if(filter != ""):
                
                temp.append(filter)
                
            else:
                temp.append("")
        losslist.append(temp)
                
    for i in range(0, len(winlist)):
        if losslist[i][2] == "Final" or winlist[i][2] == "":
            a = winlist[i][2]
            winlist[i][2] = losslist[i][2]
            losslist[i][2] = a
    
    config.winners = winlist
    config.losers = losslist


    
