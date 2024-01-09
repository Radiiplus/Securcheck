# modules/file_utils.py
import json
import logging

def load_config():
    try:
        with open('config.json', 'r') as config_file:
            return json.load(config_file).get('file_utils', {})
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

config = load_config()
config_path = 'config/config.json' 
def configure_logging():
    logging.basicConfig(
        filename=config.get('log_file', 'webtad.log'),
        level=getattr(logging, config.get('log_level', 'INFO')),
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def read_query_file(filename):
    with open(filename, 'r') as file:
        queries = [line.strip() for line in file]
    return queries

def save_to_file(data, output_file='tampered_results.txt', output_format='plain'):
    try:
        with open(output_file, 'a') as file:
            if output_format == 'json':
                file.write(json.dumps(data, indent=2))
            elif output_format == 'plain':
                for entry in data:
                    file.write(str(entry) + '\n')
            else:
                logging.warning("Unsupported output format. Saving as plain text.")
                for entry in data:
                    file.write(str(entry) + '\n')
        logging.info(f"Tampered results saved to {output_file} in {output_format} format.")
    except Exception as error:
        logging.error(f"Error saving tampered results: {error}")