import asyncpg
from config import DB_CONFIG

async def get_db():
    return await asyncpg.connect(**DB_CONFIG)

async def create_tables():
    conn = await get_db()
    
    await conn.close()
    print("✅ Database tayyor!")