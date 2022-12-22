import telebot
from config import keys, TOKEN
from extensions import ConversionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем форммате:\n\
<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n\
Пример:\n\
доллар евро\n\
биткойн доллар 5\n\
jpy usd 100\n\
Увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) > 3:
            raise ConversionException('Слишком много параметров.')
        elif len(values) < 2 :
            raise ConversionException('Слишком мало параметров.')
        elif len(values) == 2:
            values.append(1)
        quote, base, amount = values
        if str(quote).isdigit():
            amount, quote, base = values
            # А ведь удобнее написать 7 евро доллар, чем евро доллар 7
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConversionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {total_base}'
        bot.reply_to(message, text) # Выводится как ответ с цитатой вопроса
        #bot.send_message(message.chat.id, text) # Либо выводится как отдельная фраза

# Обрабатывается все документы и аудиозаписи
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    pass

@bot.message_handler(content_types=['photo', ])
def say_lmao(message: telebot.types.Message):
    bot.reply_to(message, 'Nice meme XDD')

bot.polling(none_stop=True)