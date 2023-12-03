import telebot
from telebot import types
import random

# Создание бота
bot = telebot.TeleBot('YOUR_TOKEN')

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Магический шар')
    itembtn2 = types.KeyboardButton('Хрустальный шар')
    itembtn3 = types.KeyboardButton('Книга «Гадаем на кофейной гуще»')
    itembtn4 = types.KeyboardButton('Руны')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    bot.send_message(message.chat.id, "Привет! Я магазин эзотерической атрибутики. Выбери категорию товаров:", reply_markup=markup)

# Обработчики кнопок
@bot.message_handler(func=lambda message: message.text == 'Магический шар')
def magic_ball(message):
    msg = bot.reply_to(message, "Задай свой вопрос:")
    bot.register_next_step_handler(msg, magic_ball_answer)

def magic_ball_answer(message):
    replies = ["Да", "Нет", "Возможно", "Скорее всего", "Не уверен", "Спроси позже"]
    bot.send_message(message.chat.id, random.choice(replies))

@bot.message_handler(func=lambda message: message.text == 'Хрустальный шар')
def crystal_ball(message):
    with open('crystal_ball.gif', 'rb') as photo:
        bot.send_document(message.chat.id, photo)

@bot.message_handler(func=lambda message: message.text == 'Книга «Гадаем на кофейной гуще»')
def coffee_grounds_book(message):
    with open('coffee_gounds_book.gif', 'rb') as photo:
        bot.send_document(message.chat.id, photo)

@bot.message_handler(func=lambda message: message.text == 'Руны')
def runes(message):
    bot.send_message(message.chat.id, "Выбери 3 руны...")
    #Тут нужно продолжение

# Запуск обработчика сообщений
bot.polling()