document.addEventListener('DOMContentLoaded', function() {
    function showAlert(message, callback) {
        if (confirm(message)) {
            callback();
        }
    }

    function generateRandomData() {
        return Math.random().toString(36).substr(2, 8);
    }

    function translateToLatin(text) {
        const map = {
            'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E', 'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y',
            'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F',
            'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Ы': 'Y', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya', 'Ь': '',
            'Ъ': '', 'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
            'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'y', 'э': 'e', 'ю': 'yu', 'я': 'ya',
            'ь': '', 'ъ': ''
        };
        return text.split('').map(char => map[char] || char).join('');
    }

    function fillUserNames(phone) {
        fetch(`/get_user?phone=${phone}`)
            .then(handleResponse)
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    document.getElementById('cardholder_firstname').value = translateToLatin(data.first_name);
                    document.getElementById('cardholder_lastname').value = translateToLatin(data.last_name);
                }
            })
            .catch(error => alert('Ошибка: ' + error.message));
    }

    function sendFormData(url, formId, resultId) {
    const form = document.getElementById(formId);
    const formData = new FormData(form);

    // Преобразование FormData в JSON
    const jsonData = {};
    formData.forEach((value, key) => {
        jsonData[key] = value;
    });

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
    })
    .then(handleResponse)
    .then(data => {
        document.getElementById(resultId).innerText = JSON.stringify(data, null, 2);
    })
    .catch(error => alert('Ошибка: ' + error.message));
}


    function generateUser() {
        sendFormData('/generate_user', 'user-form', 'user-result');
    }

    function generateCard() {
            sendFormData('/generate_card', 'card-form', 'card-result');
    }

    function generateTransaction() {
        sendFormData('/generate_transaction', 'transaction-form', 'transaction-result');
    }

    function generateAll() {
        fetch('/generate_all', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
            }
        })
        .then(handleResponse)
        .then(data => {
            document.getElementById('all-result').innerText = JSON.stringify(data, null, 2);
        })
        .catch(error => alert('Ошибка: ' + error.message));
    }

    function autoGenerate(fieldId) {
        switch (fieldId) {
            case 'expiration_date':
                autoGenerateValue(fieldId, new Date(new Date().setFullYear(new Date().getFullYear() + 3)).toISOString().split('T')[0]);
                break;
            case 'cvv':
                autoGenerateValue(fieldId, '', () => Math.floor(100 + Math.random() * 900).toString());
                break;
            case 'cardholder_firstname':
                autoGenerateValue(fieldId, translateToLatin('Иван'));
                break;
            case 'cardholder_lastname':
                autoGenerateValue(fieldId, translateToLatin('Иванов'));
                break;
            case 'card_limit':
                autoGenerateValue(fieldId, '10000');
                break;
            case 'card_balance':
                autoGenerateValue(fieldId, '5000');
                break;
            case 'last_usage_date':
                autoGenerateValue(fieldId, new Date().toISOString().split('T')[0]);
                break;
            default:
                break;
        }
    }

    function autoGenerateValue(fieldId, defaultValue, generator) {
        document.getElementById(fieldId).value = generator ? generator() : defaultValue;
    }

    function autoFillFields() {
        autoGenerate('expiration_date');
        autoGenerate('cvv');
        autoGenerate('cardholder_firstname');
        autoGenerate('cardholder_lastname');
        autoGenerate('card_limit');
        autoGenerate('card_balance');
        autoGenerate('last_usage_date');
        sendFormData('/generate_card', 'card-form', 'card-result');
    }

    function handleResponse(response) {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    }

    window.generateUser = generateUser;
    window.generateCard = generateCard;
    window.generateTransaction = generateTransaction;
    window.generateAll = generateAll;
    window.autoGenerate = autoGenerate;
});
