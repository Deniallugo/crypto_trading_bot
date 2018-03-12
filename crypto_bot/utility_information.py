import requests

company_name = 'crypto_bot'
base_url = 'https://sarafankabot.ru:8443/bot'


def send_data(data):
    data = data if isinstance(data, str) else str(data)
    data = {
        'company_name': company_name,
        'error': data
    }
    requests.post(url=base_url + '/error_endpoint', json=data)
