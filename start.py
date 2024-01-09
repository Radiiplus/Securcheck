import argparse
import logging
from modules import tamper, form_utils, file_utils, web, endpoint, server_info
from tabulate import tabulate
from colorama import Fore, Style
import time

Fore.__dict__['RESET'] = Style.RESET_ALL
Fore.__dict__['autoreset'] = True

LOG_COLORS = {
    'DEBUG': Fore.CYAN,
    'INFO': Fore.GREEN,
    'WARNING': Fore.YELLOW,
    'ERROR': Fore.RED
}

def colored_log(level, message):
    color = LOG_COLORS.get(level, Fore.RESET)
    print(f"{color}[{level}] {message}{Fore.RESET}")

def write_to_file(output_file, header, data):
    with open(output_file, 'a') as file:
        file.write(header + "\n")
        file.write(tabulate(data, tablefmt="plain") + "\n\n")

def configure_logging(log_file='main_script.log', log_level=logging.INFO):
    logging.basicConfig(filename=log_file, level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

def display_splash():
    splash = r"""    
┓┏┳┳┓┏┓┏┓
┃┃┃┣┫┣ ┗┓
┗┛┻┻┛┗┛┗┛
    """    
    print(Fore.MAGENTA + splash + Fore.RESET)
    print(Fore.BLUE + "Powered by Radiiplus - https://x.com/radiiplus" + Fore.RESET)

def request_concurrency_timeout():
    concurrency = int(input("Enter the concurrency level: "))
    timeout = int(input("Enter the timeout in seconds: "))
    return concurrency, timeout

def main():
    display_splash()
    
    # Request concurrency and timeout inputs
    concurrency, timeout = request_concurrency_timeout()

    parser = argparse.ArgumentParser(description='Script for web and endpoint checking.')
    parser.add_argument('url', help='Base URL for checking')
    parser.add_argument('--web-output', default='output_results_web.txt', help='Output file for Web Checker results')
    parser.add_argument('--endpoint-output', default='output_results_endpoint.txt', help='Output file for Endpoint Checker results')
    parser.add_argument('--log-file', default='main_script.log', help='Log file for script execution logs')
    parser.add_argument('--log-level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], help='Logging level')
    parser.add_argument('--output-format', default='plain', choices=['plain', 'json', 'csv'], help='Output format for result files')
    parser.add_argument('--concurrency', type=int, default=concurrency, help='Concurrency level for endpoint checking')
    parser.add_argument('--timeout', type=int, default=timeout, help='Timeout (in seconds) for endpoint checking')
    args = parser.parse_args()

    configure_logging(log_file=args.log_file, log_level=getattr(logging, args.log_level))

    server = server_info.get_server_info(args.url)
    print(Fore.BLUE + f"Server Information: {server}" + Fore.RESET)

    custom_headers = web.read_headers_file('files/headers.txt')
    tampered_inputs = web.read_tampered_inputs('files/inputs.txt')
    tampered_urls = web.generate_tampered_urls(args.url, tampered_inputs)

    paths_file = "files/sp.txt"
    results_web = []

    try:
        results_tampered = web.check_urls_status(tampered_urls)
        results_web.extend(results_tampered)

        results_scan = web.check_headers_and_paths(args.url, paths_file, custom_headers)
        results_web.extend(results_scan)

        keywords_file = "files/keywords.txt"
        results_keywords = web.check_webpage_for_keywords(args.url, keywords_file)
        results_web.extend(results_keywords)

        write_to_file(args.web_output, "Web Checker Results", results_web)
        colored_log('INFO', "Web Checker results have been saved.")

    except Exception as e:
        colored_log('ERROR', f"Web Checker encountered an error: {e}")

    try:
        results_endpoint = endpoint.check_endpoints(args.url, concurrency=args.concurrency, timeout=args.timeout)
        write_to_file(args.endpoint_output, "Endpoint Checker Results", results_endpoint)
        colored_log('INFO', "Endpoint Checker results have been saved.")

    except Exception as e:
        colored_log('ERROR', f"Endpoint Checker encountered an error: {e}")

    print(Fore.CYAN + "Results have been saved to output files." + Fore.RESET)

if __name__ == "__main__":
    main()