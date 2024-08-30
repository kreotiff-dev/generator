from dotenv import load_dotenv
import os

# Загрузка значений из .env файла
load_dotenv()

class Config:
    DEBUG = os.getenv('DEBUG')
    SECRET_KEY = os.getenv('SECRET_KEY')
    DATABASE = {
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME')
    }

class DevelopmentConfig(Config):
    DEBUG = os.getenv('DEBUG', True)

class ProductionConfig(Config):
    DEBUG = os.getenv('DEBUG', False)

def get_config(env):
    if env == 'production':
        return ProductionConfig()
    else:
        return DevelopmentConfig()
