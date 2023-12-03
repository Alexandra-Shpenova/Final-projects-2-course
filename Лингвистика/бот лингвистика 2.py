import discord
import random
from discord.ext import commands, tasks

TOKEN = 'MTE0MTI2NjkwMzAxMzI4MTkwMg.GA574U.6acz4rQDZv48hDhRxunbm8IizPbUCzTndaCOsU'

bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())
words = ['хлеб','кот', 'ток']
@bot.event
async def on_ready():
    print(f'Бот {bot.user.name} готов')
@bot.event
async def on_message(message):
    if message.content.startswith('!reverse'):
        await message.channel.send(f'{random.choice(words)}')
    for x in words:
        if x in message.content.lower():
            await message.channel.send('Умница')
            print((message.author ))



bot.run(TOKEN)