import logging
from datetime import datetime
from ..utils.utils import generate_phone_number, generate_email, generate_password, hash_password, generate_first_name, generate_last_name
from ..models.user_model import User
from ..repositories.user_repository import UserRepository

# Настройка логгирования
logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def get_user_by_phone(self, phone):
        logger.info(f"Поиск пользователя с номером телефона: {phone}")
        try:
            user = self.user_repository.get_user_by_phone(phone)
            if user:
                logger.info(f"Пользователь найден: {user}")
                return user
            else:
                logger.warning(f"Пользователь с номером телефона {phone} не найден")
                return {"error": "User not found"}, 404
        except Exception as e:
            logger.error(f"Ошибка при поиске пользователя с номером телефона {phone}: {e}")
            return {"error": "Internal Server Error"}, 500

    def generate_user(self, request):
        logger.info("Начата обработка запроса на создание пользователя")
        data = request.get_json()
        try:
            phone = data.get('phone') or generate_phone_number()
            email = data.get('email') or generate_email()
            password = data.get('password') or generate_password()
            hashed_password = hash_password(password)
            confirmed = data.get('confirmed', 'false').lower() == 'true'
            first_name = data.get('first_name') or generate_first_name()
            last_name = data.get('last_name') or generate_last_name()
            created_at = datetime.now()
            updated_at = created_at
            logger.info(f"Пользователь успешно создан с фам: {phone}, {last_name}")

            user = User(phone, email, hashed_password, confirmed, first_name, last_name, created_at, updated_at)

            # Вызов метода create_user через репозиторий
            user_id = self.user_repository.create_user(user)

            if isinstance(user_id, dict) and "error" in user_id:
                logger.error(f"Ошибка при создании пользователя: {user_id['error']}")
                return user_id, 500

            logger.info(f"Пользователь успешно создан с ID: {user_id}")
            return {"user_id": user_id}
        except Exception as e:
            logger.error(f"Необработанная ошибка при создании пользователя: {e}")
            return {"error": "Internal Server Error"}, 500
