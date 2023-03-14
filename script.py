from bs4 import BeautifulSoup
import cloudscraper
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

url = 'https://www.hltv.org/stats/teams/map/'
TB = 0
TM = 0
print("1.Inferno\n2.Nuke\n3.Overpass\n4.Anubis\n5.Vertigo\n6.Mirage\n7.Vertigo\n8.Ancient\n")
map_play = int(input('Выберите карту: '))
print("1.G2\n2.Heroic\n3.Liquid\n4.Faze\n5.NAVI\n6.Vitality\n7.Outsiders\n8.Og\n9.fnatic\n10.Cloud 9\n11.Mouz\n12.Complexity\n13.Furia\n14.Spirit\n15.Astralis\n16.Big\n17.NIP\n18.Enternal Fire\n19.IHC\n20.ENCE\n21.Bad News Eagles\n22.MIBR\n23.9INE\n24.SAW\n25.Movistars Riders\n26.Aurora\n27.GamerLegion\n28.Evil Geniuses\n29.FORZE\n30.paiN\n")
team = int(input('Введите команду: '))
year_before = input('Введите год от: ')
month_before = input('Введите месяц от: ')
day_before = input('Введите день от: ')
year_after = input('Введите год до: ')
month_after = input('Введите месяц до: ')
day_after = input('Введите день до: ')

if map_play == 1:
    url = url + "33/"
if map_play == 2:
    url = url + "34/"
if map_play == 3:
   url = url + "40/"
if map_play == 4:
    url = url + "48/"
if map_play == 5:
    url = url + "46/"
if map_play == 6:
    url = url + "32/"
if map_play == 7:
    url = url + "46/"
if map_play == 8:
    url = url + "47/"



if team == 1:
    url = url + "5995/g2?"
    team_name = "G2"
if team == 2:
    url = url + "7175/heroic?"
    team_name = "Heroic"
if team == 3:
    url = url + "5973/liquid?"
    team_name = "Liquid"
if team == 4:
    url = url + "6667/faze?"
    team_name = "FaZe"
if team == 5:
    url = url + "4608/natus-vincere?"
    team_name = "NaVi"
if team == 6:
    url = url + "9565/vitality?"
    team_name = "Vitality"
if team == 7:
    url = url + "11595/outsiders?"
    team_name = "Outsiders"
if team == 8:
    url = url + "10503/og?"
    team_name = "OG"
if team == 9:
    url = url + "4991/fnatic?"
    team_name = "fnatic"
if team == 10:
    url = url + "5752/cloud9?"
    team_name = "Cloud9"
if team == 11:
    url = url + "4494/mouz?"
    team_name = "MOUZ"
if team == 12:
    url = url + "5005/complexity?"
    team_name = "Complexity"
if team == 13:
    url = url + "8297/furia?"
    team_name = "Furia"
if team == 14:
    url = url + "7020/spirit?"
    team_name = "Spirit"
if team == 15:
    url = url + "6665/astralis?"
    team_name = "Astralis"
if team == 16:
    url = url + "7532/big?"
    team_name = "BIG"
if team == 17:
    url = url + "4411/ninjas-in-pyjamas?"
    team_name = "NIP"
if team == 18:
    url = url + "11251/eternal-fire?"
    team_name = "Eternal Fire"
if team == 19:
    url = url + "11585/ihc?"
    team_name = "IHC"
if team == 20:
    url = url + "4869/ence?"
    team_name = "Ence"
if team == 21:
    url = url + "11518/bad-news-eagles?"
    team_name = "Bad News Eagles"
if team == 22:
    url = url + "9215/mibr?"
    team_name = "MIBR"
if team == 23:
    url = url + "10278/9ine?"
    team_name = "9INE"
if team == 24:
    url = url + "10567/saw?"
    team_name = "SAW"
if team == 25:
    url = url + "7718/movistar-riders?"
    team_name = "Movistars Riders"
if team == 26:
    url = url + "11861/aurora?"
    team_name = "Aurora"
if team == 27:
    url = url + "9928/gamerlegion?"
    team_name = "GamerLegion"
if team == 28:
    url = url + "10399/evil-geniuses?"
    team_name = "Evil Geniuses"
if team == 29:
    url = url + "8135/forze?"
    team_name = "FORZE"
if team == 30:
    url = url + "4773/pain?"
    team_name = "paIN"
 
url = url + 'startDate='+year_before+'-'+month_before+'-'+day_before+'&endDate='+year_after+'-'+month_after+'-'+day_after
print(url)

scraper = cloudscraper.create_scraper(delay=10,   browser={'custom': 'ScraperBot/1.0',})
req = scraper.get(url)
soup = BeautifulSoup(req.content,'html.parser')
game = soup.find('table',attrs={'class' : 'stats-table'})
data = []
table_body = game.find('tbody')
rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])

for elem in data:
    head, sep, tail = elem[3].partition(' - ')
    summa =  int(head) + int(tail)
    if summa > 26.5:
        TB +=1
    else:
        TM +=1

for elem in data:
    last = elem[1]
    elem[1] = team_name + ' - ' + last 

data.append(['TБ 26.5 - '+str(TB)+'шт.'])
data.append(['TМ 26.5 - '+str(TM)+'шт.'])

# Подсоединение к Google Таблицам
scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]
data_1 = [[]]
credentials = ServiceAccountCredentials.from_json_keyfile_name("gs_credentials.json", scope)
client = gspread.authorize(credentials)
sheet = client.open("NewDatabase").sheet1
df = pd.DataFrame(data)
df.columns =['Дата', 'Соперник', 'Ивент', 'Результат']
sheet.clear()
sheet.update([df.columns.values.tolist()] + df.values.tolist())