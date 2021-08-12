import requests
from bs4 import BeautifulSoup
import re
import random
import json

main = 'https://ru.dotabuff.com'
# url1 = 'https://ru.dotabuff.com/matches?game_mode=single_draft&skill_bracket=normal_skill'
url1 = 'https://ru.dotabuff.com/matches?game_mode=ability_draft'
url = 'https://ru.dotabuff.com/matches/'

def get_match_info():

	# ВЗЯТЬ СЛУЧАЙНЫЙ МАТЧ

	response = requests.get(url1, headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'})
	soup = BeautifulSoup(response.text, 'html.parser')
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
	hero_info_list = {}
	# print(soup1)
	for hero in soup1.find_all('tr', class_='col-hints'):

		items_list = []
		current_hero = hero.find('div', class_='image-container image-container-hero image-container-icon image-container-overlay')
		if current_hero != None:

			hero_info = current_hero.find('a', href=True)['href']
			hero_name = hero_info[hero_info.rfind('/')+1:]
			hero_name = hero_name.replace('-', ' ')
			# print('Герой: ' + hero_name) # Название героя

			hero_img = main + current_hero.find('img', src=True)['src']
			# print('Иконка героя: ' + hero_img + '\n') # Иконка героя

			hero_items = hero.find('div', class_='player-inventory-items')

			items_list.append(hero_img)

			i = 1
			for item in hero_items.find_all('div', class_='match-item-with-time'):
				try:
					item_info = item.find('a', href=True)['href']
					item_name = item_info[item_info.rfind('/')+1:]
					item_name = item_name.replace('-', ' ')
					# print('Предмет #'+str(i)+': ' + item_name) # Название предмета

					item_img = main + item.find('img', src=True)['src']

					# print('Иконка предмета: ' + item_img) # Иконка предмета


					items_list.append(item_img)
					
					i += 1
				except:
					continue

			hero_info_list.update({hero_name : items_list})





	with open("match.json", 'w', encoding='utf-8') as write_message:
		json.dump(hero_info_list, write_message, ensure_ascii=False, indent=4)

# get_match_info()
# from settings import *
# import vk_api

# vk_session = vk_api.VkApi(token=token)

# session_api = vk_session.get_api()

# delete_messages = [2866418, 2866419, 2866420]

# for msg in delete_messages:
# 	vk_session.method('messages.delete',
# 		{
# 		'message_ids': msg,
# 		'delete_for_all': 1,
# 		'chat_id': 10
# 		}
# 	)