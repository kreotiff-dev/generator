import logging
from ..utils.utils import generate_card_number, generate_cvv, generate_first_name, generate_last_name
from datetime import datetime, timedelta
import random

# Настройка логгирования
logger = logging.getLogger(__name__)

class GeneralService:
    def __init__(self, user_service, card_service, transaction_service):
        self.user_service = user_service
        self.card_service = card_service
        self.transaction_service = transaction_service

    def generate_all(self, request):
        logger.info("Начата обработка запроса на генерацию всех данных")
        try:
            user_response = self.user_service.generate_user(request)
            user_data = user_response.get_json()

            if 'last_name' not in user_data:
                user_data['last_name'] = generate_last_name()

            phone = user_data['phone']
            email = user_data['email']
            password = user_data['password']
            user_id = user_data['user_id']

            logger.info(f"Пользователь успешно создан с ID: {user_id}")

            card_ids = []
            for _ in range(3):
                card_type = random.choice(['Visa', 'MasterCard', 'UnionPay', 'МИР'])
                card_number = generate_card_number()
                expiration_date = (datetime.now() + timedelta(days=365 * 3)).strftime('%Y-%m-%d')
                cvv = generate_cvv()
                cardholder_firstname = generate_first_name()
                cardholder_lastname = user_data['last_name']
                card_category = random.choice(['debit', 'credit'])
                card_status = random.choice(['blocked', 'Active', 'In Progress', 'Wait Activation'])
                currency = random.choice(['USD', 'RUB', 'EUR', 'CNY'])
                card_limit = round(random.uniform(1000, 10000), 2)
                card_balance = round(random.uniform(0, card_limit), 2)
                last_usage_date = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')

                card_data = {
                    'user_id': user_id,
                    'card_number': card_number,
                    'expiration_date': expiration_date,
                    'cvv': cvv,
                    'cardholder_firstname': cardholder_firstname,
                    'cardholder_lastname': cardholder_lastname,
                    'card_type': card_type,
                    'card_category': card_category,
                    'card_status': card_status,
                    'currency': currency,
                    'card_limit': card_limit,
                    'card_balance': card_balance,
                    'last_usage_date': last_usage_date
                }

                card_id = self.card_service.create_card(card_data)
                if isinstance(card_id, dict) and "error" in card_id:
                    logger.error(f"Ошибка при создании карты: {card_id['error']}")
                    return card_id
                card_ids.append(card_id)

                logger.info(f"Карта успешно создана с ID: {card_id}")

                for _ in range(5):
                    transaction_date = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d %H:%M:%S')
                    amount = round(random.uniform(10.0, 1000.0), 2)
                    transaction_type = random.choice(['buy', 'top-up'])
                    transaction_status = random.choice(['Executed', 'Rejected', 'Pending', 'Draft'])
                    transaction_description = 'Тестовая транзакция'

                    transaction_data = {
                        'card_id': card_id,
                        'transaction_date': transaction_date,
                        'amount': amount,
                        'transaction_type': transaction_type,
                        'transaction_status': transaction_status,
                        'transaction_description': transaction_description
                    }

                    self.transaction_service.create_transaction(transaction_data)
                    logger.info(f"Транзакция успешно создана для карты с ID: {card_id}")

            return {
                'status': 'success',
                'user': {
                    'phone': phone,
                    'email': email,
                    'password': password
                },
                'card_ids': card_ids
            }
        except Exception as e:
            logger.error(f"Необработанная ошибка в generate_all: {e}")
            return {"error": "Internal Server Error"}, 500
