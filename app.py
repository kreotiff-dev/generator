from flask import Flask, render_template, request, jsonify
from config.logging_config import setup_logging
from app.controllers.user_controller import generate_user, get_user_by_phone
from app.controllers.card_controller import generate_card
from app.controllers.transaction_controller import generate_transaction
from app.controllers.general_controller import generate_all

setup_logging()

app = Flask(__name__)

@app.route('/generate_user', methods=['POST'])
def handle_generate_user():
    return generate_user(request)

@app.route('/generate_card', methods=['POST'])
def handle_generate_card():
    return generate_card(request)

@app.route('/generate_transaction', methods=['POST'])
def handle_generate_transaction():
    return generate_transaction(request)

@app.route('/generate_all', methods=['POST'])
def handle_generate_all():
    return generate_all(request)

@app.route('/get_user', methods=['GET'])
def handle_get_user():
    phone = request.args.get('phone')
    user_info = get_user_by_phone(phone)
    if user_info:
        return jsonify(user_info)
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
