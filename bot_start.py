# -*- coding: utf-8 -*-
import vk_api
from vk_api.upload import VkUpload
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType

import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random
from PIL import Image, ImageDraw, ImageFont
from urllib.request import urlopen
#pip install Pillow


from settings import *
from test import *

vk_session = vk_api.VkApi(token=token)

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
upload = VkUpload(vk_session)

def send_user(user, msg, attachment=''):
	vk_session.method('messages.send',
		{
		'user_id': user,
		'message': msg,
		'random_id': 0,
		'attachment': attachment
		}
	)

def delete_message_chat(chat_id, message_id):
	vk_session.method('messages.delete',
		{
		'message_ids': message_id,
		'delete_for_all': 1,
		'chat_id': chat_id
		}
	)

def send_user_reply(user, msg, reply='', attachment=''):
	vk_session.method('messages.send',
		{
		'user_id': user,
		'message': msg,
		'random_id': 0,
		'attachment': attachment,
		'reply_to': reply
		}
	)

def send_chat(chat, msg, attachment=''):
	vk_session.method('messages.send',
		{
		'chat_id': chat,
		'message': msg,
		'random_id': 0,
		'attachment': attachment
		}
	)

def send_chat_reply(chat, msg, reply='', attachment=''):
	vk_session.method('messages.send',
		{
		'chat_id': chat,
		'message': msg,
		'random_id': 0,
		'attachment': attachment,
		'reply_to': reply
		}
	)

def photo_messages(img):
	url = session_api.photos.getMessagesUploadServer(peer_id=0)['upload_url']
	res = requests.post(url, files={'photo': open(img, 'rb')}).json()
	result = session_api.photos.saveMessagesPhoto(**res)[0]
	photo_name = "photo{}_{}".format(result["owner_id"], result["id"])
	print('Фото ID: '+photo_name)
	return photo_name

def get_user_name(user_id):
	user = session_api.users.get(user_ids=user_id)
	fullname = [user[0]['first_name'], user[0]['last_name']]
	return fullname




def create_test():
	with open("match.json", 'r', encoding='utf-8') as read_message:
		message = json.load(read_message)

	my_list = []
	for item in message.keys():
		my_list.append(item)

	hero_list = []
	chk = 3
	while chk != 0: 
		hero = random.choice(my_list)
		hero_list.append(hero)
		my_list.remove(hero)
		chk -= 1

	current_hero = random.choice(hero_list)

	for url in message[current_hero]:
		hero_img = url
		print('Картинка: '+hero_img)
		break

	img_bag = Image.open('bag.jpg')

	url_hero = message[current_hero][0]
	headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
	img_hero = Image.open(requests.get(url_hero, stream=True, headers = headers).raw)

	wid, yid = 6, 5
	for url in message[current_hero]:
		if current_hero not in url.replace('-', ' '):
			print(url)
			maxsize = (60, 43)
			im = Image.open(requests.get(url, stream=True, headers = headers).raw)
			im.thumbnail(maxsize, Image.ANTIALIAS)
			img_bag.paste(im, (wid, yid))

			wid += 66
			if wid >= 150:
				yid += 48
				wid = 6

	img_bag.save('bag1.jpg') # Отправить в чат

	img_bg = Image.open('bg.jpg')
	chk = 3
	wid, yid = 2, 2
	while chk != 0: 
		hero = random.choice(hero_list)

		maxsize = (60, 43)
		im = Image.open(requests.get(message[hero][0], stream=True, headers = headers).raw)
		img_bg.paste(im, (wid, yid))
		chk -= 1
		wid += 130

		hero_list.remove(hero)

	img_bg.save('bg1.jpg') # Отправить в чат

	result = [current_hero]

	with open("result.json", 'w', encoding='utf-8') as write_message:
		json.dump(result, write_message, ensure_ascii=False, indent=4)


	x1 = photo_messages('bg1.jpg')
	x2 = photo_messages('bag1.jpg')
	# send_user(user_id, 'Угадайте героя по билду', photo_messages('bg1.jpg'))
	# send_user(user_id, '', photo_messages('bag1.jpg'))


	send_chat(10, 'Угадайте героя по билду', x1)
	send_chat(10, '', x2)


with open("heroes.json", 'r', encoding='utf-8') as read_message:
	heroes = json.load(read_message)

delete_messages = []

