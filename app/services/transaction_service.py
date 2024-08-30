import logging
from ..models.transaction_model import Transaction
from ..repositories.transaction_repository import TransactionRepository

# Настройка логгирования
logger = logging.getLogger(__name__)

class TransactionService:
    def __init__(self, transaction_repository):
        self.transaction_repository = transaction_repository

    def generate_transaction(self, request):
        logger.info("Начата обработка запроса на генерацию транзакции")
        data = request.get_json()
        try:
            card_number = data.get('card_number')
            transaction_date = data.get('transaction_date')
            amount = data.get('amount')
            transaction_type = data.get('transaction_type')
            transaction_status = data.get('transaction_status')
            transaction_description = data.get('transaction_description')

            logger.info(f"Поиск карты с номером: {card_number}, {transaction_date}")
            card = self.transaction_repository.get_card_by_number(card_number)
            if not card:
                logger.warning(f"Карта с номером {card_number} не найдена")
                return {'error': 'Card not found'}, 404

            card_id = card[0]
            logger.info(f"Карта найдена с ID: {card_id}")

            transaction = Transaction(
                card_id=card_id,
                transaction_date=transaction_date,
                amount=amount,
                transaction_type=transaction_type,
                transaction_status=transaction_status,
                transaction_description=transaction_description
            )

            result = self.transaction_repository.create_transaction(transaction)
            if isinstance(result, dict) and "error" in result:
                logger.error(f"Ошибка при создании транзакции: {result['error']}")
                return result, 500

            logger.info(f"Транзакция успешно создана для карты с ID: {card_id}")
            return result

        except Exception as e:
            logger.error(f"Необработанная ошибка в generate_transaction: {e}")
            return {'error': 'Internal Server Error'}, 500
