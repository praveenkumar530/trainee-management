import pandas as pd
import logging

import asyncpg 
from asyncpg.pool import Pool

logger = logging.getLogger(__name__)
connection_pool : Pool = None 


async def get_connection_string():
    dbname = "gym"
    user = "postgres"
    password = "password"
    host = "localhost"
    port = 5432

    db_connection_string = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    print("db_connection_string ", db_connection_string)
    return db_connection_string

async def create_connection_pool():
    try:
        global connection_pool
        ans = await asyncpg.create_pool(await get_connection_string() )
        print("ans" , ans)
        connection_pool = ans
    except Exception as e:
        print(e)

async def close_connection_pool():
    global connection_pool
    if connection_pool:
        await connection_pool.close()
        connection_pool = None 


# converts it to dataframe and returns
async def fetch_as_dataframe(query: str, *args):
    logger.info(query)
    print(query)
    async with connection_pool.acquire() as conn:
        stmt = await conn.prepare(query)
        columns = [a.name for a in stmt.get_attributes()]
        data = await stmt.fetch(*args)

        return pd.DataFrame(data, columns=columns)

# directly returns json list 
async def fetch_all(query: str, *args):
    print(query)
    async with connection_pool.acquire() as conn:
        return await conn.fetch(query, *args)

async def insert(query: str, *args):
    print("insert query ", query)
    async with connection_pool.acquire() as connection:
        return await connection.execute(query, *args)

async def update(query: str, *args):
    print("update query ", query)
    async with connection_pool.acquire() as connection:
        return await connection.execute(query, *args)