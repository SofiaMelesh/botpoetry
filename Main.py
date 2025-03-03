import telebot

#Сончикс
bot = telebot.TeleBot('7680395003:AAFDsDd1KzrREdG-529OUIiRw2xqz2afwx0')
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Этот бот поможет тебе ...")
bot.polling(none_stop=True)
#