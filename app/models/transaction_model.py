class Transaction:
    def __init__(self, card_id, transaction_date, amount, transaction_type, transaction_status, transaction_description):
        self.card_id = card_id
        self.transaction_date = transaction_date
        self.amount = amount
        self.transaction_type = transaction_type
        self.transaction_status = transaction_status
        self.transaction_description = transaction_description
