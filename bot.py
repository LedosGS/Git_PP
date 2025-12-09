import telebot
from telebot import types
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)


DB_FILE = 'recipes.db'


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            rating INTEGER DEFAULT 0,
            tags TEXT DEFAULT ''
        )
    ''')
    conn.commit()
    conn.close()

init_db()
user_states = {}


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот Вкусограф. Я могу помочь управлять твоими рецептами.\n"
                                      "Команды:\n"
                                      "/add_recipe - Добавить рецепт\n"
                                      "/list_recipes - Показать список рецептов\n"
                                      "/view_recipe - Показать развёрнутый рецепт\n"
                                      "/rate_recipe - Дать оценку рецепту")


@bot.message_handler(commands=['add_recipe'])
def add_recipe_start(message):
    user_id = message.from_user.id
    user_states[user_id] = {'state': 'add_name'}
    bot.send_message(message.chat.id, "Введите название рецепта:")


@bot.message_handler(func=lambda message: message.from_user.id in user_states and user_states[message.from_user.id]['state'] == 'add_name')
def add_recipe_name(message):
    user_id = message.from_user.id
    user_states[user_id]['name'] = message.text
    user_states[user_id]['state'] = 'add_description'
    bot.send_message(message.chat.id, "Введите полное описание рецепта (ингредиенты и инструкции):")

@bot.message_handler(func=lambda message: message.from_user.id in user_states and user_states[message.from_user.id]['state'] == 'add_description')
def add_recipe_description(message):
    user_id = message.from_user.id
    user_states[user_id]['description'] = message.text
    user_states[user_id]['state'] = 'add_tags'
    bot.send_message(message.chat.id, "Введите теги через запятую (например: десерт, веган):")

@bot.message_handler(func=lambda message: message.from_user.id in user_states and user_states[message.from_user.id]['state'] == 'add_tags')
def add_recipe_tags(message):
    user_id = message.from_user.id
    tags = message.text.strip()
    name = user_states[user_id]['name']
    description = user_states[user_id]['description']

    # Сохраняем в БД
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO recipes (user_id, name, description, tags)
        VALUES (?, ?, ?, ?)
    ''', (user_id, name, description, tags))
    conn.commit()
    conn.close()

    del user_states[user_id]
    bot.send_message(message.chat.id, f"Рецепт '{name}' добавлен!")

@bot.message_handler(commands=['list_recipes'])
def list_recipes(message):
    user_id = message.from_user.id
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, rating, tags FROM recipes WHERE user_id = ?', (user_id,))
    recipes = cursor.fetchall()
    conn.close()

    if not recipes:
        bot.send_message(message.chat.id, "У вас нет рецептов.")
        return

    response = "Ваши рецепты:\n"
    for rec in recipes:
        response += f"ID: {rec[0]} | {rec[1]} | Оценка: {rec[2]} | Теги: {rec[3]}\n"
    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=['view_recipe'])
def view_recipe_start(message):
    user_id = message.from_user.id
    user_states[user_id] = {'state': 'view_id'}
    bot.send_message(message.chat.id, "Введите ID рецепта для просмотра:")


@bot.message_handler(func=lambda message: message.from_user.id in user_states and user_states[message.from_user.id]['state'] == 'view_id')
def view_recipe(message):
    user_id = message.from_user.id
    try:
        recipe_id = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Неверный ID. Попробуйте снова.")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT name, description, rating, tags FROM recipes WHERE id = ? AND user_id = ?', (recipe_id, user_id))
    recipe = cursor.fetchone()
    conn.close()

    if not recipe:
        bot.send_message(message.chat.id, "Рецепт не найден.")
    else:
        response = f"Название: {recipe[0]}\nОписание: {recipe[1]}\nОценка: {recipe[2]}\nТеги: {recipe[3]}"
        bot.send_message(message.chat.id, response)

    del user_states[user_id]

# Команда /rate_recipe - начать оценку рецепта
@bot.message_handler(commands=['rate_recipe'])
def rate_recipe_start(message):
    user_id = message.from_user.id
    user_states[user_id] = {'state': 'rate_id'}
    bot.send_message(message.chat.id, "Введите ID рецепта для оценки:")

# Обработчик для оценки рецепта
@bot.message_handler(func=lambda message: message.from_user.id in user_states and user_states[message.from_user.id]['state'] == 'rate_id')
def rate_recipe_id(message):
    user_id = message.from_user.id
    try:
        recipe_id = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Неверный ID. Попробуйте снова.")
        return

    if not recipe_exists(user_id, recipe_id):
        bot.send_message(message.chat.id, "Рецепт не найден.")
        del user_states[user_id]
        return

    user_states[user_id]['recipe_id'] = recipe_id
    user_states[user_id]['state'] = 'rate_value'
    bot.send_message(message.chat.id, "Введите оценку (от 1 до 5):")

@bot.message_handler(func=lambda message: message.from_user.id in user_states and user_states[message.from_user.id]['state'] == 'rate_value')
def rate_recipe_value(message):
    user_id = message.from_user.id
    try:
        rating = int(message.text)
        if not 1 <= rating <= 5:
            raise ValueError
    except ValueError:
        bot.send_message(message.chat.id, "Неверная оценка. Должна быть от 1 до 5.")
        return

    recipe_id = user_states[user_id]['recipe_id']

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('UPDATE recipes SET rating = ? WHERE id = ? AND user_id = ?', (rating, recipe_id, user_id))
    conn.commit()
    conn.close()

    bot.send_message(message.chat.id, f"Оценка {rating} установлена для рецепта ID {recipe_id}.")
    del user_states[user_id]


def recipe_exists(user_id, recipe_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM recipes WHERE id = ? AND user_id = ?', (recipe_id, user_id))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

if __name__ == '__main__':
    bot.polling(none_stop=True)