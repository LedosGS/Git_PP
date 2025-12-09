import telebot
import json
from telebot import types
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage

from config import BOT_TOKEN, DB_NAME
from database import Database
from keyboards import Keyboards

# Инициализация бота с поддержкой состояний
state_storage = StateMemoryStorage()
bot = telebot.TeleBot(BOT_TOKEN, state_storage=state_storage)

# Инициализация базы данных
db = Database(DB_NAME)


# ========== СОСТОЯНИЯ ДЛЯ ДОБАВЛЕНИЯ РЕЦЕПТА ==========
class RecipeStates(StatesGroup):
    waiting_for_title = State()
    waiting_for_ingredients = State()
    waiting_for_steps = State()
    waiting_for_tags = State()


# ========== ОБРАБОТЧИКИ КОМАНД ==========

@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    """Обработчик команд /start и /help"""
    welcome_text = """
🍳 *Добро пожаловать в Вкусограф!*

*Ваш личный кулинарный дневник*

*Основные команды:*
• /start или /help - это меню
• /add - добавить новый рецепт
• /list - список ваших рецептов
• /stats - статистика и аналитика
• /search - поиск по тегам

*Или используйте кнопки ниже:*
    """

    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode='Markdown',
        reply_markup=Keyboards.main_menu()
    )


@bot.message_handler(commands=['add'])
def handle_add(message):
    """Начало добавления рецепта"""
    bot.send_message(
        message.chat.id,
        "📝 *Введите название блюда:*\n\n_Можно использовать эмодзи для наглядности_",
        parse_mode='Markdown',
        reply_markup=Keyboards.cancel_button()
    )
    bot.set_state(message.from_user.id, RecipeStates.waiting_for_title, message.chat.id)


@bot.message_handler(commands=['list'])
def handle_list(message):
    """Показать список рецептов"""
    show_recipe_list(message.chat.id, message.from_user.id)


@bot.message_handler(commands=['stats'])
def handle_stats(message):
    """Показать статистику"""
    show_stats(message.chat.id, message.from_user.id)


@bot.message_handler(commands=['search'])
def handle_search(message):
    """Поиск рецептов по тегу"""
    bot.send_message(
        message.chat.id,
        "🔍 *Введите тег для поиска:*\n\n_Или выберите популярный тег:_",
        parse_mode='Markdown',
        reply_markup=Keyboards.search_tags_buttons()
    )


# ========== ОБРАБОТЧИКИ СООБЩЕНИЙ С КНОПКАМИ ==========

@bot.message_handler(func=lambda message: message.text == "📖 Мои рецепты")
def handle_my_recipes_button(message):
    show_recipe_list(message.chat.id, message.from_user.id)


@bot.message_handler(func=lambda message: message.text == "➕ Добавить рецепт")
def handle_add_button(message):
    handle_add(message)


@bot.message_handler(func=lambda message: message.text == "📊 Статистика")
def handle_stats_button(message):
    show_stats(message.chat.id, message.from_user.id)


@bot.message_handler(func=lambda message: message.text == "🔍 Поиск по тегу")
def handle_search_button(message):
    handle_search(message)


@bot.message_handler(func=lambda message: message.text == "❓ Помощь")
def handle_help_button(message):
    handle_start(message)


# ========== ОБРАБОТЧИКИ СОСТОЯНИЙ ДЛЯ ДОБАВЛЕНИЯ РЕЦЕПТА ==========

@bot.message_handler(state=RecipeStates.waiting_for_title)
def handle_title(message):
    """Обработка названия рецепта"""
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['title'] = message.text

    bot.send_message(
        message.chat.id,
        "🛒 *Опишите ингредиенты:*\n\n_Можно списком, каждый с новой строки_",
        parse_mode='Markdown',
        reply_markup=Keyboards.cancel_button()
    )
    bot.set_state(message.from_user.id, RecipeStates.waiting_for_ingredients, message.chat.id)


@bot.message_handler(state=RecipeStates.waiting_for_ingredients)
def handle_ingredients(message):
    """Обработка ингредиентов"""
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['ingredients'] = message.text

    bot.send_message(
        message.chat.id,
        "👨‍🍳 *Опишите пошаговый процесс приготовления:*",
        parse_mode='Markdown',
        reply_markup=Keyboards.cancel_button()
    )
    bot.set_state(message.from_user.id, RecipeStates.waiting_for_steps, message.chat.id)


