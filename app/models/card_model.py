class Card:
    def __init__(self, user_id, card_number, expiration_date, cvv, cardholder_firstname, cardholder_lastname,
                 card_type, card_category, card_status, currency, card_limit=None, card_balance=None, last_usage_date=None):
        self.user_id = user_id
        self.card_number = card_number
        self.expiration_date = expiration_date
        self.cvv = cvv
        self.cardholder_firstname = cardholder_firstname
        self.cardholder_lastname = cardholder_lastname
        self.card_type = card_type
        self.card_category = card_category
        self.card_status = card_status
        self.currency = currency
        self.card_limit = card_limit
        self.card_balance = card_balance
        self.last_usage_date = last_usage_date
