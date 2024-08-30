import logging
import psycopg2

# Настройка логгирования
logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self, conn):
        self.conn = conn

    def create_user(self, user):
        with self.conn.cursor() as c:
            try:
                logger.info("Создание пользователя с email: %s", user.email)
                c.execute("""
                    INSERT INTO users (first_name, last_name, email, password, phone)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id
                """, (user.first_name, user.last_name, user.email, user.password, user.phone))

                user_id = c.fetchone()
                if user_id:
                    self.conn.commit()
                    logger.info("Пользователь успешно создан с ID: %s", user_id[0])
                    return user_id[0]
                else:
                    self.conn.rollback()
                    logger.error("Ошибка при создании пользователя: запись не была вставлена.")
                    return {"error": "Ошибка при создании пользователя"}
            except psycopg2.Error as e:
                self.conn.rollback()
                logger.error("Ошибка при создании пользователя: %s", e)
                return {"error": str(e)}

    def get_user_by_phone(self, phone):
        with self.conn.cursor() as c:
            try:
                logger.info("Получение пользователя с номером телефона: %s", phone)
                c.execute("SELECT id, first_name, last_name FROM users WHERE phone = %s", (phone,))
                user = c.fetchone()
                if user:
                    logger.info("Пользователь найден с ID: %s", user[0])
                    return {
                        "id": user[0],
                        "first_name": user[1],
                        "last_name": user[2]
                    }
                else:
                    logger.warning("Пользователь с номером телефона %s не найден", phone)
                    return None
            except psycopg2.Error as e:
                logger.error("Ошибка при получении пользователя: %s", e)
                return {"error": str(e)}
