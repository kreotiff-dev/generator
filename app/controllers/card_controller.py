import logging
from flask import jsonify

from ..repositories.card_repository import CardRepository
from ..repositories.user_repository import UserRepository
from ..services.card_service import CardService
from ..services.user_service import UserService
from config.database import get_db_connection

# Настройка логгирования
logger = logging.getLogger(__name__)

# Создание соединения с базой данных и репозиториев
try:
    conn = get_db_connection()
    user_service = UserService(conn)
    card_repository = CardRepository(conn)
    user_repository = UserRepository(conn)
    card_service = CardService(card_repository, user_service, user_repository)
    logger.info("Сервисы и репозитории успешно инициализированы")
except Exception as e:
    logger.error(f"Ошибка при инициализации сервисов: {e}")
    raise

def generate_card(request):
    logger.info("Начата обработка запроса на генерацию карты")
    if request.is_json:
        try:
            card_id = card_service.generate_card(request)
            if isinstance(card_id, dict) and "error" in card_id:
                logger.error(f"Ошибка при генерации карты: {card_id['error']}")
                return jsonify(card_id), 500
            logger.info(f"Карта успешно сгенерирована с ID: {card_id}")
            return jsonify({'status': 'success', 'card_id': card_id})
        except Exception as e:
            logger.error(f"Необработанная ошибка в generate_card: {e}")
            return jsonify({'error': 'Internal Server Error'}), 500
    else:
        logger.error("Неподдерживаемый формат запроса. Ожидается JSON.")
        return jsonify({'error': 'Unsupported Media Type'}), 415
