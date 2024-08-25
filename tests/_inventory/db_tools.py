__all__ = [
    "create_database",
    "drop_database",
]

import logging
from asyncio import sleep

import asyncpg

logger = logging.getLogger('db_tools')


async def create_database(url):
    db_name = url.split('/')[-1]
    url = url.replace('+asyncpg', '').replace(db_name, '')
    logger.info('Creating database...')
    logger.info(f'Database name: {db_name}')
    try:
        conn = await asyncpg.connect(url)
        await conn.execute(f'CREATE DATABASE {db_name}')
        await conn.close()
        logger.info('Database created')
    except Exception as e:
        logger.error(f'Error creating database: {e}')
        raise e


async def drop_database(url, force=False):
    db_name = url.split('/')[-1]
    url = url.replace('+asyncpg', '').replace(db_name, '')

    logger.info('Dropping database...')

    logger.info(f'Database name: {db_name}')
    try:
        conn = await asyncpg.connect(url)
        if force:
            await conn.execute(f'''
                SELECT pg_terminate_backend(pid) 
                FROM pg_stat_activity 
                WHERE datname = '{db_name}' 
                AND pid <> pg_backend_pid();
            ''')
        await conn.execute(f'DROP DATABASE IF EXISTS {db_name}')
        await conn.close()
        logger.info('Database dropped')
    except Exception as e:
        logger.error(f'Error dropping database: {e}')
        raise e
