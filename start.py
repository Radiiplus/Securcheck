# start.py
import argparse
import logging
from modules import tamper, form_utils, file_utils, web, endpoint, server_info
from tabulate import tabulate

# Define ANSI escape codes for colors
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def print_splash():
    splash_banner = f"""
{Colors.HEADER}âââ³â³âââââ   {Colors.OKBLUE}@Radiiplus{Colors.ENDC}
ââââ£â«â£   ââ
âââ»â»âââââ{Colors.ENDC}
    """
    print(splash_banner)

def write_to_file(output_file, header, data):
    with open(output_file, 'a') as file:
        file.write(f"{Colors.HEADER}{header}{Colors.ENDC}\n")
        file.write(tabulate(data, tablefmt="plain") + "\n\n")

def configure_logging(log_file='main_script.log', log_level=logging.INFO):
    logging.basicConfig(filename=log_file, level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Print splash banner
    print_splash()

    # Argument parsing
    parser = argparse.ArgumentParser(description='Script for web and endpoint checking.')
    parser.add_argument('url', help='Base URL for checking')
    parser.add_argument('--web-output', default='output/output_results_web.txt', help='Output file for Web Checker results')
    parser.add_argument('--endpoint-output', default='output/output_results_endpoint.txt', help='Output file for Endpoint Checker results')
    parser.add_argument('--log-file', default='output/main_script.log', help='Log file for script execution logs')
    parser.add_argument('--log-level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], help='Logging level')
    parser.add_argument('--output-format', default='plain', choices=['plain', 'json', 'csv'], help='Output format for result files')
    args = parser.parse_args()

    # Configure logging
    configure_logging(log_file=args.log_file, log_level=getattr(logging, args.log_level))

    # Web Checker
    custom_headers = web.read_headers_file('files/headers.txt')
    tampered_inputs = web.read_tampered_inputs('files/inputs.txt')
    tampered_urls = web.generate_tampered_urls(args.url, tampered_inputs)

    paths_file = "files/sp.txt"

    results_web = []

    try:
        # Check tampered URLs
        results_tampered = web.check_urls_status(tampered_urls)
        results_web.extend(results_tampered)

        # Check headers and paths
        results_scan = web.check_headers_and_paths(args.url, paths_file, custom_headers)
        results_web.extend(results_scan)

        # Check webpage for keywords
        keywords_file = "files/keywords.txt"
        results_keywords = web.check_webpage_for_keywords(args.url, keywords_file)
        results_web.extend(results_keywords)

        # Output Web Checker Results
        write_to_file(args.web_output, "Web Checker Results", results_web)
        logging.info("Web Checker results have been saved.")

    except Exception as e:
        logging.error(f"Web Checker encountered an error: {e}")

    # Endpoint Checker
    try:
        concurrency = int(input("Enter the concurrency level for endpoint checking: "))
        timeout = int(input("Enter the timeout (in seconds) for endpoint checking: "))
        results_endpoint = endpoint.check_endpoints(args.url, concurrency=concurrency, timeout=timeout)

        # Output Endpoint Checker Results
        write_to_file(args.endpoint_output, "Endpoint Checker Results", results_endpoint)
        logging.info("Endpoint Checker results have been saved.")

    except Exception as e:
        logging.error(f"Endpoint Checker encountered an error: {e}")

    # Server Information Checker
    try:
        server_info_result = server_info.get_server_info(args.url)
        print(f"{Colors.OKBLUE}Server Information: {server_info_result}{Colors.ENDC}")
        logging.info(f"Server Information: {server_info_result}")

    except Exception as e:
        logging.error(f"Server Information Checker encountered an error: {e}")

    print(f"{Colors.OKGREEN}Results have been saved to output files.{Colors.ENDC}")

if __name__ == "__main__":
    main()