import telebot
import time

class Castle:
    def __init__(self, walls):
        self.walls = walls

    def get_walls(self):
        return self.walls

    def upgrade_walls(self, level):
        self.walls += level

    def damage(self, level):
        self.walls -= level

class Enemy:
    def __init__(self, level, health):
        self.level = level
        self.health = health

    def attack(self, target):
        target.damage(self.level)

class Guard:
    def __init__(self, strength):
        self.strength = strength

    def protect(self, target):
        target.upgrade_walls(self.strength)

class Game:
    def __init__(self, castle):
        self.castle = castle
        self.enemies = []

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def start_wave(self):
        for enemy in self.enemies:
            enemy.attack(castle)
            if castle.get_walls() <= 0:
                return "Game Over!"
            time.sleep(1)  # Задержка для реального времени игры
        return "Wave cleared!"

# Создание бота
bot = telebot.TeleBot('Token')

# Создание замка, врагов, стражников и игры
castle = Castle(100)
enemy1 = Enemy(10, 50)
enemy2 = Enemy(15, 75)
guard1 = Guard(10)
game = Game(castle)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_game(message):
    bot.reply_to(message, "Добро пожаловать в игру Защита башни!")

# Обработчик команды /wave
@bot.message_handler(commands=['wave'])
def start_wave(message):
    game.add_enemy(enemy1)
    game.add_enemy(enemy2)
    result = game.start_wave()
    bot.reply_to(message, result)

# Запуск обработчика сообщений
bot.polling()
