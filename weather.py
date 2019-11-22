import requests
import os
import shutil
from bs4 import BeautifulSoup
from datetime import datetime


def save(file, data):
    f = open('log/'+file, "a", newline='')
    f.write("%s\n" % data)
    f.close()
    return


def writeLog(logText):
    stamp = datetime.now()
    w = 'weather.log'
    log = open('log/'+w, "a", newline='')
    log.write(str(stamp) + " - " + str(logText)+"\n")
    log.close()
    return

l = []
f = 'weather.txt'



root = os.path.dirname(os.path.abspath(__file__))
DIR = root+'\log'

shutil.rmtree(DIR)
os.mkdir(DIR)

writeLog("Directory: " +DIR)

page = requests.get("https://weather.com/en-IN/weather/tenday/l/ef7f13b9534857ea753d5c744794e4c2aaee79f3b7e2ffb8c8a55596aad226f1")
content = page.content
soup = BeautifulSoup(content, "html.parser")

if page != None : writeLog("Message: BeautifulSoup has successfully requested the page")
else : writeLog("Message: BeautifulSoup was unsuccessful in requesting the page")


all = soup.find("div", {"class": "locations-title ten-day-page-title"}).find("h1").text

table = soup.find_all("table", {"class": "twc-table"})
for items in table:
    for i in range(len(items.find_all("tr")) - 1):
        d = {}
        try:
            d["Day"] = items.find_all("span", {"class": "date-time"})[i].text
            d["Date"] = items.find_all("span", {"class": "day-detail"})[i].text
            d["Desc"] = items.find_all("td", {"class": "description"})[i].text.lower()
            d["H/L Temp"] = items.find_all("td", {"class": "temp"})[i].text
            d["Precip"] = items.find_all("td", {"class": "precip"})[i].text
            d["Wind"] = items.find_all("td", {"class": "wind"})[i].text
            d["Humidity"] = items.find_all("td", {"class": "humidity"})[i].text
        except:
            d["Day"] = "None"
            d["Date"] = "None"
            d["Date"] = "None"
            d["H/L Temp"] = "None"
            d["Precip"] = "None"
            d["Wind"] = "None"
            d["Humidity"] = "None"
        writeLog("Message: Weather data for "+d["Date"]+" has been appended.")
        l.append(d)

        s = "\nDetroit Weather for "+d["Day"]+", "+d["Date"]+":\nIt will be "+d["Desc"]+" with high and low temperature(celsius) "\
            + d["H/L Temp"]+"\nChance of rain: "+d["Precip"]+"\nWind info: "+d["Wind"]+"\nHumidity info: "+d["Humidity"]

        print(s)
        save(f, s)

writeLog("Message: File has been saved.")
writeLog("Message: Execution terminated normally.")

