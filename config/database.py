import psycopg2
from psycopg2 import OperationalError
import logging
from .config import get_config
import os

logger = logging.getLogger(__name__)
# Определение текущей среды (например, через переменную окружения)
env = os.getenv('FLASK_ENV', 'development')

# Получение конфигурации
config = get_config(env)

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=config.DATABASE['database'],
            user=config.DATABASE['user'],
            password=config.DATABASE['password'],
            host=config.DATABASE['host'],
            port=config.DATABASE['port']
        )
        return conn
    except Exception as e:
        logger.error(f"Ошибка при подключении к базе данных: {e}")
        raise
def check_database_connection():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute('SELECT version();')
            db_version = cursor.fetchone()
            print(f"Подключение к базе данных успешно! Версия базы данных: {db_version[0]}")
    except OperationalError as e:
        print(f"Ошибка подключения к базе данных: {e}")
    finally:
        if conn:
            conn.close()