@bot.message_handler(state=RecipeStates.waiting_for_steps)
def handle_steps(message):
    """Обработка шагов приготовления"""
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['steps'] = message.text

    bot.send_message(
        message.chat.id,
        "🏷️ *Введите теги через пробел:*\n\n_Например: завтрак быстро диетическое_",
        parse_mode='Markdown',
        reply_markup=Keyboards.cancel_button()
    )
    bot.set_state(message.from_user.id, RecipeStates.waiting_for_tags, message.chat.id)


@bot.message_handler(state=RecipeStates.waiting_for_tags)
def handle_tags(message):
    """Обработка тегов и сохранение рецепта"""
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        recipe_id = db.add_recipe(
            user_id=message.from_user.id,
            title=data['title'],
            ingredients=data['ingredients'],
            steps=data['steps'],
            tags=message.text
        )

    bot.send_message(
        message.chat.id,
        f"✅ *Рецепт \"{data['title']}\" успешно сохранен!*\n\nID: {recipe_id}\n\n_Чтобы посмотреть рецепт, нажмите \"📖 Мои рецепты\"_",
        parse_mode='Markdown',
        reply_markup=Keyboards.main_menu()
    )
    bot.delete_state(message.from_user.id, message.chat.id)


# ========== ОБРАБОТЧИКИ INLINE-КНОПОК ==========

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    """Обработка всех inline-кнопок"""
    try:
        data = json.loads(call.data)
        action = data.get('action')

        if action == 'view_recipe':
            recipe_id = data['recipe_id']
            show_recipe(call.message.chat.id, call.from_user.id, recipe_id)

        elif action == 'rate':
            recipe_id = data['recipe_id']
            rating = data['rating']

            if db.add_rating(recipe_id, call.from_user.id, rating):
                # Обновляем сообщение с рецептом
                show_recipe(call.message.chat.id, call.from_user.id, recipe_id)

                # Отправляем подтверждение
                bot.answer_callback_query(
                    call.id,
                    f"✅ Вы оценили рецепт на {rating}/5 баллов"
                )
            else:
                bot.answer_callback_query(call.id, "❌ Не удалось оценить рецепт")

        elif action == 'list_page':
            page = data['page']
            show_recipe_list(call.message.chat.id, call.from_user.id, page)

        elif action == 'back_to_list':
            show_recipe_list(call.message.chat.id, call.from_user.id)

        elif action == 'add_recipe':
            handle_add(call.message)

        elif action == 'delete_recipe':
            recipe_id = data['recipe_id']
            if db.delete_recipe(recipe_id, call.from_user.id):
                bot.answer_callback_query(call.id, "✅ Рецепт удален")
                show_recipe_list(call.message.chat.id, call.from_user.id)
            else:
                bot.answer_callback_query(call.id, "❌ Не удалось удалить рецепт")

        elif action == 'quick_search':
            tag = data['tag']
            search_and_show_results(call.message.chat.id, call.from_user.id, tag)

        elif action == 'cancel':
            bot.delete_state(call.from_user.id, call.message.chat.id)
            bot.send_message(
                call.message.chat.id,
                "❌ Действие отменено",
                reply_markup=Keyboards.main_menu()
            )
            bot.answer_callback_query(call.id)

    except Exception as e:
        print(f"Error in callback: {e}")
        bot.answer_callback_query(call.id, "❌ Произошла ошибка")


# ========== ПОИСК ПО ТЕГАМ ==========

@bot.message_handler(func=lambda message: True)
def handle_search_query(message):
    """Обработка поискового запроса"""
    if message.text.startswith('#'):
        tag = message.text[1:]  # Убираем решетку
    else:
        tag = message.text

    search_and_show_results(message.chat.id, message.from_user.id, tag)


# ========== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==========

