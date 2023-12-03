import telebot
from telebot import types
import sqlite3
import random

TOKEN = '6724021310:AAFVi7wT4MZ6D35PEm93_7p_hm7RlXLkC5k'
bot = telebot.TeleBot(TOKEN)

# Класс для монстра
class Monster:
    def __init__(self, name, strength):
        self.name = name
        self.strength = strength

# Класс для защиты замка
class CastleDefense:
    def __init__(self, db_connection):
        self.db_connection = db_connection
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
        else:
            self.walls -= damage - self.guards
            self.guards = 0
            result = "Монстр прорвал оборону и нанес урон стенам замка!"
        self.update_db()
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
        cursor = self.db_connection.cursor()
        cursor.execute('UPDATE game SET walls = ?, guards = ? WHERE id = ?', (self.walls, self.guards, 1))
        self.db_connection.commit()

    def load_game(self):
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT walls, guards FROM game WHERE id = ?', (1,))
        game_data = cursor.fetchone()
        self.walls = game_data[0]
        self.guards = game_data[1]

# Создание базы данных и таблицы game, если они еще не созданы
db_connection = sqlite3.connect('game.db')
cursor = db_connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS game (
    id INTEGER PRIMARY KEY,
    walls INTEGER,
    guards INTEGER
)''')
cursor.execute('INSERT OR IGNORE INTO game (id, walls, guards) VALUES (1, 10, 5)')
db_connection.commit()

# Объект игры
castle_defense = CastleDefense(db_connection)
castle_defense.load_game()  # Загружаем текущее состояние игры

# Ответ на команду /start
@bot.message_handler(commands=['start'])
def start_game(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add('Атака монстров', 'Укрепить стены', 'Добавить стражников')
    bot.send_message(message.chat.id, "Добро пожаловать в Защиту Замка!", reply_markup=keyboard)

# Ответ на кнопку "Атака монстров"
@bot.message_handler(func=lambda message: message.text == "Атака монстров")
def monster_attack(message):
    result = castle_defense.attack()
    bot.send_message(message.chat.id, result)

# Ответ на кнопку "Укрепить стены"
@bot.message_handler(func=lambda message: message.text == "Укрепить стены")
def repair_walls(message):
    result = castle_defense.repair_walls()
    bot.send_message(message.chat.id, result)

# Ответ на кнопку "Добавить стражников"
@bot.message_handler(func=lambda message: message.text == "Добавить стражников")
def add_guards(message):
    result = castle_defense.add_guards()
    bot.send_message(message.chat.id, result)

# Проверка изменений в БД и вывод в консоль
def check_db_changes():
    cursor = db_connection.cursor()
    cursor.execute('SELECT * FROM game')
    entries = cursor.fetchall()
    for entry in entries:
        print(entry)

if __name__ == '__main__':
    # запустить телеграм бот
    bot.polling(none_stop=True)