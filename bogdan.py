import vk_api
from vk_api.upload import VkUpload
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType

token = '93f1723b61b66da0a90236b27b0015ad7a57ad49c79d383db875ffbf77b91c058b3cd51b9d8ef8f0a6157'


import time


vk_session = vk_api.VkApi(token=token)

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

def send_chat(chat, msg, attachment=''):
	vk_session.method('messages.send',
		{
		'chat_id': chat,
		'message': msg,
		'random_id': 0,
		'attachment': attachment
		}
	)
send_chat(10, 'Работаем')
txt = 325
time.sleep(70700)

while True:
	try:
		text = 'Может быть Богдан вернётся через: ' + str(txt) + ' дней.'
		send_chat(10, text)
		txt -= 1
		time.sleep(86 400)
		time.sleep(30)
	except requests.exceptions.ReadTimeout:
		print("\n Переподключение к серверам ВК \n")
		time.sleep(3)