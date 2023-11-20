import discord
import random

# создаем клиент discord
client = discord.Client()

# функция для выбора случайного пользователя
'''определяется функция whowin(), которая выбирает случайного пользователя из всех 
онлайн-участников сервера. Мы используем клиент discord для получения списка всех участников 
и выбираем из них только тех, кто находится в сети. 
После этого выбираем случайного победителя с помощью функции random.choice().'''

def whowin():
    online_users = [member for member in client.get_all_members() if member.status == discord.Status.online]
    winner = random.choice(online_users)
    return winner

# обработчик события подключения к серверу
'''Мы также определяем обработчик события onready(), который выполняется при подключении бота к серверу,
 и обработчик команды onmessage(), который реагирует на сообщения, начинающиеся с "!choosewinner" и проверяет, 
 имеет ли отправитель роль "администратор". Если условие выполняется, бот вызывает функцию whowin(),
 чтобы выбрать победителя, и отправляет сообщение с упоминанием победителя на канал. '''

@client.event
async def on_ready():
    print('Бот подключился к серверу')

# обработчик команды для выбора победителя
@client.event
async def on_message(message):
    if message.content.startswith('!choosewinner') and "администратор" in [role.name for role in message.author.roles]:
        winner = whowin()
        await message.channel.send(f'Победитель лотереи - {winner.mention}')

# запускаем бота
client.run('ваш_токен_бота')
