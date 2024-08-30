import logging
from flask import jsonify
from ..services.user_service import UserService
from config.database import get_db_connection
from ..repositories.user_repository import UserRepository  # Исправлено на правильный путь

# Настройка логгирования
logger = logging.getLogger(__name__)

# Создание соединения с базой данных и репозитория
try:
    conn = get_db_connection()
    user_repository = UserRepository(conn)
    user_service = UserService(user_repository)
    logger.info("UserService и UserRepository успешно инициализированы")
except Exception as e:
    logger.error(f"Ошибка при инициализации сервисов: {e}")
    raise

def get_user_by_phone(phone):
    logger.info(f"Начат запрос на получение пользователя с номером телефона: {phone}")
    try:
        user = user_service.get_user_by_phone(phone)
        if user:
            logger.info(f"Пользователь с номером телефона {phone} найден")
            return jsonify(user)
        else:
            logger.warning(f"Пользователь с номером телефона {phone} не найден")
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        logger.error(f"Необработанная ошибка в get_user_by_phone: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

def generate_user(request):
    logger.info("Начата обработка запроса на создание пользователя")
    try:
        user_id = user_service.generate_user(request)
        if isinstance(user_id, dict) and "error" in user_id:
            logger.error(f"Ошибка при создании пользователя: {user_id['error']}")
            return jsonify(user_id), 500
        logger.info(f"Пользователь успешно создан с ID: {user_id}")
        return jsonify({"status": "success", "user_id": user_id})
    except Exception as e:
        logger.error(f"Необработанная ошибка в generate_user: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
