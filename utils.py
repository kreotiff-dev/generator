import random
import string
import bcrypt

def generate_phone_number():
    return '+7' + ''.join(random.choices(string.digits, k=10))

def generate_email():
    domains = ["example.com", "test.com", "mail.com"]
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + '@' + random.choice(domains)

def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

def hash_password(password):
    # Укажите количество раундов (work factor), соответствующее значению в основном приложении (3 в данном случае)
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()

def generate_card_number():
    return ''.join(random.choices(string.digits, k=16))

def generate_cvv():
    return ''.join(random.choices(string.digits, k=3))

def generate_first_name():
    return random.choice(["Ivan", "Petr", "Alexey"])

def generate_last_name():
    return random.choice(["Ivanov", "Petrov", "Sidorov"])

def translate_to_latin(text):
    map = {
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E', 'Ж': 'Zh', 'З': 'Z',
        'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R',
        'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch',
        'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya',
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z',
        'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
    }
    return ''.join([map.get(char, char) for char in text])
