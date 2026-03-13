import asyncpg
from config import config


class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME,
            host=config.DB_HOST,
            port=config.DB_PORT
        )

    # --- USERS ---
    async def add_user(self, telegram_id, name, surename, age, phone):
        query = """
        INSERT INTO users (telegram_id, name, surename, age, phone)
        VALUES ($1, $2, $3, $4, $5)
        """
        await self.pool.execute(query, telegram_id, name, surename, int(age), phone)

    async def get_user_id(self, telegram_id):
        query = "SELECT id FROM users WHERE telegram_id=$1"
        return await self.pool.fetchval(query, telegram_id)

    async def get_user_role(self, telegram_id):
        """
        Foydalanuvchining role ni qaytaradi ('user', 'admin', va hokazo)
        """
        query = "SELECT role FROM users WHERE telegram_id=$1"
        return await self.pool.fetchval(query, telegram_id)

    # --- PRODUCTS ---
    async def get_products(self):
        query = "SELECT * FROM products WHERE is_active=TRUE"
        return await self.pool.fetch(query)

    # --- CART & ORDERS ---
    async def get_or_create_cart(self, user_id):
        order = await self.pool.fetchrow(
            "SELECT * FROM orders WHERE user_id=$1 AND order_status='cart'", user_id
        )
        if order:
            return order["id"]

        order = await self.pool.fetchrow(
            "INSERT INTO orders(user_id) VALUES($1) RETURNING id", user_id
        )
        return order["id"]

    async def add_product_to_cart(self, user_id, product_id):
        order_id = await self.get_or_create_cart(user_id)
        await self.pool.execute(
            "INSERT INTO order_items(order_id, product_id) VALUES($1,$2)", order_id, product_id
        )

    async def get_cart_with_total(self, user_id):
        products = await self.pool.fetch(
            """
            SELECT p.id, p.name, p.price
            FROM order_items oi
            JOIN orders o ON oi.order_id=o.id
            JOIN products p ON oi.product_id=p.id
            WHERE o.user_id=$1 AND o.order_status='cart'
            """,
            user_id
        )
        total = await self.pool.fetchval(
            """
            SELECT SUM(p.price)
            FROM order_items oi
            JOIN orders o ON oi.order_id=o.id
            JOIN products p ON oi.product_id=p.id
            WHERE o.user_id=$1 AND o.order_status='cart'
            """,
            user_id
        )
        return products, total

    # --- GET USER ORDERS ---
    async def get_user_orders(self, user_id):
        """
        Foydalanuvchining barcha buyurtmalarini qaytaradi (cart bo‘lmagan)
        """
        query = """
        SELECT o.id, o.order_status, SUM(p.price) AS total
        FROM orders o
        JOIN order_items oi ON oi.order_id=o.id
        JOIN products p ON p.id=oi.product_id
        WHERE o.user_id=$1 AND o.order_status != 'cart'
        GROUP BY o.id, o.order_status
        ORDER BY o.id DESC
        """
        return await self.pool.fetch(query, user_id)