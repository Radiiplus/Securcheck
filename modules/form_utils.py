# modules/form_utils.py
import logging
from bs4 import BeautifulSoup

def find_form_fields(form):
    return form.find_all(['input', 'select', 'textarea'])

def explore_forms(forms):
    try:
        for i, form in enumerate(forms, start=1):
            logging.info(f"\nForm {i}:")
            form_fields = find_form_fields(form)
            for field in form_fields:
                field_name = field.get('name')
                logging.info(f"- {field_name} ({field.name})")
        return True
    except Exception as error:
        logging.error(f"Error exploring forms: {error}")
        return False