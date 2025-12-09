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
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_add = types.KeyboardButton('➕ Добавить рецепт')
    btn_list = types.KeyboardButton('📋 Список рецептов')
    btn_view = types.KeyboardButton('👁 Просмотреть рецепт')
    btn_rate = types.KeyboardButton('⭐ Оценить рецепт')
    btn_delete = types.KeyboardButton('🗑 Удалить рецепт')

    markup.row(btn_add, btn_list)
    markup.row(btn_view, btn_rate)
    markup.row(btn_delete)

    bot.send_message(
        message.chat.id,
        "🍳 Привет! Я бот Вкусограф. Я могу помочь управлять твоими рецептами.\n\n"
        "Доступные команды:\n"
        "➕ Добавить рецепт\n"
        "📋 Список рецептов\n"
        "👁 Просмотреть рецепт\n"
        "⭐ Оценить рецепт\n"
        "🗑 Удалить рецепт\n\n"
        "Или используйте команды:\n"
        "/add_recipe - Добавить рецепт\n"
        "/list_recipes - Показать список рецептов\n"
        "/view_recipe - Показать развёрнутый рецепт\n"
        "/rate_recipe - Дать оценку рецепту\n"
        "/delete_recipe - Удалить рецепт",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.text == '➕ Добавить рецепт')
@bot.message_handler(commands=['add_recipe'])
def add_recipe_start(message):
    user_id = message.from_user.id
    user_states[user_id] = {'state': 'add_name'}

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_cancel = types.KeyboardButton('❌ Отмена')
    markup.add(btn_cancel)

    bot.send_message(
        message.chat.id,
        "✍️ Введите название рецепта:",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.text == '❌ Отмена')
def cancel_operation(message):
    user_id = message.from_user.id
    if user_id in user_states:
        del user_states[user_id]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_add = types.KeyboardButton('➕ Добавить рецепт')
    btn_list = types.KeyboardButton('📋 Список рецептов')
    btn_view = types.KeyboardButton('👁 Просмотреть рецепт')
    btn_rate = types.KeyboardButton('⭐ Оценить рецепт')
    btn_delete = types.KeyboardButton('🗑 Удалить рецепт')

    markup.row(btn_add, btn_list)
    markup.row(btn_view, btn_rate)
    markup.row(btn_delete)

    bot.send_message(
        message.chat.id,
        "❌ Операция отменена.",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.from_user.id in user_states and user_states[message.from_user.id][
    'state'] == 'add_name' and message.text != '❌ Отмена')
def add_recipe_name(message):
    user_id = message.from_user.id
    user_states[user_id]['name'] = message.text
    user_states[user_id]['state'] = 'add_description'

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_cancel = types.KeyboardButton('❌ Отмена')
    markup.add(btn_cancel)

    bot.send_message(
        message.chat.id,
        "📝 Введите полное описание рецепта (ингредиенты и инструкции):",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.from_user.id in user_states and user_states[message.from_user.id][
    'state'] == 'add_description')
def add_recipe_description(message):
    user_id = message.from_user.id
    user_states[user_id]['description'] = message.text
    user_states[user_id]['state'] = 'add_tags'

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_cancel = types.KeyboardButton('❌ Отмена')
    markup.add(btn_cancel)

    bot.send_message(
        message.chat.id,
        "🏷 Введите теги через запятую (например: десерт, веган, быстро):",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.from_user.id in user_states and user_states[message.from_user.id][
    'state'] == 'add_tags')
