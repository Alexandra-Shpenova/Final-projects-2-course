import telebot
from telebot import types
import sqlite3
import random

class Monster:
    def __init__(self, name, strength):
        self.name = name
        self.strength = strength

class CastleDefense:
    def __init__(self, db_connection):
        self.db  = db
        self.monsters = [
            Monster("Гоблин", 1),
            Monster("Тролль", 2),
            Monster("Дракон", 5)
        ]
        self.walls = 10
        self.guards = 5
    def attack(self):
        monster = random.choice(self.monsters)
        damage = monster.strength
        if self.guards >= damage:
            self.guards -= damage
            result = "Стражники отразили атаку!"
            db = sqlite3.connect('game.db')
            cursor = db.cursor()
            for i in cursor.execute('SELECT * FROM game'):
                print(i)
        else:
            self.walls -= damage - self.guards
            self.guards = 0
            result = "Монстр прорвал оборону и нанес урон стенам замка!"
            db = sqlite3.connect('game.db')
            cursor = db.cursor()
            cursor.execute('UPDATE game SET walls = ?, guards = ? WHERE id = ?', (self.walls, self.guards, 1))
            self.db.commit()
            for i in cursor.execute('SELECT * FROM game'):
                print(i)
        return result

    def repair_walls(self):
        self.walls += 1
        self.update_db()
        return "Стены замка укреплены!"
    def add_guards(self):
        self.guards += 1
        self.update_db()
        return "Стражи добавлены на стены!"

    def update_db(self):
        db = sqlite3.connect('game.db')
        cursor = db.cursor()
        try:
            #cursor = self.db.cursor()
            cursor.execute('UPDATE game SET walls = ?, guards = ? WHERE id = ?', (self.walls, self.guards, 1))
            #self.db.commit()
        finally:
            # Закрытие подключения к базе данных
            for i in cursor.execute('SELECT * FROM game'):
                print(i,'entry')
            db.close()

    def load_game(self):
        db = sqlite3.connect('game.db')
        cursor = db.cursor()
        try:
            cursor.execute('SELECT walls, guards FROM game WHERE id = ?', (1,))
            game_data = cursor.fetchone()
            self.walls = game_data[0]
            self.guards = game_data[1]

            # Выполнение операций с курсором...
        finally:
            # Закрытие подключения к базе данных
            db.close()

TOKEN = '6724021310:AAFVi7wT4MZ6D35PEm93_7p_hm7RlXLkC5k'
bot = telebot.TeleBot(TOKEN)

db = sqlite3.connect('game.db')
cursor = db.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS game (
    id INTEGER PRIMARY KEY,
    walls INTEGER,
    guards INTEGER
)''')
cursor.execute('INSERT OR IGNORE INTO game (id, walls, guards) VALUES (1, 10, 5)')
db.commit()

castle_defense = CastleDefense(db)
castle_defense.load_game()  # Загружаем текущее состояние игры


# Ответ на команду /start
@bot.message_handler(commands=['start'])
def start_game(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add('Атака монстров', 'Укрепить стены', 'Добавить стражников')
    bot.send_message(message.chat.id, "Добро пожаловать в Защиту Замка!", reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def monster_attack(message):
    if message.text == "Атака монстров":
        result = castle_defense.attack()
        bot.send_message(message.chat.id, result)
    if message.text == "Укрепить стены":
        result = castle_defense.repair_walls()
        bot.send_message(message.chat.id, result)
    if message.text == "Добавить стражников":
        result = castle_defense.add_guards()
        bot.send_message(message.chat.id, result)

def check_db_changes():
    db = sqlite3.connect('game.db')
    try:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM game')
        entries = cursor.fetchall()
    finally:
        # Закрытие подключения к базе данных
        db.close()
    for entry in entries:
        print(entry)

if __name__ == '__main__':
    # запустить телеграм бот
    bot.polling(none_stop=True)