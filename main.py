import telebot
import time
from datetime import datetime

import telebot
import time
import os

TOKEN = os.env("BV_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для помощи с дыханием по методу Бутейко. Используйте /breathe для начала упражнения.")

@bot.message_handler(commands=['breathe'])
def breathe(message):
    bot.send_message(message.chat.id, "Начинаем дыхательное упражнение по Бутейко:")
    time.sleep(1)
    
    for i in range(5):  # 5 циклов дыхания
        bot.send_message(message.chat.id, "Вдох (2 секунды)")
        time.sleep(2)
        bot.send_message(message.chat.id, "Задержка дыхания (4 секунды)")
        time.sleep(4)
        bot.send_message(message.chat.id, "Выдох (4 секунды)")
        time.sleep(4)
        
    bot.send_message(message.chat.id, "Упражнение завершено!")
@bot.message_handler(commands=['test'])
def breathing_test(message):
    msg = bot.send_message(message.chat.id, 
        "Тест контрольной паузы по Бутейко:\n\n" +
        "1. Сядьте прямо, расслабьтесь\n" +
        "2. Сделайте спокойный вдох и выдох через нос\n" +
        "3. После выдоха нажмите 'Начать'\n" +
        "4. Задержите дыхание до первого дискомфорта\n" +
        "5. Нажмите 'Стоп' при первом желании вдохнуть", 
        reply_markup=get_test_keyboard())

def get_test_keyboard():
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(text="Начать", callback_data="start_test"),
    )
    return keyboard

@bot.callback_query_handler(func=lambda call: call.data == "start_test")
def start_test(call):
    start_time = datetime.now()
    bot.edit_message_reply_markup(
        call.message.chat.id, 
        call.message.message_id,
        reply_markup=get_stop_keyboard(start_time)
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("stop_test"))
def stop_test(call):
    start_time = datetime.fromtimestamp(float(call.data.split(":")[1]))
    duration = (datetime.now() - start_time).seconds
    
    result = ""
    if duration > 40:
        result = "Отличный результат! У вас здоровое дыхание"
    elif duration > 20:
        result = "Первая стадия нарушения дыхания. Рекомендуются регулярные тренировки"
    elif duration > 10:
        result = "Вторая стадия нарушения дыхания. Необходимы регулярные тренировки"
    else:
        result = "Серьезное нарушение дыхания. Требуется систематическая работа над дыханием"
        
    bot.edit_message_text(
        f"Ваша контрольная пауза: {duration} секунд\n\n{result}",
        call.message.chat.id,
        call.message.message_id
    )

def get_stop_keyboard(start_time):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            text="Стоп",
            callback_data=f"stop_test:{start_time.timestamp()}"
        )
    )
    return keyboard


bot.polling(none_stop=True)


