import logging
from datetime import datetime, timedelta
from ..utils.utils import generate_card_number, generate_cvv, translate_to_latin
from ..models.card_model import Card
from ..repositories.card_repository import CardRepository

logger = logging.getLogger(__name__)
class CardService:
    def __init__(self, card_repository, user_service, user_repository):
        self.card_repository = card_repository
        self.user_repository = user_repository
        self.user_service = user_service

    def generate_card(self, request):
        logger.info("Начата обработка запроса на генерацию карты")
        data = request.get_json()
        try:
            phone = data.get('phone')
            card_type = data.get('card_type')
            card_number = data.get('card_number') or generate_card_number()
            expiration_date = data.get('expiration_date') or (datetime.now() + timedelta(days=365 * 3)).strftime('%Y-%m-%d')
            cvv = data.get('cvv') or generate_cvv()
            cardholder_firstname = data.get('cardholder_firstname')
            cardholder_lastname = data.get('cardholder_lastname')
            card_category = data.get('card_category')
            card_status = data.get('card_status') or "Active"
            currency = data.get('currency')
            card_limit = data.get('card_limit') or None
            card_balance = data.get('card_balance')
            last_usage_date = data.get('last_usage_date') or None
            request_id = data.get('request_id')

            user = self.user_repository.get_user_by_phone(phone)
            if isinstance(user, dict) and "error" in user:
                logger.warning(f"Ошибка при получении пользователя с номером телефона {phone}: {user['error']}")
                return user, 500
            elif user:
                logger.info(f"Пользователь найден с ID: {user['id']}")
            else:
                logger.warning(f"Пользователь с номером телефона {phone} не найден")
                return {"error": "User not found"}, 404

            card = Card(
                user_id=user['id'],
                card_number=card_number,
                expiration_date=expiration_date,
                cvv=cvv,
                cardholder_firstname=cardholder_firstname,
                cardholder_lastname=cardholder_lastname,
                card_type=card_type,
                card_category=card_category,
                card_status=card_status,
                currency=currency,
                card_limit=card_limit,
                card_balance=card_balance,
                last_usage_date=last_usage_date
            )

            card_id = self.card_repository.create_card(card)
            if isinstance(card_id, dict) and "error" in card_id:
                logger.error(f"Ошибка при создании карты: {card_id['error']}")
                return card_id, 500

            logger.info(f"Карта успешно создана с ID: {card_id}")

            if request_id:
                self.card_repository.update_card_request(card_id, request_id)
                logger.info(f"Запрос на карту обновлен с ID запроса: {request_id}")

            return card_id
        except Exception as e:
            logger.error(f"Необработанная ошибка в generate_card: {e}")
            return {"error": "Internal Server Error"}, 500
