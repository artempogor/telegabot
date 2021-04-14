import telebot
import configs
from bank import valut
from telebot import types
#ДЛЯ ПОГОДЫ
from pyowm import OWM
from pyowm.commons.enums import SubscriptionTypeEnum
from pyowm.utils.measurables import kelvin_to_celsius
config = {
    'subscription_type': SubscriptionTypeEnum.FREE,
    'language': 'ru',
    'connection': {
        'use_ssl': True,
        'verify_ssl_certs': True,
        'use_proxy': False,
        'timeout_secs': 5
    },
    'proxies': {
        'http': 'http://user:pass@host:port',
        'https': 'socks5://user:pass@host:port'
    }
}
owm = OWM('0e2fb7ff25bb51220ee47248e5c5884c', config=config)
bot = telebot.TeleBot(configs.TOKEN)
@bot.message_handler(commands = ['start'])
def welcome(message):
	sti = open('stickers/Hi.webp', 'rb')
	bot.send_sticker(message.chat.id, sti)
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("💱 Курс валют")
	item2 = types.KeyboardButton("🌆 Новости")
	item3 = types.KeyboardButton("⛅ Погода")
	markup.add(item1, item2)
	markup.add(item3)

	bot.send_message(message.chat.id, "Привет!, {0.first_name}!\n Я - <b>{1.first_name}</b>, и я буду предоставлять тебе актуальную информацию о любимом городе😉".format(message.from_user,bot.get_me()),parse_mode='html', reply_markup=markup)
@bot.message_handler(content_types=["text"])
def lalala(message):
    string = ''
    if message.chat.type =='private':
        if message.text == '💱 Курс валют':
            bot.send_message(message.chat.id,valut(string))
        elif message.text == '⛅ Погода':
            keyboard = types.InlineKeyboardMarkup()
            item11 = types.InlineKeyboardButton("Донецк",callback_data = 'Донецк')
            item22 = types.InlineKeyboardButton("Горловка",callback_data = 'Горловка')
            keyboard.add(item11,item22)
            item33 = types.InlineKeyboardButton("Макеевка",callback_data = 'Макеевка')
            item44 = types.InlineKeyboardButton("Харцысзк",callback_data = 'Харцызск')
            keyboard.add(item33,item44)

            bot.send_message(message.chat.id,"В каком городе интересует погода?", reply_markup=keyboard)
        elif message.text == '🌆 Новости':
            bot.send_message(message.chat.id, '1️⃣убили Жака Фреско\n2️⃣Анна Серёженко <b>лучшая</b> девчуля\n3️⃣Дмитрий Овчинников <b>пиздатый</b> мужик',parse_mode='html')
        else:
            bot.send_message(message.chat.id,"Ты случайно не Иванченко?я тебя не понимаю 😭")

@bot.callback_query_handler(func = lambda call: call.data in ['Горловка', 'Донецк','Макеевка','Харцызск'])
def callback_inline(call):
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(call.data)
        w = observation.weather
        detailed_status = observation.weather.detailed_status
        answer = "В городе " +call.data+ " сейчас : " + str(kelvin_to_celsius(w.temp['temp'])) + " градусов по цельсию, " + detailed_status +".\n"
        if int(kelvin_to_celsius(w.temp['temp']))> 30:
            answer+="Cлишком жарко для прогулок 🥵"
        elif int(kelvin_to_celsius(w.temp['temp']))< 25:
            answer+="Можно и прогулятся в такую погоду 😎"
        try:
            if call.message:
               if call.data=='Горловка':
                bot.send_message(call.message.chat.id,answer)
               elif call.data == 'Донецк':
                bot.send_message(call.message.chat.id, answer)
               elif call.data == 'Макеевка':
                bot.answer_callback_query(call.id,text ='❤❤❤❤')
                bot.send_message(call.message.chat.id,answer)
               #bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=None)
               elif call.data == 'Харцызск':
                bot.send_message(call.message.chat.id,answer)
                bot.answer_callback_query(call.id,text ='💩💩💩💩')

        except Exception as e:
            print(repr(e))
bot.polling(none_stop=True)
