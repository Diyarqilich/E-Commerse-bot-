import asyncpg
from config import config


class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        try:
            self.pool = await asyncpg.create_pool(
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                database=config.DB_NAME,
                host=config.DB_HOST,
                port=config.DB_PORT,
                min_size=1,
                max_size=10
            )
            print("База данных подключена")
        except Exception as e:
            print(f"Ошибка подключения к базе: {e}")

    async def close(self):
        if self.pool:
            await self.pool.close()
            print("База данных закрыта")

    async def add_user(self, telegram_id, name, surename, age, phone):
        query = """
        INSERT INTO users (telegram_id, name, surename, age, phone)
        VALUES ($1, $2, $3, $4, $5)
        ON CONFLICT (telegram_id) DO NOTHING;
        """
        try:
            await self.pool.execute(query, telegram_id, name, surename, int(age), phone)
        except Exception as e:
            print(f"Ошибка добавления пользователя: {e}")

    async def is_user_exists(self, telegram_id: int) -> bool:
        query = "SELECT EXISTS (SELECT 1 FROM users WHERE telegram_id=$1);"
        try:
            return await self.pool.fetchval(query, telegram_id)
        except Exception as e:
            print(f"Ошибка проверки пользователя: {e}")
            return False
        
    async def user_profile(self, telegram_id):
        query = "SELECT name, surename, age, phone, role FROM users WHERE telegram_id=$1;"
        try:
            return await self.pool.fetchrow(query, telegram_id)
        except Exception as e:
            print(f"Ошибка получения профиля: {e}")
            return None

    async def get_user_role(self, telegram_id):
        query = "SELECT role FROM users WHERE telegram_id=$1;"
        try:
            return await self.pool.fetchval(query, telegram_id)
        except Exception as e:
            print(f"Ошибка получения роли: {e}")
            return None
        
    async def get_users(self):
        query = "SELECT telegram_id, name, role FROM users ORDER BY telegram_id;"
        try:
            return await self.pool.fetch(query)
        except Exception as e:
            print(f"Ошибка получения списка пользователей: {e}")
            return []

    async def set_user_role(self, telegram_id, role):
        query = "UPDATE users SET role=$1 WHERE telegram_id=$2;"
        try:
            await self.pool.execute(query, role, telegram_id)
        except Exception as e:
            print(f"Ошибка установки роли: {e}")

    async def get_products(self):
        query = "SELECT * FROM products WHERE is_active=TRUE;"
        try:
            return await self.pool.fetch(query)
        except Exception as e:
            print(f"Ошибка получения продуктов: {e}")
            return []