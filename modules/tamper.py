# modules/tamper.py
import requests
from bs4 import BeautifulSoup
import random
import string
import json
import logging
from .form_utils import find_form_fields

config = {}

def load_config():
    global config
    try:
        config_path = 'config/config.json'

        with open('config.json', 'r') as config_file:
            config = json.load(config_file).get('tamper', {})
    except (FileNotFoundError, json.JSONDecodeError):
        config = {}

load_config()

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def tamper_input(url, form, field, tampered_value):
    try:
        form_action = form.get('action') or url
        form_method = form.get('method', 'GET').upper()

        data = {}
        for form_field in find_form_fields(form):
            field_name = form_field.get('name')
            if field_name:
                if form_field.name == 'input' and form_field.get('type') in ['radio', 'checkbox']:
                    if field_name == field:
                        data[field_name] = tampered_value
                    else:
                        data[field_name] = form_field.get('value', 'on')
                elif form_field.name == 'select':
                    selected_option = form_field.find('option', selected=True)
                    if selected_option:
                        data[field_name] = selected_option.get('value', '')
                elif form_field.name == 'textarea':
                    data[field_name] = tampered_value
                else:
                    data[field_name] = form_field.get('value', '')

        tampered_response = requests.request(form_method, form_action, data=data)
        logging.info(f"Tampered input field '{field}' in form on {url} - Status Code: {tampered_response.status_code}")

        return tampered_response.text

    except requests.RequestException as error:
        logging.error(f"Error tampering input field: {error}")
        return f"Error tampering input field: {error}"