# modules/endpoint.py
import requests
import json
import random
import string
import logging
from concurrent.futures import ThreadPoolExecutor
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def setup_session():
    session = requests.Session()
    retry_strategy = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def generate_random_user():
    username = ''.join(random.choices(string.ascii_lowercase, k=5))
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return username, password

def generate_random_json_data():
    return json.dumps({"name": ''.join(random.choices(string.ascii_letters, k=5)), "age": random.randint(18, 60)})

def generate_random_file_contents():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=20))

def generate_random_order_id():
    return random.randint(1000, 9999)

def generate_random_data_for_endpoint(endpoint):
    if 'username' in endpoint:
        return generate_random_user()
    elif '{"name":' in endpoint:
        return generate_random_json_data()
    elif '"file":' in endpoint:
        return generate_random_file_contents()
    elif '"id":' in endpoint:
        return {"id": random.randint(100, 999)}
    # ... (add more cases based on your needs)

def send_request(session, url, method='GET', data=None):
    try:
        response = session.request(method, url, data=data, timeout=5)
        return response
    except requests.RequestException as error:
        logging.error(f"Error accessing {url} with method {method}: {error}")
        return None

def check_endpoints(base_url, endpoints_file='files/Endpoints.txt', concurrency=5, timeout=5):
    with open(endpoints_file, 'r') as file:
        endpoints = [line.strip() for line in file.readlines()]

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        session = setup_session()

        futures = []
        for endpoint in endpoints:
            url = base_url.rstrip('/') + endpoint
            method = 'GET'
            data = None

            if 'Data:' in endpoint:
                data = generate_random_data_for_endpoint(endpoint)
                method = 'POST'

            futures.append(executor.submit(send_request, session, url, method, data))

        results = []
        for future in futures:
            response = future.result(timeout=timeout)
            if response:
                status_code = response.status_code
                headers = response.headers
                results.append((response.request.url, status_code, headers))

        return results