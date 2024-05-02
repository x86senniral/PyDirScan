import requests
import re
import argparse

class Colors:
    GREEN = '\033[32m'
    RED = '\033[31m'
    RESET = '\033[0m'

def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|https)://'
        r'(?:\S+(?::\S*)?@)?'
        r'(?:localhost|[\w.-]+(?:\.\w+)+)'
        r'(?::\d{2,5})?'
        r'(?:/?|[/?]\S*)?$', re.IGNORECASE)
    return re.match(regex, url) is not None

def create_parser():
    parser = argparse.ArgumentParser(description='Directory Scanner')
    parser.add_argument('--dir', type=str, help='Direct URL input. Example: --dir https://example.com')
    return parser

parser = create_parser()
args = parser.parse_args()

if not args.dir:
    parser.print_help()
    exit()

url = args.dir
customfile = input('Custom files? (leave empty if not): ')

if not is_valid_url(url):
    print(f"{Colors.RED}Invalid URL format. Ensure it starts with http:// or https://{Colors.RESET}")
    exit()

def scan():
    filename = customfile if customfile else 'directory-list-2.3-big.txt'
    with open(filename, 'r') as file:
        lines = file.readlines()
        total_lines = len(lines)
        count = 0
        found_count = 0
        forbidden_count = 0

        print("""
----------------------------------------------------------
███████████████████████████████████████████████████████
█▄─▄▄─█▄─█─▄█▄─▄▄▀█▄─▄█▄─▄▄▀█─▄▄▄▄█─▄▄▄─██▀▄─██▄─▀█▄─▄█
██─▄▄▄██▄─▄███─██─██─███─▄─▄█▄▄▄▄─█─███▀██─▀─███─█▄▀─██
▀▄▄▄▀▀▀▀▄▄▄▀▀▄▄▄▄▀▀▄▄▄▀▄▄▀▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▀▄▄▀▄▄▄▀▀▄▄▀        
----------------------------------------------------------
DIR SCANNER
----------------------------------------------------------
""")

        for directory in lines:
            directory = directory.strip()
            new_url = f"{url.rstrip('/')}/{directory.lstrip('/')}"
            count += 1
            try:
                response = requests.get(new_url)
                if response.status_code == 200:
                    found_count += 1
                    print(f"{Colors.GREEN}Found #{found_count} with 200 code status: {new_url}{Colors.RESET}")
                elif response.status_code == 403:
                    forbidden_count += 1
                    print(f"{Colors.RED}Forbidden #{forbidden_count}: {new_url}{Colors.RESET}")
                print(f"GOING THROUGH DIRS: {count} / {total_lines}", end='\r')
            except requests.exceptions.ConnectionError:
                continue

        print("\nScan completed.")

scan()
