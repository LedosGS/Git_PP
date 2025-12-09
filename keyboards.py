from telebot import types
import json


class Keyboards:
    """Класс для создания всех клавиатур бота"""

    @staticmethod
    def main_menu():
        """Основное меню (Reply-клавиатура под строкой ввода)"""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        buttons = [
            types.KeyboardButton("📖 Мои рецепты"),
            types.KeyboardButton("➕ Добавить рецепт"),
            types.KeyboardButton("📊 Статистика"),
            types.KeyboardButton("🔍 Поиск по тегу"),
            types.KeyboardButton("❓ Помощь")
        ]
        markup.add(*buttons)
        return markup

    @staticmethod
    def rating_buttons(recipe_id: int):
        """Кнопки оценки 0-5 (Inline-клавиатура под сообщением)"""
        markup = types.InlineKeyboardMarkup(row_width=6)

        buttons = []
        for i in range(6):  # 0-5
            callback_data = json.dumps({'action': 'rate', 'recipe_id': recipe_id, 'rating': i})
            buttons.append(types.InlineKeyboardButton(str(i), callback_data=callback_data))

        markup.add(*buttons)

        # Кнопка "Просмотреть список"
        markup.add(types.InlineKeyboardButton(
            "📋 К списку рецептов",
            callback_data=json.dumps({'action': 'back_to_list'})
        ))
        return markup

    @staticmethod
    def recipe_list_buttons(recipes: list, page: int = 0, per_page: int = 5):
        """Кнопки для навигации по списку рецептов"""
        markup = types.InlineKeyboardMarkup(row_width=2)

        start_idx = page * per_page
        end_idx = start_idx + per_page

        # Добавляем кнопки для рецептов на текущей странице
        for recipe in recipes[start_idx:end_idx]:
            recipe_id = recipe['id']
            title = recipe['title'][:30] + "..." if len(recipe['title']) > 30 else recipe['title']
            rating = f"⭐ {recipe['avg_rating']:.1f}" if recipe['avg_rating'] >= 0 else "⭐ -"

            callback_data = json.dumps({'action': 'view_recipe', 'recipe_id': recipe_id})
            markup.add(types.InlineKeyboardButton(
                f"{title} ({rating})",
                callback_data=callback_data
            ))

        # Кнопки навигации
        nav_buttons = []
        if page > 0:
            nav_buttons.append(types.InlineKeyboardButton(
                "◀️ Назад",
                callback_data=json.dumps({'action': 'list_page', 'page': page - 1})
            ))

        if end_idx < len(recipes):
            nav_buttons.append(types.InlineKeyboardButton(
                "Вперед ▶️",
                callback_data=json.dumps({'action': 'list_page', 'page': page + 1})
            ))

        if nav_buttons:
            markup.add(*nav_buttons)

        # Кнопка добавления нового рецепта
        markup.add(types.InlineKeyboardButton(
            "➕ Добавить рецепт",
            callback_data=json.dumps({'action': 'add_recipe'})
        ))

        return markup

    @staticmethod
    def recipe_actions(recipe_id: int):
        """Действия с рецептом (удаление, редактирование)"""
        markup = types.InlineKeyboardMarkup(row_width=2)

        markup.add(
            types.InlineKeyboardButton(
                "🗑️ Удалить",
                callback_data=json.dumps({'action': 'delete_recipe', 'recipe_id': recipe_id})
            ),
            types.InlineKeyboardButton(
                "✏️ Редактировать",
                callback_data=json.dumps({'action': 'edit_recipe', 'recipe_id': recipe_id})
            ),
            types.InlineKeyboardButton(
                "📋 К списку",
                callback_data=json.dumps({'action': 'back_to_list'})
            )
        )

        return markup

    @staticmethod
    def cancel_button():
        """Кнопка отмены действия"""
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            "❌ Отмена",
            callback_data=json.dumps({'action': 'cancel'})
        ))
        return markup

    @staticmethod
    def search_tags_buttons():
        """Быстрый поиск по популярным тегам"""
        markup = types.InlineKeyboardMarkup(row_width=3)

        popular_tags = ["завтрак", "ужин", "десерт", "суп", "салат", "выпечка",
                        "быстро", "диетическое", "праздничное", "вегетарианское"]

        buttons = []
        for tag in popular_tags:
            buttons.append(types.InlineKeyboardButton(
                f"#{tag}",
                callback_data=json.dumps({'action': 'quick_search', 'tag': tag})
            ))

        # Добавляем кнопки по 3 в ряд
        for i in range(0, len(buttons), 3):
            markup.add(*buttons[i:i + 3])

        return markup