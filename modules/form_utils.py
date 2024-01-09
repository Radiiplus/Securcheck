# modules/form_utils.py
from bs4 import BeautifulSoup

def find_form_fields(form):
    return form.find_all(['input', 'select', 'textarea'])

def explore_forms(forms):
    try:
        for i, form in enumerate(forms, start=1):
            print(f"\nForm {i}:")
            form_fields = find_form_fields(form)
            for field in form_fields:
                field_name = field.get('name')
                print(f"- {field_name} ({field.name})")
        return True
    except Exception as error:
        logging.error(f"Error exploring forms: {error}")
        return False