# modules/web.py
import requests
import os
import validators
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from tabulate import tabulate
import logging
import configparser

# Suppress only the InsecureRequestWarning from urllib3 needed for 'verify=False'
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Read configuration
config = configparser.ConfigParser()
config.read('config/web_config.ini')

headers_file = config.get('web', 'headers_file')
inputs_file = config.get('web', 'inputs_file')
paths_file = config.get('web', 'paths_file')
keywords_file = config.get('web', 'keywords_file')

# Set up logging
logging.basicConfig(filename='web_script.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_headers_file(filename=headers_file):
    with open(filename, 'r') as file:
        headers = [line.strip() for line in file]
    return headers

def read_tampered_inputs(filename=inputs_file):
    with open(filename, 'r') as file:
        tampered_inputs = [line.strip() for line in file]
    return tampered_inputs

def generate_tampered_urls(base_url, tampered_inputs):
    tampered_urls = [f"{base_url.rstrip('/')}/{input_path.lstrip('/')}" for input_path in tampered_inputs]
    return tampered_urls

def check_urls_status(tampered_urls):
    results_tampered = []
    for url in tampered_urls:
        try:
            response = requests.get(url, timeout=5, verify=False)
            status_code = response.status_code
            headers = response.headers

            message = f"Checking tampered URL {url} - Status Code: {status_code}"
            print(message)
            logging.info(message)

            results_tampered.append((url, status_code, headers))

        except requests.RequestException as error:
            message = f"Error accessing {url}: {error}"
            print(message)
            logging.error(message)

    return results_tampered

def check_headers_and_paths(url, paths_file, custom_headers):
    with open(paths_file, 'r') as file:
        paths_to_check = [line.strip() for line in file.readlines()]

    results_scan = []
    for path in paths_to_check:
        full_url = f"{url.rstrip('/')}/{path.lstrip('/')}"
        try:
            if not validators.url(full_url):
                message = f"Invalid URL: {full_url}"
                print(message)
                logging.warning(message)
                continue

            response = requests.get(full_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}, timeout=5, verify=False)
            status_code = response.status_code
            headers = response.headers

            message = f"Checking headers and path for {full_url} - Status Code: {status_code}"
            print(message)
            logging.info(message)

            results_scan.append((full_url, path, status_code, headers))

        except Exception as error:
            message = f"Error accessing {full_url}: {error}"
            print(message)
            logging.error(message)

    return results_scan

def check_webpage_for_keywords(url, keywords_file):
    with open(keywords_file, 'r') as file:
        keywords = [line.strip().lower() for line in file]

    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.text.lower()

        found_keywords = [(url, keyword) for keyword in keywords if keyword in content]

        if found_keywords:
            print("Found sensitive keywords in webpage comments:")
            for found_keyword in found_keywords:
                print(f"- {found_keyword}")
                logging.warning(f"Found sensitive keyword: {found_keyword}")
        else:
            print("No sensitive keywords found in webpage comments.")
            logging.info("No sensitive keywords found in webpage comments.")

        return found_keywords

    except requests.RequestException as error:
        message = f"Error accessing the webpage: {error}"
        print(message)
        logging.error(message)
        return []