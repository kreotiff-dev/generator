import logging
import psycopg2

# Настройка логгирования
logger = logging.getLogger(__name__)

class CardRepository:
    def __init__(self, conn):
        self.conn = conn

    def create_card(self, card):
        with self.conn.cursor() as c:
            try:
                logger.info("Создание карты для пользователя с ID: %s", card.user_id)
                logger.debug("Тип объекта card: %s", type(card))
                logger.debug("Значения атрибутов карты: %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s",
                             card.user_id, card.card_number, card.expiration_date, card.cvv,
                             card.cardholder_firstname, card.cardholder_lastname, card.card_type,
                             card.card_category, card.card_status, card.currency,
                             card.card_limit, card.card_balance, card.last_usage_date)

                c.execute("""
                    INSERT INTO cards (user_id, card_number, expiration_date, cvv, cardholder_firstname, cardholder_lastname, 
                                       card_type, card_category, card_status, currency, card_limit, card_balance, last_usage_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
                """, (card.user_id, card.card_number, card.expiration_date, card.cvv, card.cardholder_firstname,
                      card.cardholder_lastname, card.card_type, card.card_category, card.card_status,
                      card.currency, card.card_limit, card.card_balance, card.last_usage_date))
                card_id = c.fetchone()[0]
                self.conn.commit()
                logger.info("Карта успешно создана с ID: %s", card_id)
                return card_id
            except psycopg2.Error as e:
                self.conn.rollback()
                logger.error("Ошибка при создании карты: %s", e)
                return {"error": str(e)}

    def update_card_request(self, card_id, request_id):
        with self.conn.cursor() as c:
            try:
                logger.info("Обновление запроса на карту с ID запроса: %s для карты с ID: %s", request_id, card_id)
                c.execute("""
                    UPDATE card_requests
                    SET card_id = %s
                    WHERE id = %s
                """, (card_id, request_id))
                self.conn.commit()
                logger.info("Запрос на карту успешно обновлен для ID запроса: %s", request_id)
            except psycopg2.Error as e:
                self.conn.rollback()
                logger.error("Ошибка при обновлении запроса на карту: %s", e)
                return {"error": str(e)}
