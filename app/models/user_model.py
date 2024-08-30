class User:
    def __init__(self, phone, email, password, confirmed, first_name, last_name, created_at=None, updated_at=None):
        self.phone = phone
        self.email = email
        self.password = password
        self.confirmed = confirmed
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = created_at
        self.updated_at = updated_at
