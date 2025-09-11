import requests
import re
import json
from pprint import pprint
from urllib.parse import quote
from html import unescape

DATA = {}
    
def scrape_PRTS():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    url = "https://prts.wiki/api.php"
    LINKAGE = '联动寻访'
    LIMITED = '限定寻访'
    LIMITED_OBTAIN_METHODS = [LINKAGE, LIMITED]
    limit = 500
    offset = 0
    # you can use CO.obtainMethod to list limited operators
    params = {
        "action": "cargoquery",
        "tables": "char_obtain=CO,chara=C",
        "fields": "CO._pageName=page,CO.cnOnlineTime=cnOnlineTime,CO.obtainMethod=obtainMethod,C.charId=charId",
        "join_on": "CO._pageName=C._pageName",
        "format": "json",
    }
    while 1:
        params['limit'] = limit
        params['offset'] = offset
        r = requests.get(url, params=params, headers=headers)
        pages = r.json()['cargoquery']
        for page in pages:
            charId = page['title']['charId']
            obtain = page['title']['obtainMethod']
            online = page['title']['cnOnlineTime']
            limited = obtain in LIMITED_OBTAIN_METHODS
            DATA[charId] = {'cnOnlineTime':online, 'isLimited': limited}
        offset += limit
        if len(pages) < limit:
            break
    return DATA
def scrape_wiki():
    # update the prts.wiki data with global release dates from arknights.wiki.gg/
    # while it is possible to get limited status and some CN dates from the wiki, those only come from prts for now.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    url = "https://arknights.wiki.gg/api.php"
    limit = 500
    offset = 0
    # if you need the rest of the data use fields "E.cn_date_start" and "E.event_type"
    params = {
        "action": "cargoquery",
        "tables": "Operators=O,Events=E,OperatorFiles=F",
        "fields": "E.global_date_start=start,F.id=charId",
        "join_on": "O.event=E.name,F.name=O.name",
        "format": "json",
        "where": "F.id IS NOT NULL AND E.global_date_start IS NOT NULL",
    }
    while 1:
        params['limit'] = limit
        params['offset'] = offset
        r = requests.get(url, params=params, headers=headers)
        pages = r.json()['cargoquery']
        for page in pages:
            charId = page['title']['charId']
            online = page['title']['start']
            if charId in DATA:
                DATA[charId]['onlineTime'] = online
        offset += limit
        if len(pages) < limit:
            break
    return DATA
scrape_PRTS()
scrape_wiki() # must call AFTER scrape_PRTS as it will update DATA (and relies on it being filled)
with open('./json/operator_release_dates.json','w') as f:
    json.dump(DATA,f)