def show_recipe_list(chat_id, user_id, page=0):
    """Показать список рецептов пользователя"""
    recipes = db.get_user_recipes(user_id)

    if not recipes:
        bot.send_message(
            chat_id,
            "📭 *У вас пока нет рецептов*\n\n_Добавьте первый рецепт с помощью кнопки \"➕ Добавить рецепт\"_",
            parse_mode='Markdown',
            reply_markup=Keyboards.main_menu()
        )
        return

    # Формируем текст сообщения
    total = len(recipes)
    start_idx = page * 5 + 1
    end_idx = min((page + 1) * 5, total)

    text = f"📚 *Ваши рецепты* ({total} всего)\n\n"

    for i, recipe in enumerate(recipes[page * 5:(page + 1) * 5], start=1):
        rating_text = f"⭐ {recipe['avg_rating']:.1f}" if recipe['avg_rating'] >= 0 else "⭐ -"
        text += f"{start_idx + i - 1}. {rating_text} *{recipe['title']}*\n"
        if recipe['tags']:
            text += f"   _{recipe['tags']}_\n"
        text += "\n"

    if total > 5:
        text += f"\n_Страница {page + 1} из {((total - 1) // 5) + 1}_"

    # Отправляем сообщение с inline-клавиатурой
    bot.send_message(
        chat_id,
        text,
        parse_mode='Markdown',
        reply_markup=Keyboards.recipe_list_buttons(recipes, page)
    )


def show_recipe(chat_id, user_id, recipe_id):
    """Показать полный рецепт"""
    recipe = db.get_recipe(recipe_id, user_id)

    if not recipe:
        bot.send_message(chat_id, "❌ Рецепт не найден")
        return

    # Формируем текст рецепта
    rating_text = ""
    if recipe['avg_rating'] >= 0:
        rating_text = f"⭐ *{recipe['avg_rating']:.1f}/5* ({recipe['rating_count']} оценок)\n"
    else:
        rating_text = "⭐ *Еще нет оценок*\n"

    text = f"""
🍳 *{recipe['title']}*

{rating_text}
🏷️ *Теги:* {recipe['tags'] or 'нет'}

🛒 *Ингредиенты:*
{recipe['ingredients']}

👨‍🍳 *Приготовление:*
{recipe['steps']}

📅 *Добавлен:* {recipe['created_at'].split()[0]}
"""

    # Отправляем рецепт с кнопками оценки
    bot.send_message(
        chat_id,
        text,
        parse_mode='Markdown',
        reply_markup=Keyboards.rating_buttons(recipe_id)
    )


def show_stats(chat_id, user_id):
    """Показать статистику пользователя"""
    stats = db.get_recipe_stats(user_id)

    # Формируем текст статистики
    text = f"""
📊 *Ваша кулинарная статистика*

• Всего рецептов: *{stats['total_recipes']}*
• Оценено рецептов: *{stats['rated_recipes']}*
• Средний балл: *{stats['avg_rating_all']:.1f}/5*
"""

    # Топ-3 рецепта
    if stats['top_recipes']:
        text += "\n🏆 *Топ рецептов:*\n"
        for i, recipe in enumerate(stats['top_recipes'], 1):
            text += f"{i}. *{recipe['title']}* — ⭐ {recipe['rating']:.1f}\n"

    # Популярные теги
    if stats['popular_tags']:
        text += "\n🔖 *Популярные теги:*\n"
        for tag, count in stats['popular_tags']:
            text += f"• #{tag} — {count} рецепт(ов)\n"

    bot.send_message(
        chat_id,
        text,
        parse_mode='Markdown',
        reply_markup=Keyboards.main_menu()
    )


def search_and_show_results(chat_id, user_id, tag):
    """Поиск и отображение результатов"""
    recipes = db.search_recipes(user_id, tag)

    if not recipes:
        bot.send_message(
            chat_id,
            f"🔍 *По запросу \"{tag}\" ничего не найдено*",
            parse_mode='Markdown',
            reply_markup=Keyboards.main_menu()
        )
        return

    text = f"🔍 *Результаты поиска по тегу \"{tag}\":*\n\n"

    for i, recipe in enumerate(recipes, 1):
        rating_text = f"⭐ {recipe['avg_rating']:.1f}" if recipe['avg_rating'] >= 0 else "⭐ -"
        text += f"{i}. {rating_text} *{recipe['title']}*\n"
        if recipe['tags']:
            text += f"   _{recipe['tags']}_\n"
        text += "\n"

    # Отправляем результаты
    bot.send_message(
        chat_id,
        text,
        parse_mode='Markdown',
        reply_markup=Keyboards.main_menu()
    )


# ========== ЗАПУСК БОТА ==========
if __name__ == "__main__":
    print("Бот 'Вкусограф' запущен...")
    try:
        bot.infinity_polling()
    finally:
        db.close()