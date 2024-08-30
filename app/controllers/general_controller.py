import logging
from flask import jsonify, request

from ..repositories import user_repository
from ..services.general_service import GeneralService
from ..services.user_service import UserService
from ..services.card_service import CardService
from ..services.transaction_service import TransactionService
from config.database import get_db_connection

# Настройка логгирования
logger = logging.getLogger(__name__)

# Создание соединения с базой данных и репозиториев
try:
    conn = get_db_connection()
    user_service = UserService(conn)
    transaction_service = TransactionService(conn)
    card_service = CardService(transaction_service, user_service, user_repository)
    general_service = GeneralService(user_service, card_service, transaction_service)
    logger.info("Сервисы и репозитории успешно инициализированы")
except Exception as e:
    logger.error(f"Ошибка при инициализации сервисов: {e}")
    raise

def generate_all(request):
    logger.info("Начата обработка запроса на генерацию всех данных")
    try:
        result = general_service.generate_all(request)
        if isinstance(result, dict) and "error" in result:
            logger.error(f"Ошибка при генерации данных: {result['error']}")
            return jsonify(result), 500
        logger.info("Данные успешно сгенерированы")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Необработанная ошибка в generate_all: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
