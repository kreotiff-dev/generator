import logging
import psycopg2

# Настройка логгирования
logger = logging.getLogger(__name__)

class TransactionRepository:
    def __init__(self, conn):
        self.conn = conn

    def create_transaction(self, transaction):
        with self.conn.cursor() as c:
            try:
                logger.info("Создание транзакции для карты с ID: %s", transaction.card_id)
                c.execute("""
                    INSERT INTO transactions (card_id, transaction_date, amount, transaction_type, transaction_status, transaction_description)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (transaction.card_id, transaction.transaction_date, transaction.amount, transaction.transaction_type,
                      transaction.transaction_status, transaction.transaction_description))
                self.conn.commit()
                logger.info("Транзакция успешно создана для карты с ID: %s", transaction.card_id)
            except psycopg2.Error as e:
                self.conn.rollback()
                logger.error("Ошибка при создании транзакции для карты с ID: %s, ошибка: %s", transaction.card_id, e)
                return {"error": str(e)}

    def get_card_by_number(self, card_number):
        with self.conn.cursor() as c:
            try:
                logger.info("Получение карты по номеру: %s", card_number)
                c.execute("SELECT id FROM cards WHERE card_number = %s", (card_number,))
                card = c.fetchone()
                if card:
                    logger.info("Карта найдена с ID: %s", card[0])
                else:
                    logger.warning("Карта с номером %s не найдена", card_number)
                return card
            except psycopg2.Error as e:
                logger.error("Ошибка при получении карты по номеру %s: %s", card_number, e)
                return {"error": str(e)}
