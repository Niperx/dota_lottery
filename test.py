import requests
from bs4 import BeautifulSoup
import re
import random

main = 'https://ru.dotabuff.com'
url = 'https://ru.dotabuff.com/matches/'

# ВЗЯТЬ СЛУЧАЙНЫЙ МАТЧ

response = requests.get(url, headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'})
soup = BeautifulSoup(response.text, 'html.parser')
# quotes = soup.find_all('tr')

# for n in en
# # print(quotes)

# print(soup)
matches = []
for el in soup.select('tr'):
	title = el.select('td > a')
	for x in title:
		for y in x:
			y = re.findall('\d+', y)
			if len(y) != 0:
				matches.append(y[0])

match = random.choice(matches)


print(match)

# ВЗЯТЬ ИМЯ И КАРТИНКУ ГЕРОЯ

response1 = requests.get(url + str(match), headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'})
soup1 = BeautifulSoup(response1.text, 'lxml')

for hero in soup1.find_all('tr', class_='col-hints'):
	current_hero = hero.find('div', class_='image-container image-container-hero image-container-icon image-container-overlay')
	if current_hero != None:

		hero_info = current_hero.find('a', href=True)['href']
		hero_name = hero_info[hero_info.rfind('/')+1:].title()
		hero_name = hero_name.replace('-', ' ')
		print('Герой: ' + hero_name) # Название героя

		hero_img = main + current_hero.find('img', src=True)['src']
		print('Иконка героя: ' + hero_img + '\n') # Иконка героя

		hero_items = hero.find('div', class_='player-inventory-items')
		# print(hero_items)

		i = 1
		for item in hero_items.find_all('div', class_='match-item-with-time'):
			try:
				item_info = item.find('a', href=True)['href']
				item_name = item_info[item_info.rfind('/')+1:].title()
				item_name = item_name.replace('-', ' ')
				print('Предмет #'+str(i)+': ' + item_name) # Название предмета

				item_img = main + item.find('img', src=True)['src']
				print('Иконка предмета: ' + item_img) # Иконка предмета
				i+=1
			except:
				continue

		print('\n\n\n\n\n')

