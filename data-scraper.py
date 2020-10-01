import requests
from bs4 import BeautifulSoup
import csv 

url = 'https://www.billboard.com/charts/hot-100'
#Possible access denied error fix
agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

result = requests.get(url, headers=agent)
print(result.status_code)
headers = open("headers.txt", "w")
headers.write(str(result.headers))
content = result.content
src = open("src.txt", "w")
src.write(str(content))

soup = BeautifulSoup(content, "html.parser")

#soup_file = open("soup.txt", "w")
#soup_file.write(str(soup))

table = soup.find('ol', attrs = {'class':'chart-list__elements'})
#table_file = open("table.txt", "w")
#table_file.write(str(table.prettify()))

res = []
dic = {}
table_c = table.find_all('li')
for elem in table_c:
	#dic['name'] = elem.span['chart-element__information__song'].text()
	#print(elem.span['chart-element__information__song'].text())
	dic = {}
	dic['Name'] = elem.find('span', attrs = {'class':"chart-element__information__song"}).text
	dic['Artist'] = elem.find('span', attrs = {'class':"chart-element__information__artist"}).text
	dic['Last week'] = elem.find('span', attrs = {'class':"chart-element__information__delta__text text--last"}).text[:2]
	dic['Peak'] = elem.find('span', attrs = {'class':"chart-element__information__delta__text text--peak"}).text[:2]
	dic['Wks on chart'] = elem.find('span', attrs = {'class':"chart-element__information__delta__text text--week"}).text[:2]
	dic['song_id'] = dic['Name']+dic['Artist']
	res.append(dic)
res_file = 'list.csv'

with open(res_file, 'w', newline='') as f:
	w = csv.DictWriter(f,['Name', 'Artist', 'Last week', 'Peak', 'Wks on chart', 'song_id'])
	w.writeheader()
	for elem in res:
		w.writerow(elem)
