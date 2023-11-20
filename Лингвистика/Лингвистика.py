
import discord
import random

# создаем клиент discord
client = discord.Client()

# список слов для игры
word_list = ["привет", "мир", "лингвистика", "питон", "игра", "дискорд", "код", "слово", "переворот", "бот"]


# функция для переворачивания слова
def reverse_word(word):
    return word[::-1]


# обработчик события подключения к серверу
@client.event
async def on_ready():
    print('Бот подключился к серверу')


# обработчик команды для игры "Задом наперёд"
@client.event
async def on_message(message):
    if message.content.startswith('!reverse'):
        word = random.choice(word_list)
        await message.channel.send(f'Переверни слово: {word}')

        def check(msg):
            return msg.content.lower() == reverse_word(word).lower() and msg.author == message.author

        try:
            response = await client.wait_for('message', timeout=10.0, check=check)
        except TimeoutError:
            await message.channel.send('Время вышло!')
        else:
            await message.channel.send(f'Правильно, {message.author.mention}! Молодец!')


# запускаем бота
client.run('ваш_токен_бота')