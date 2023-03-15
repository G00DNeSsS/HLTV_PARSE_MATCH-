from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import requests
import urllib.parse
import json

settings = open('data.json')
config = json.load(settings)

url = 'https://www.hltv.org/stats/teams/map/'
TB = 0
TM = 0
map_play_dict = {
    "1" :["Inferno","33/"],
    "2" :["Nuke", "34/"],
    "3" : ["Overpass","40/"],
    "4" : ["Anubis","48/"],
    "5" : ["Vertigo","46/"],
    "6" : ["Mirage","32/"],
    "7" : ["Ancient","47/"],
}

team_dict = {
    "1" : ["G2","5995/g2?"],
    "2" : ["heroic","7175/heroic?"],
    "3" : ["liquid","5973/liquid?"],
    "4" : ["faze","6667/faze?"],
    "5" : ["natus-vincere","4608/natus-vincere?"],
    "6" : ["vitality","9565/vitality?"],
    "7" : ["outsiders","11595/outsiders?"],
    "8" : ["og","10503/og?"],
    "9" : ["fnatic","4991/fnatic?"],
    "10" : ["cloud9","5752/cloud9?"],
    "11" : ["mouz","4494/mouz?"],
    "12" : ["complexity","5005/complexity?"],
    "13" : ["furia","8297/furia?"],
    "14" : ["spirit","7020/spirit?"],
    "15" : ["astralis","6665/astralis?"],
    "16" : ["big","7532/big?"],
    "17" : ["ninjas-in-pyjamas","4411/ninjas-in-pyjamas?"],
    "18" : ["eternal-fire","11251/eternal-fire?"],
    "19" : ["ihc","11585/ihc?"],
    "20" : ["ence","4869/ence?"],
    "21" : ["bad-news-eagles","11518/bad-news-eagles?"],
    "22" : ["mibr","9215/mibr?"],
    "23" : ["9ine","10278/9ine?"],
    "24" : ["saw","10567/saw?"],
    "25" : ["movistar-riders","7718/movistar-riders?"],
    "26" : ["aurora","11861/aurora?"],
    "27" : ["gamerlegion","9928/gamerlegion?"],
    "28" : ["evil-geniuses","10399/evil-geniuses?"],
    "29" : ["forze","8135/forze?"],
    "30" : ["pain","4773/pain?"]
}

print("1.Inferno\n2.Nuke\n3.Overpass\n4.Anubis\n5.Vertigo\n6.Mirage\n7.Ancient\n")
map_play = input('Выберите карту: ')
for val in map_play_dict.keys():
    if map_play == val:
        url = url + map_play_dict[val][1]
        team_map = map_play_dict[val][0]
print("1.G2\n2.Heroic\n3.Liquid\n4.Faze\n5.NAVI\n6.Vitality\n7.Outsiders\n8.Og\n9.fnatic\n10.Cloud 9\n11.Mouz\n12.Complexity\n13.Furia\n14.Spirit\n15.Astralis\n16.Big\n17.NIP\n18.Enternal Fire\n19.IHC\n20.ENCE\n21.Bad News Eagles\n22.MIBR\n23.9INE\n24.SAW\n25.Movistars Riders\n26.Aurora\n27.GamerLegion\n28.Evil Geniuses\n29.FORZE\n30.paiN\n")
team = input('Введите команду: ')
for val in team_dict.keys():
    if team == val:
        url = url + team_dict[val][1]
        team_name = team_dict[val][0]
year_before = input('Введите год от: ')
month_before = input('Введите месяц от: ')
day_before = input('Введите день от: ')
year_after = input('Введите год до: ')
month_after = input('Введите месяц до: ')
day_after = input('Введите день до: ')
 
url = url + 'startDate='+year_before+'-'+month_before+'-'+day_before+'&endDate='+year_after+'-'+month_after+'-'+day_after
print(url)
sa_key = config['ScrapingAnt API Token']
sa_api = 'https://api.scrapingant.com/v2/general'
qParams = {'url': url, 'x-api-key': sa_key}
reqUrl = f'{sa_api}?{urllib.parse.urlencode(qParams)}'
r = requests.get(reqUrl)
soup = BeautifulSoup(r.content,'html.parser')
game = soup.find('table',attrs={'class' : 'stats-table'})
data = []
table_body = game.find('tbody')
rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])

for elem in data:
    last = elem[1]
    elem[1] = team_name + ' - ' + last 
    elem.append(team_map)
    head, sep, tail = elem[3].partition(' - ')
    summa =  int(head) + int(tail)
    if summa > 26.5:
        TB +=1
    else:
        TM +=1

data.append(['TБ 26.5 - '+str(TB)+'шт.'])
data.append(['TМ 26.5 - '+str(TM)+'шт.'])

scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("gs_credentials.json", scope)
client = gspread.authorize(credentials)
sheet = client.open("NewDatabase").sheet1
df = pd.DataFrame(data)
df.columns =['Дата', 'Соперник', 'Ивент', 'Результат','Карта']
sheet.clear()
sheet.update([df.columns.values.tolist()] + df.values.tolist())