import telebot

# ======= Telegram Chat BOT
TOKEN = 'TOKEN'
bot = telebot.TeleBot(token=TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,'Hola soy ChatChato!, el intermediario de tus conversaciones!')

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message,'Para ver mis comandos, escribe /help')

@bot.message_handler(commands=['intercambio'])
def send_menu(message):
    bot.reply_to(message,'Menu de intercambio, escribe /menu')

@bot.message_handler(commands=['menu'])
def send_menu(message):
    bot.reply_to(message,'¿Qué material quieres intercambiar?')
    

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)

if __name__ == '__main__':
    bot.polling(none_stop=True)