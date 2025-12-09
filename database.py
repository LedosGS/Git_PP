import sqlite3
import datetime
from typing import List, Dict, Optional, Tuple


class Database:
    def __init__(self, db_name: str):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Создание таблиц в базе данных"""
        # Таблица рецептов
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                ingredients TEXT NOT NULL,
                steps TEXT NOT NULL,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Таблица оценок
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                rating INTEGER CHECK (rating >= 0 AND rating <= 5),
                rated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
            )
        ''')

        # Индексы для быстрого поиска
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_recipes ON recipes(user_id)')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_recipe_ratings ON ratings(recipe_id)')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_ratings ON ratings(user_id, recipe_id)')

        self.conn.commit()

    # ========== РЕЦЕПТЫ ==========

    def add_recipe(self, user_id: int, title: str, ingredients: str, steps: str, tags: str = "") -> int:
        """Добавление нового рецепта"""
        self.cursor.execute('''
            INSERT INTO recipes (user_id, title, ingredients, steps, tags)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, title, ingredients, steps, tags))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_user_recipes(self, user_id: int) -> List[Dict]:
        """Получение всех рецептов пользователя"""
        self.cursor.execute('''
            SELECT r.id, r.title, r.tags, 
                   COALESCE(AVG(rat.rating), -1) as avg_rating,
                   COUNT(rat.id) as rating_count
            FROM recipes r
            LEFT JOIN ratings rat ON r.id = rat.recipe_id
            WHERE r.user_id = ?
            GROUP BY r.id
            ORDER BY r.created_at DESC
        ''', (user_id,))

        columns = [col[0] for col in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

    def get_recipe(self, recipe_id: int, user_id: int) -> Optional[Dict]:
        """Получение конкретного рецепта с проверкой владельца"""
        self.cursor.execute('''
            SELECT r.*, 
                   COALESCE(AVG(rat.rating), -1) as avg_rating,
                   COUNT(rat.id) as rating_count
            FROM recipes r
            LEFT JOIN ratings rat ON r.id = rat.recipe_id
            WHERE r.id = ? AND r.user_id = ?
            GROUP BY r.id
        ''', (recipe_id, user_id))

        row = self.cursor.fetchone()
        if row:
            columns = [col[0] for col in self.cursor.description]
            return dict(zip(columns, row))
        return None

    def search_recipes(self, user_id: int, tag: str) -> List[Dict]:
        """Поиск рецептов по тегу"""
        self.cursor.execute('''
            SELECT r.id, r.title, r.tags,
                   COALESCE(AVG(rat.rating), -1) as avg_rating,
                   COUNT(rat.id) as rating_count
            FROM recipes r
            LEFT JOIN ratings rat ON r.id = rat.recipe_id
            WHERE r.user_id = ? AND (r.tags LIKE ? OR r.title LIKE ?)
            GROUP BY r.id
            ORDER BY r.created_at DESC
        ''', (user_id, f'%{tag}%', f'%{tag}%'))

        columns = [col[0] for col in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

    def delete_recipe(self, recipe_id: int, user_id: int) -> bool:
        """Удаление рецепта с проверкой владельца"""
        self.cursor.execute('DELETE FROM recipes WHERE id = ? AND user_id = ?', (recipe_id, user_id))
        self.conn.commit()
        return self.cursor.rowcount > 0

    # ========== ОЦЕНКИ ==========

    def add_rating(self, recipe_id: int, user_id: int, rating: int) -> bool:
        """Добавление оценки к рецепту"""
        # Сначала проверяем, что рецепт принадлежит пользователю
        self.cursor.execute('SELECT 1 FROM recipes WHERE id = ? AND user_id = ?', (recipe_id, user_id))
        if not self.cursor.fetchone():
            return False

        # Добавляем оценку
        self.cursor.execute('''
            INSERT INTO ratings (recipe_id, user_id, rating)
            VALUES (?, ?, ?)
        ''', (recipe_id, user_id, rating))
        self.conn.commit()
        return True

    def get_recipe_stats(self, user_id: int) -> Dict:
        """Получение статистики пользователя"""
        # Общая статистика
        self.cursor.execute('''
            SELECT 
                COUNT(DISTINCT r.id) as total_recipes,
                COUNT(DISTINCT rat.recipe_id) as rated_recipes,
                COALESCE(AVG(rat.rating), 0) as avg_rating_all
            FROM recipes r
            LEFT JOIN ratings rat ON r.id = rat.recipe_id
            WHERE r.user_id = ?
        ''', (user_id,))

        stats = dict(zip(['total_recipes', 'rated_recipes', 'avg_rating_all'], self.cursor.fetchone()))

        # Топ-3 рецепта
        self.cursor.execute('''
            SELECT r.id, r.title, AVG(rat.rating) as avg_rating
            FROM recipes r
            JOIN ratings rat ON r.id = rat.recipe_id
            WHERE r.user_id = ?
            GROUP BY r.id
            HAVING COUNT(rat.id) >= 1
            ORDER BY avg_rating DESC
            LIMIT 3
        ''', (user_id,))

        stats['top_recipes'] = [
            {'title': row[1], 'rating': row[2]}
            for row in self.cursor.fetchall()
        ]

        # Популярные теги
        self.cursor.execute('''
            SELECT tags FROM recipes WHERE user_id = ? AND tags IS NOT NULL AND tags != ''
        ''', (user_id,))

        tag_counts = {}
        for row in self.cursor.fetchall():
            for tag in row[0].split():
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

        stats['popular_tags'] = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:5]

        return stats

    def close(self):
        """Закрытие соединения с БД"""
        self.conn.close()