while True:
	try:
		for event in longpoll.listen():
			# if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
			if event.type == VkEventType.MESSAGE_NEW and event.text:
				print('\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/')
				print('Сообщение пришло в: ' + str(datetime.strftime(datetime.now(), "%H:%M:%S")))
				print('Текст сообщения: ' + str(event.text))
				print('ID пользователя: ' + str(event.user_id))
				print('===========================================')

				if event.from_chat:
					response = event.text.lower()
					text = ''
					fullname = get_user_name(event.user_id)
					print('Кто: '+fullname[0]+' '+fullname[1])
					print('Номер сообщения: '+str(event.message_id))

					if 'это правильный ответ!' in response:
						delete_messages.append(event.message_id)

					if 'угадайте героя по билду' in response:
						delete_messages.append(event.message_id)
						delete_messages.append(event.message_id + 1)

					if 'минус бал тебе в ебало, лошара' in response:
						delete_messages.append(event.message_id)

					if response == 'мем' and event.user_id == 201044121:

						get_match_info()
						create_test()

					if response == '!shop' and event.user_id == 201044121:

						text = 'Пнуть по ебалу участника беседы - 2000 поинтов\nЗамутить участника беседы на 2 часа - 4000 поинтов\nКикнуть участника беседы нахуй отсюда - 10000 поинтов'
						send_chat_reply(10, text, event.message_id)
						delete_messages.append(event.message_id)

					with open("heroes.json", 'r', encoding='utf-8') as read_message:
						heroes = json.load(read_message)

					with open("result.json", 'r', encoding='utf-8') as read_message:
						message = json.load(read_message)

					if response == message[0]:
						delete_messages.append(event.message_id)
						# Человек получает поинты
						with open("stats.json", 'r', encoding='utf-8') as read_message:
							msg = json.load(read_message)

						user_id = str(event.user_id)
						player = msg.get(user_id)
						if player != None:
							msg.update({user_id : player + 1})
						else:
							msg.update({user_id : 1})

						lead_text = "⭐️ ТОП знатоков ⭐️️ \n\n"
						k = {k: v for k, v in sorted(msg.items(), key=lambda item: item[1], reverse=True)}
						y = 1
						for key in k:
							if y == 1:
								smile = "🥇"
							elif y == 2:
								smile = "🥈"
							elif y == 3:
								smile = "🥉"
							else:
								smile = "🎗"
							fullname = get_user_name(key)
							lead_text += smile + " " + str(y) + ". " + fullname[0]+' '+fullname[1] + " - " + str(k[key]) + " points. " + smile + "\n"
							y += 1

						text = 'Это правильный ответ!\n\n ' + lead_text + '\n\nМагазин открывается с 1000 поинтов.\n\nОжидайте следующий билд...'
						print(text)

						send_chat_reply(10, text, event.message_id)

						with open("stats.json", 'w', encoding='utf-8') as write_message:
							json.dump(msg, write_message, ensure_ascii=False, indent=4)

						time.sleep(120)
						get_match_info()
						create_test()

						for msg in delete_messages:
							try:
								delete_message_chat(10, msg)
							except vk_api.exceptions.ApiError:
								continue

						delete_messages = []


					heroes.remove(message[0])
					for name in heroes:
						if response == name:
							with open("stats.json", 'r', encoding='utf-8') as read_message:
								msg = json.load(read_message)

							user_id = str(event.user_id)
							player = msg.get(user_id)
							if player != None:
								msg.update({user_id : player - 3})
								text = 'Минус бал тебе в ебало, лошара'
								send_chat_reply(10, text, event.message_id)
								delete_messages.append(event.message_id)
							else:
								msg.update({user_id : 0})

							with open("stats.json", 'w', encoding='utf-8') as write_message:
								json.dump(msg, write_message, ensure_ascii=False, indent=4)

	except requests.exceptions.ReadTimeout:
		print("\n Переподключение к серверам ВК \n")
		time.sleep(3)
				

		# if event.from_user and not (event.from_me):
		# 	response = event.text.lower()
		# 	text = ''
		# 	fullname = get_user_name(event.user_id)
		# 	print('Кто: '+fullname[0]+' '+fullname[1])
		# 	print('Номер сообщения: '+str(event.message_id))

		# 	if response == 'мем' and event.user_id == 201044121:

		# 		create_test(event.user_id)


		# 	with open("result.json", 'r', encoding='utf-8') as read_message:
		# 		message = json.load(read_message)

		# 	if response == message[0]:
		# 		# Человек получает поинты
		# 		text = 'Это правильный ответ!\nОжидайте следующий билд...'
		# 		send_user_reply(event.user_id, text, event.message_id)

		# 		get_match_info()
		# 		create_test(event.user_id)

		# 		time.sleep(35)
