from flask import jsonify
from database import get_db_connection
from utils import generate_phone_number, generate_email, generate_password, hash_password, generate_card_number, \
    generate_cvv, generate_first_name, generate_last_name, translate_to_latin
from datetime import datetime, timedelta
import random
import psycopg2


def get_user_by_phone(phone):
    print(f"Поиск пользователя с номером телефона: {phone}")
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("SELECT first_name, last_name FROM users WHERE phone = %s", (phone,))
        user = c.fetchone()
        if not user:
            return None
        return {
            "first_name": user[0],
            "last_name": user[1]
        }
    except psycopg2.Error as e:
        return {"error": str(e)}
    finally:
        c.close()
        conn.close()


def generate_user(request):
    phone = request.form.get('phone') or generate_phone_number()
    email = request.form.get('email') or generate_email()
    password = request.form.get('password') or generate_password()
    hashed_password = hash_password(password)
    confirmed = request.form.get('confirmed', 'false').lower() == 'true'
    first_name = request.form.get('first_name') or generate_first_name()
    last_name = request.form.get('last_name') or generate_last_name()
    created_at = datetime.now()
    updated_at = created_at

    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO users (phone, email, password, confirmed, first_name, last_name, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
        """, (phone, email, hashed_password, confirmed, first_name, last_name, created_at, updated_at))
        user_id = c.fetchone()[0]
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        c.close()
        conn.close()

    return jsonify({'phone': phone, 'email': email, 'password': password, 'user_id': user_id})


def generate_card(request):
    phone = request.form.get('phone')
    card_type = request.form.get('card_type')
    card_number = request.form.get('card_number') or generate_card_number()
    expiration_date = request.form.get('expiration_date') or (datetime.now() + timedelta(days=365 * 3)).strftime(
        '%Y-%m-%d')
    cvv = request.form.get('cvv') or generate_cvv()
    cardholder_firstname = request.form.get('cardholder_firstname')
    cardholder_lastname = request.form.get('cardholder_lastname')
    card_category = request.form.get('card_category')
    card_status = request.form.get('card_status')
    currency = request.form.get('currency')
    card_limit = request.form.get('card_limit') or None
    card_balance = request.form.get('card_balance') or None
    last_usage_date = request.form.get('last_usage_date') or None

    user_info = get_user_by_phone(phone)
    if user_info:
        if not cardholder_firstname:
            cardholder_firstname = translate_to_latin(user_info['first_name'])
        if not cardholder_lastname:
            cardholder_lastname = translate_to_latin(user_info['last_name'])

    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("SELECT id FROM users WHERE phone = %s", (phone,))
        user = c.fetchone()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        user_id = user[0]

        c.execute("""
            INSERT INTO cards (user_id, card_number, expiration_date, cvv, cardholder_firstname, cardholder_lastname, 
                               card_type, card_category, card_status, currency, card_limit, card_balance, last_usage_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
        """, (user_id, card_number, expiration_date, cvv, cardholder_firstname, cardholder_lastname, card_type,
              card_category, card_status, currency, card_limit, card_balance, last_usage_date))
        card_id = c.fetchone()[0]
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        c.close()
        conn.close()

    return jsonify({'status': 'success', 'card_id': card_id})


def generate_transaction(request):
    card_number = request.form.get('card_number')
    transaction_date = request.form.get('transaction_date')
    amount = request.form.get('amount')
    transaction_type = request.form.get('transaction_type')
    transaction_status = request.form.get('transaction_status')
    transaction_description = request.form.get('transaction_description')

    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("SELECT id FROM cards WHERE card_number = %s", (card_number,))
        card = c.fetchone()
        if not card:
            return jsonify({'error': 'Card not found'}), 404

        card_id = card[0]

        c.execute("""
            INSERT INTO transactions (card_id, transaction_date, amount, transaction_type, transaction_status, transaction_description)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (card_id, transaction_date, amount, transaction_type, transaction_status, transaction_description))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        c.close()
        conn.close()

    return jsonify({'status': 'success'})


def generate_all(request):
    user_response = generate_user(request)
    user_data = user_response.get_json()

    # Проверка наличия ключа 'last_name'
    if 'last_name' not in user_data:
        user_data['last_name'] = generate_last_name()

    phone = user_data['phone']
    email = user_data['email']
    password = user_data['password']
    user_id = user_data['user_id']

    # Генерация нескольких карт для пользователя
    conn = get_db_connection()
    c = conn.cursor()
    try:
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

            c.execute("""
                INSERT INTO cards (user_id, card_number, expiration_date, cvv, cardholder_firstname, cardholder_lastname, 
                                   card_type, card_category, card_status, currency, card_limit, card_balance, last_usage_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
            """, (user_id, card_number, expiration_date, cvv, cardholder_firstname, cardholder_lastname, card_type,
                  card_category, card_status, currency, card_limit, card_balance, last_usage_date))

            card_id_result = c.fetchone()
            if card_id_result is None:
                conn.rollback()
                return jsonify({'error': 'Failed to insert card data'}), 500

            card_id = card_id_result[0]
            card_ids.append(card_id)

            # Генерация нескольких транзакций для каждой карты
            for _ in range(5):
                transaction_date = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime(
                    '%Y-%m-%d %H:%M:%S')
                amount = round(random.uniform(10.0, 1000.0), 2)
                transaction_type = random.choice(['buy', 'top-up'])
                transaction_status = random.choice(['Executed', 'Rejected', 'Pending', 'Draft'])
                transaction_description = 'Тестовая транзакция'

                c.execute("""
                    INSERT INTO transactions (card_id, transaction_date, amount, transaction_type, transaction_status, transaction_description)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (card_id, transaction_date, amount, transaction_type, transaction_status, transaction_description))

        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        c.close()
        conn.close()

    return jsonify({
        'status': 'success',
        'user': {
            'phone': phone,
            'email': email,
            'password': password
        },
        'card_ids': card_ids
    })