def add_recipe_tags(message):
    user_id = message.from_user.id
    tags = message.text.strip()
    name = user_states[user_id]['name']
    description = user_states[user_id]['description']

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO recipes (user_id, name, description, tags)
        VALUES (?, ?, ?, ?)
    ''', (user_id, name, description, tags))
    recipe_id = cursor.lastrowid
    conn.commit()
    conn.close()

    del user_states[user_id]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_add = types.KeyboardButton('➕ Добавить рецепт')
    btn_list = types.KeyboardButton('📋 Список рецептов')
    btn_view = types.KeyboardButton('👁 Просмотреть рецепт')
    btn_rate = types.KeyboardButton('⭐ Оценить рецепт')
    btn_delete = types.KeyboardButton('🗑 Удалить рецепт')

    markup.row(btn_add, btn_list)
    markup.row(btn_view, btn_rate)
    markup.row(btn_delete)

    bot.send_message(
        message.chat.id,
        f"✅ Рецепт '{name}' добавлен! ID: {recipe_id}",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.text == '📋 Список рецептов')
@bot.message_handler(commands=['list_recipes'])
def list_recipes(message):
    user_id = message.from_user.id
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, rating, tags FROM recipes WHERE user_id = ?', (user_id,))
    recipes = cursor.fetchall()
    conn.close()

    if not recipes:
        bot.send_message(message.chat.id, "📭 У вас пока нет рецептов.")
        return

    response = "📚 Ваши рецепты:\n\n"
    for rec in recipes:
        rating_stars = '⭐' * rec[2] + '☆' * (5 - rec[2]) if rec[2] > 0 else 'Нет оценки'
        response += f"🆔 ID: {rec[0]}\n📌 Название: {rec[1]}\n⭐ Оценка: {rating_stars}\n🏷 Теги: {rec[3]}\n{'─' * 30}\n"

    bot.send_message(message.chat.id, response)


@bot.message_handler(func=lambda message: message.text == '👁 Просмотреть рецепт')
@bot.message_handler(commands=['view_recipe'])
def view_recipe_start(message):
    user_id = message.from_user.id

    # Сначала покажем список рецептов для выбора
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM recipes WHERE user_id = ?', (user_id,))
    recipes = cursor.fetchall()
    conn.close()

    if not recipes:
        bot.send_message(message.chat.id, "📭 У вас пока нет рецептов.")
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_cancel = types.KeyboardButton('❌ Отмена')
    markup.add(btn_cancel)

    user_states[user_id] = {'state': 'view_id'}

    recipes_list = "📚 Ваши рецепты:\n"
    for recipe in recipes:
        recipes_list += f"🆔 {recipe[0]} - {recipe[1]}\n"

    bot.send_message(
        message.chat.id,
        f"{recipes_list}\n✏️ Введите ID рецепта для просмотра:",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.from_user.id in user_states and user_states[message.from_user.id][
    'state'] == 'view_id')
def view_recipe(message):
    user_id = message.from_user.id
    try:
        recipe_id = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "❌ Неверный ID. Попробуйте снова.")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT name, description, rating, tags FROM recipes WHERE id = ? AND user_id = ?',
                   (recipe_id, user_id))
    recipe = cursor.fetchone()
    conn.close()

    if not recipe:
        bot.send_message(message.chat.id, "❌ Рецепт не найден.")
    else:
        rating_stars = '⭐' * recipe[2] + '☆' * (5 - recipe[2]) if recipe[2] > 0 else 'Нет оценки'
        response = f"🍽 **{recipe[0]}**\n\n"
        response += f"📝 **Описание:**\n{recipe[1]}\n\n"
        response += f"⭐ **Оценка:** {rating_stars}\n"
        response += f"🏷 **Теги:** {recipe[3]}"

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_add = types.KeyboardButton('➕ Добавить рецепт')
        btn_list = types.KeyboardButton('📋 Список рецептов')
        btn_view = types.KeyboardButton('👁 Просмотреть рецепт')
        btn_rate = types.KeyboardButton('⭐ Оценить рецепт')
        btn_delete = types.KeyboardButton('🗑 Удалить рецепт')

        markup.row(btn_add, btn_list)
        markup.row(btn_view, btn_rate)
        markup.row(btn_delete)

        bot.send_message(message.chat.id, response, parse_mode='Markdown', reply_markup=markup)

    del user_states[user_id]


@bot.message_handler(func=lambda message: message.text == '⭐ Оценить рецепт')
@bot.message_handler(commands=['rate_recipe'])
def rate_recipe_start(message):
    user_id = message.from_user.id

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM recipes WHERE user_id = ?', (user_id,))
    recipes = cursor.fetchall()
    conn.close()

    if not recipes:
        bot.send_message(message.chat.id, "📭 У вас пока нет рецептов.")
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_cancel = types.KeyboardButton('❌ Отмена')
    markup.add(btn_cancel)

    user_states[user_id] = {'state': 'rate_id'}

    recipes_list = "📚 Ваши рецепты:\n"
    for recipe in recipes:
        recipes_list += f"🆔 {recipe[0]} - {recipe[1]}\n"

    bot.send_message(
        message.chat.id,
        f"{recipes_list}\n✏️ Введите ID рецепта для оценки:",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.from_user.id in user_states and user_states[message.from_user.id][
    'state'] == 'rate_id')
def rate_recipe_id(message):
    user_id = message.from_user.id
    try:
        recipe_id = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "❌ Неверный ID. Попробуйте снова.")
        return

    if not recipe_exists(user_id, recipe_id):
        bot.send_message(message.chat.id, "❌ Рецепт не найден.")
        del user_states[user_id]
        return

    user_states[user_id]['recipe_id'] = recipe_id
    user_states[user_id]['state'] = 'rate_value'

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
    btn1 = types.KeyboardButton('1')
    btn2 = types.KeyboardButton('2')
    btn3 = types.KeyboardButton('3')
    btn4 = types.KeyboardButton('4')
    btn5 = types.KeyboardButton('5')
    btn_cancel = types.KeyboardButton('❌ Отмена')
    markup.row(btn1, btn2, btn3, btn4, btn5)
    markup.row(btn_cancel)

    bot.send_message(
        message.chat.id,
        "⭐ Введите оценку от 1 до 5:",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.from_user.id in user_states and user_states[message.from_user.id][
    'state'] == 'rate_value')
def rate_recipe_value(message):
    user_id = message.from_user.id
    try:
        rating = int(message.text)
        if not 1 <= rating <= 5:
            raise ValueError
    except ValueError:
        bot.send_message(message.chat.id, "❌ Неверная оценка. Должна быть от 1 до 5.")
        return

    recipe_id = user_states[user_id]['recipe_id']

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('UPDATE recipes SET rating = ? WHERE id = ? AND user_id = ?', (rating, recipe_id, user_id))
    conn.commit()
    conn.close()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_add = types.KeyboardButton('➕ Добавить рецепт')
    btn_list = types.KeyboardButton('📋 Список рецептов')
    btn_view = types.KeyboardButton('👁 Просмотреть рецепт')
    btn_rate = types.KeyboardButton('⭐ Оценить рецепт')
    btn_delete = types.KeyboardButton('🗑 Удалить рецепт')

    markup.row(btn_add, btn_list)
    markup.row(btn_view, btn_rate)
    markup.row(btn_delete)

    bot.send_message(
        message.chat.id,
        f"✅ Оценка {rating} ⭐ установлена для рецепта ID {recipe_id}.",
        reply_markup=markup
    )
    del user_states[user_id]


@bot.message_handler(func=lambda message: message.text == '🗑 Удалить рецепт')
@bot.message_handler(commands=['delete_recipe'])
def delete_recipe_start(message):
    user_id = message.from_user.id

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM recipes WHERE user_id = ?', (user_id,))
    recipes = cursor.fetchall()
    conn.close()

    if not recipes:
        bot.send_message(message.chat.id, "📭 У вас пока нет рецептов.")
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_cancel = types.KeyboardButton('❌ Отмена')
    markup.add(btn_cancel)

    user_states[user_id] = {'state': 'delete_id'}

    recipes_list = "📚 Ваши рецепты:\n"
    for recipe in recipes:
        recipes_list += f"🆔 {recipe[0]} - {recipe[1]}\n"

    bot.send_message(
        message.chat.id,
        f"{recipes_list}\n⚠️ Введите ID рецепта для удаления:",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.from_user.id in user_states and user_states[message.from_user.id][
    'state'] == 'delete_id')
def delete_recipe_confirm(message):
    user_id = message.from_user.id
    try:
        recipe_id = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "❌ Неверный ID. Попробуйте снова.")
        return

    if not recipe_exists(user_id, recipe_id):
        bot.send_message(message.chat.id, "❌ Рецепт не найден.")
        del user_states[user_id]
        return

    # Получаем название рецепта для подтверждения
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM recipes WHERE id = ? AND user_id = ?', (recipe_id, user_id))
    recipe_name = cursor.fetchone()[0]
    conn.close()

    user_states[user_id]['recipe_id'] = recipe_id
    user_states[user_id]['state'] = 'delete_confirm'
    user_states[user_id]['recipe_name'] = recipe_name

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_yes = types.KeyboardButton('✅ Да, удалить')
    btn_no = types.KeyboardButton('❌ Нет, отменить')
    markup.row(btn_yes, btn_no)

    bot.send_message(
        message.chat.id,
        f"⚠️ Вы уверены, что хотите удалить рецепт:\n\n"
        f"📌 **{recipe_name}**\n"
        f"🆔 ID: {recipe_id}\n\n"
        f"Это действие нельзя отменить!",
        reply_markup=markup,
        parse_mode='Markdown'
    )


@bot.message_handler(func=lambda message: message.from_user.id in user_states and user_states[message.from_user.id][
    'state'] == 'delete_confirm')
def delete_recipe_execute(message):
    user_id = message.from_user.id

    if message.text == 'Да' or message.text == 'да':
        recipe_id = user_states[user_id]['recipe_id']
        recipe_name = user_states[user_id]['recipe_name']

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM recipes WHERE id = ? AND user_id = ?', (recipe_id, user_id))
        conn.commit()
        conn.close()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_add = types.KeyboardButton('➕ Добавить рецепт')
        btn_list = types.KeyboardButton('📋 Список рецептов')
        btn_view = types.KeyboardButton('👁 Просмотреть рецепт')
        btn_rate = types.KeyboardButton('⭐ Оценить рецепт')
        btn_delete = types.KeyboardButton('🗑 Удалить рецепт')

        markup.row(btn_add, btn_list)
        markup.row(btn_view, btn_rate)
        markup.row(btn_delete)

        bot.send_message(
            message.chat.id,
            f"🗑 Рецепт '{recipe_name}' (ID: {recipe_id}) успешно удален!",
            reply_markup=markup
        )
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_add = types.KeyboardButton('➕ Добавить рецепт')
        btn_list = types.KeyboardButton('📋 Список рецептов')
        btn_view = types.KeyboardButton('👁 Просмотреть рецепт')
        btn_rate = types.KeyboardButton('⭐ Оценить рецепт')
        btn_delete = types.KeyboardButton('🗑 Удалить рецепт')

        markup.row(btn_add, btn_list)
        markup.row(btn_view, btn_rate)
        markup.row(btn_delete)

        bot.send_message(
            message.chat.id,
            "✅ Удаление отменено.",
            reply_markup=markup
        )

    del user_states[user_id]


def recipe_exists(user_id, recipe_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM recipes WHERE id = ? AND user_id = ?', (recipe_id, user_id))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    # Если сообщение не обработано другими хэндлерами
    if message.text not in ['➕ Добавить рецепт', '📋 Список рецептов', '👁 Просмотреть рецепт',
                            '⭐ Оценить рецепт', '🗑 Удалить рецепт', '❌ Отмена']:
        # Проверяем, не находится ли пользователь в процессе диалога
        if message.from_user.id not in user_states:
            bot.send_message(
                message.chat.id,
                "🤔 Не понял вашу команду. Используйте кнопки ниже или команды из /start"
            )


# Запуск бота
if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)