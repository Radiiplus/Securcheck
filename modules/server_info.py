# modules/server_info.py
import requests
import logging

def get_server_info(url):
    try:
        response = requests.get(url)
        server_info = response.headers.get('Server', 'Unknown')
        return server_info
    except requests.RequestException as error:
        logging.error(f"Error retrieving server information: {error}")
        return None