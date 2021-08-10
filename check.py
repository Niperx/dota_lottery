import requests
import json
from bs4 import BeautifulSoup

url = 'https://ru.dotabuff.com/heroes'

response = requests.get(url, headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'})
soup = BeautifulSoup(response.text, 'html.parser')

heroes_list = []
# print(soup.select('.hero-grid'))
for el in soup.select('.hero-grid > a'):
	x = 0
	title = el.select('.hero > .name')
	heroes_list.append(title[x].text)
	x += 1

with open("heroes.json", 'w', encoding='utf-8') as write_message:
	json.dump(heroes_list, write_message, ensure_ascii=False, indent=4)
	# for x in title:
	# 	for y in x:
	# 		y = re.findall('\d+', y)
	# 		if len(y) != 0:
	# 			matches.append(y[0])

