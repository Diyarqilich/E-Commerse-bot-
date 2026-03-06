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

    async def add_user(self, telegram_id, name, surename, age, phone):
        query = """
        INSERT INTO users (telegram_id, name, surename, age, phone)
        VALUES ($1, $2, $3, $4, $5)
        """
        await self.pool.execute(
            query, telegram_id, name, surename, int(age), phone
        )
    async def is_user_exists(self, telegram_id: int) -> bool:
        query = """
        SELECT EXISTS (
        SELECT 1 FROM users WHERE telegram_id = $1
        );
        """
        return await self.pool.fetchval(query, telegram_id)
    

    async def user_profile(self,telegram_id):
        query="""
        select name,age,phone,role from users where telegram_id=$1;
        """
        return await self.pool.fetchrow(query,telegram_id)
    
    async def get_user_role(self, telegram_id):
        query = "SELECT role FROM users WHERE telegram_id=$1"
        return await self.pool.fetchval(query, telegram_id)
    
    async def get_users(self):
        query = "SELECT telegram_id, name, role FROM users ORDER BY id"
        return await self.pool.fetch(query)
    
    async def set_user_role(self, telegram_id, role):
        query = "UPDATE users SET role=$1 WHERE telegram_id=$2"
        await self.pool.execute(query, role, telegram_id)

    #Products

    async def get_products(self):
        query = "SELECT * FROM products WHERE is_active=TRUE"
        return await self.pool.fetch(query)
    
    async def add_product(self,name,price,description):
        query=""" INSERT INTO products(name,price,description) VALUES($1,$2,$3)"""
        await self.pool.execute(query,name,int(price),description)