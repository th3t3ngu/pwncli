#!/usr/bin/env python3

import argparse
import os
import requests
import time
from pathlib import Path

CONFIG_DIR = Path.home() / '.config' / 'pwncli'
API_KEY_FILE = CONFIG_DIR / 'api_key.txt'
HIBP_API_URL = "https://haveibeenpwned.com/api/v3/breachedaccount/"

HEADERS = {
    "User-Agent": "pwncli",
    "hibp-api-key": ""
}

def load_api_key():
    if not API_KEY_FILE.exists():
        print("[-] No API-Key found. Please set with --manage-key.")
        exit(1)
    with open(API_KEY_FILE, 'r') as f:
        key = f.read().strip()
    if not key:
        print("[-] API-Key seems empty please set with --manage-key.")
        exit(1)
    HEADERS["hibp-api-key"] = key

def manage_key():
    if not CONFIG_DIR.exists():
        print(f"[+] Creating config in {CONFIG_DIR}")
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    if API_KEY_FILE.exists():
        with open(API_KEY_FILE, 'r') as f:
            current_key = f.read().strip()
        if current_key:
            print(f"[+] Installed API-Key found: {current_key}")
            choice = input("Do you want to change this key? (y/N): ").strip().lower()
            if choice != 'y':
                print("[*] Keeping current API-Key.")
                return

    new_key = input("Please re-enter your API-Key: ").strip()
    if new_key:
        with open(API_KEY_FILE, 'w') as f:
            f.write(new_key)
        print("[+] New API-Key saved.")
    else:
        print("[-] No Key inserted. Cancelling.")

def check_email(email):
    url = HIBP_API_URL + email
    try:
        response = requests.get(url, headers=HEADERS, params={"truncateResponse": False})
        if response.status_code == 404:
            print(f"[+] {email} wasn't found in a breach.")
        elif response.status_code == 200:
            print(f"[!] {email} was found in the following breach(es):")
            for breach in response.json():
                print(f"  - {breach['Name']} ({breach['BreachDate']}): {breach['Title']}")
        else:
            print(f"[-] Error in request: HTTP {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[-] Critical error in request: {e}")

def check_list(file_path):
    if not os.path.isfile(file_path):
        print(f"[-] File {file_path} not found.")
        return

    with open(file_path, 'r') as f:
        emails = [line.strip() for line in f if line.strip()]

    print(f"[+] Checking {len(emails)} Mail address(es)...\n")
    for i, email in enumerate(emails, 1):
        print(f"=== [{i}/{len(emails)}] {email} ===")
        check_email(email)
        print()
        if i < len(emails):
            time.sleep(4) # otherwise Have I been Pwnd answers with a 429 

def main():
    parser = argparse.ArgumentParser(description="PwnCli – Checking if mails appeared in data breaches via Have I Been Pwned API")
    parser.add_argument('--manage-key', action='store_true', help='show API-Key and/or configure')
    parser.add_argument('--mail', type=str, help='Check a single mail address')
    parser.add_argument('--list', type=str, help='Check a .txt with mail addresses (one address per line)')

    args = parser.parse_args()

    if args.manage_key:
        manage_key()
    elif args.mail:
        load_api_key()
        check_email(args.mail)
    elif args.list:
        load_api_key()
        check_list(args.list)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
