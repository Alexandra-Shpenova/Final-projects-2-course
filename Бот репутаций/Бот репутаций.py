import discord
from discord.ext import commands
import sqlite3

# Подключение к базе данных SQLite
conn = sqlite3.connect('reputation.db')
c = conn.cursor()

#Создадим таблицу
c.execute('''CREATE TABLE IF NOT EXISTS users(
    user_id INT,
    reputation INT
)''')

# Инициализация клиента Discord
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# Обработка события загрузки бота
@bot.event
async def on_ready():
    print(f'Бот {bot.user} запущен')

# Обработка команды plus
@bot.command(name='plus', help='Увеличить рейтинг пользователя')
async def plus_reputation(ctx, member: discord.Member):
    c.execute("SELECT reputation FROM users WHERE user_id=?", (member.id,))
    reputation = c.fetchone()
    if reputation is not None:
        new_reputation = reputation[0] + 1
        c.execute("UPDATE users SET reputation=? WHERE user_id=?", (new_reputation, member.id))
    else:
        c.execute("INSERT INTO users (user_id, reputation) VALUES (?, 1)", (member.id,))
        new_reputation = 1
    conn.commit()
    await update_role(ctx, member, new_reputation)

# Обработка команды minus
@bot.command(name='minus', help='Уменьшить рейтинг пользователя')
async def minus_reputation(ctx, member: discord.Member):
    c.execute("SELECT reputation FROM users WHERE user_id=?", (member.id,))
    reputation = c.fetchone()
    if reputation is not None:
        new_reputation = max(0, reputation[0] - 1)
        c.execute("UPDATE users SET reputation=? WHERE user_id=?", (new_reputation, member.id))
        conn.commit()
        await update_role(ctx, member, new_reputation)


async def update_role(ctx, member, reputation):
    role = None
    if reputation < 50:
        role = discord.utils.get(ctx.guild.roles, name='новичок')
    elif reputation < 150:
        role = discord.utils.get(ctx.guild.roles, name='рекрут')
    elif reputation < 300:
        role = discord.utils.get(ctx.guild.roles, name='бывалый')
    else:
        role = discord.utils.get(ctx.guild.roles, name='гуру')

    if role:
        await member.add_roles(role, reason="Изменение репутации")
        await ctx.send(f'Роль пользователя {member.mention} обновлена')
    else:
        await ctx.send(f'Для пользователя {member.mention} не найдена установленная роль')

# Запуск бота
bot.run('ваш_токен_бота')