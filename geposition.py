import requests
import time
import json

TOKEN = '7680395003:AAFDsDd1KzrREdG-529OUIiRw2xqz2afwx0' #Это токен конкретного нашего бота
URL = f'https://api.telegram.org/bot'  # Это просто ссылочка 

#создание кнопок
def reply_keyboard(chat_id, text):
    reply_markup ={ "keyboard": [["Привет"], [{"request_location":True, "text":"Где я нахожусь"}], ["Отправить другую геопозицию"]], "resize_keyboard": True, "one_time_keyboard": True}
    #keyboard - строки с кнопками, в первой строке кнопка привет, во второй где я нахожусь, в третьей отправить другую геопизацию
    #request_location автоматически отправляет текущую гео + приходит запрос  конфиденциальности 
    #после третьей кнопки только приходит соо, но интерфейс выбора места на карте не открвается, я пока не придумала, как это сделать
    #resize_keyboard - клавиатура автоматтически подстраивается под размер кнопок
    #one_time_keyboard - клавиатура скрыта после нажатия на одну из кнопок
    data = {'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps(reply_markup)}
    #словарь данных для отправки соо
    requests.post(f'{URL}{TOKEN}/sendMessage', data=data)
    #запрос к api telegram

#функция для обновлений, пришло ли что-то новое в бот
def get_updates(offset=0):
    #offset - то, с чего считаем сообщения новыми, изначально 0, потом обновляется каждый раз
    result = requests.get(f'{URL}{TOKEN}/getUpdates?offset={offset}').json()
    #здесь обращение к методу getUpdates
    return result['result']

#функция для отправки соо от бота
def send_message(chat_id, text):
    requests.get(f'{URL}{TOKEN}/sendMessage?chat_id={chat_id}&text={text}')

#функция для проверки, какое соо пришло 
def check_message(chat_id, message):
    #отвечаем, если привет или hello
    if message.lower() in ['привет']:
        send_message(chat_id, 'Привет, мяу')
    if message.lower()=='отправить другую геопозицию':
        send_message(chat_id, 'Жду геопозицию')
    #отвечаем на другое текстовое соо и выкидываем кнопки снова
    else:
        reply_keyboard(chat_id, 'Я не понимаю тебя :(')
        #надо будет придумать что-то со стартом

#функция для получения адреса по коордианатам
def geocoder(latitude, longitude):
    token = 'pk.c198157a80eda06853578215b58c41d1' #мой токен на каком-то сайте, который отлично всё это делает сам
    headers = {"Accept-Language": "ru"} 
    address = requests.get(f'https://eu1.locationiq.com/v1/reverse.php?key={token}&lat={latitude}&lon={longitude}&format=json', headers=headers).json()
    #кидаем запрос тому сайту по токину и координатам и записываем это в адрес
    return f'Твое местоположение: {address.get("display_name")}'
    #берем конкретно display_name из адреса, потому что там и координаты есть, например
    #функция возвращает строку, мы потом ниже её отправим как сообщение

def run():
    update_id = 0
_updates = get_updates()  # Получаем обновления
if _updates:  # Проверяем, есть ли обновления
    update_id = _updates[-1]['update_id']  # Сохраняем ID последнего обновления
    while True:
        time.sleep(2)
        messages = get_updates(update_id) # Получаем обновления
        for message in messages:
            # Если в обновлении есть ID больше чем ID последнего сообщения, значит пришло новое сообщение
            if update_id < message['update_id']:
                update_id = message['update_id']# Сохраняем ID последнего отправленного сообщения боту
                user_message = message['message'].get('text') # Определяем, что за соо пришло
                if user_message: # Проверим, есть ли текст в сообщении -не пустой ли он
                    check_message(message['message']['chat']['id'], user_message) # Отвечаем
                user_location = message['message'].get('location') #Определяем, что за локация пришла
                if user_location: # Проверим, если ли location в сообщении - не пустая ли она
                    latitude = user_location['latitude']
                    longitude = user_location['longitude']
                    send_message(message['message']['chat']['id'], geocoder(latitude, longitude))

if __name__ == '__main__':
    run()