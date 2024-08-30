import logging
from flask import jsonify

from ..repositories.transaction_repository import TransactionRepository
from ..services.transaction_service import TransactionService
from config.database import get_db_connection

# Настройка логгирования
logger = logging.getLogger(__name__)

# Создание соединения с базой данных и репозитория
try:
    conn = get_db_connection()
    transaction_repository = TransactionRepository(conn)
    transaction_service = TransactionService(transaction_repository)
    logger.info("TransactionService и TransactionRepository успешно инициализированы")
except Exception as e:
    logger.error(f"Ошибка при инициализации сервисов: {e}")
    raise

def generate_transaction(request):
    logger.info("Начата обработка запроса на генерацию транзакции")
    try:
        result = transaction_service.generate_transaction(request)
        if isinstance(result, tuple) and result[1] == 404:
            logger.warning(f"Транзакция не найдена: {result[0]}")
            return jsonify(result[0]), 404
        elif isinstance(result, dict) and "error" in result:
            logger.error(f"Ошибка при генерации транзакции: {result['error']}")
            return jsonify(result), 500
        logger.info("Транзакция успешно сгенерирована")
        return jsonify({'status': 'success'})
    except Exception as e:
        logger.error(f"Необработанная ошибка в generate_transaction: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
