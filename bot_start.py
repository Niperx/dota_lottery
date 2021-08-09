# -*- coding: utf-8 -*-
import vk_api
from vk_api.upload import VkUpload
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType

import math
import os.path
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import sqlite3
import threading
import random
from PIL import Image, ImageDraw, ImageFont
import io
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


for event in longpoll.listen():
	if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
		print('\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/')
		print('Сообщение пришло в: ' + str(datetime.strftime(datetime.now(), "%H:%M:%S")))
		print('Текст сообщения: ' + str(event.text))
		print('ID пользователя: ' + str(event.user_id))
		print('===========================================')

		if event.from_chat and not (event.from_me):
			response = event.text.lower()
			text = ''
			fullname = get_user_name(event.user_id)
			print('Кто: '+fullname[0]+' '+fullname[1])
			print('Номер сообщения: '+str(event.message_id))

			if response == 'мем' and event.user_id == 201044121:

				create_test()


			with open("result.json", 'r', encoding='utf-8') as read_message:
				message = json.load(read_message)

			if response == message[0]:
				# Человек получает поинты
				with open("stats.json", 'r', encoding='utf-8') as read_message:
					msg = json.load(read_message)

				check = 0
				for player in msg.keys():
					if player == event.user_id:
						check = 2
					else:
						check = 1

				if check == 1:
					msg.update({event.user_id : 1})
				elif check == 2:
					popit = msg.pop(event.user_id)
					print(popit)
					msg.update({event.user_id : popit+1})

				with open("stats.json", 'w', encoding='utf-8') as write_message:
					json.dump(msg, write_message, ensure_ascii=False, indent=4)

				text = 'Это правильный ответ!\nОжидайте следующий билд...'
				send_chat_reply(10, text, event.message_id)

				get_match_info()
				time.sleep(35)
				create_test()
				

		if event.from_user and not (event.from_me):
			response = event.text.lower()
			text = ''
			fullname = get_user_name(event.user_id)
			print('Кто: '+fullname[0]+' '+fullname[1])
			print('Номер сообщения: '+str(event.message_id))

			if response == 'мем' and event.user_id == 201044121:

				create_test(event.user_id)


			with open("result.json", 'r', encoding='utf-8') as read_message:
				message = json.load(read_message)

			if response == message[0]:
				# Человек получает поинты
				text = 'Это правильный ответ!\nОжидайте следующий билд...'
				send_user_reply(event.user_id, text, event.message_id)

				get_match_info()
				create_test(event.user_id)

				time.sleep(35)
