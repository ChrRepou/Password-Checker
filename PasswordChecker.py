import sys
import requests
import hashlib
from pathlib import Path

def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    resp = request_api_data(first5_char)
    return get_password_leaks_count(resp, tail)

def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(f'Error fetching {response.status_code}, check the api and try again')
    return response

def main(passwords_file):
    passwords_filepath = Path(passwords_file)
    with open(passwords_filepath, 'r') as file:
        passwords = file.read().splitlines()
        for password in passwords:
            count = pwned_api_check(password)
            if count:
                print(f'"{password}" was found {count} times... you should probably change your password')
            else:
                print(f'"{password}" was not found. Carry on!')
    file.close()

if __name__ == '__main__':
    try:
        if len(sys.argv) == 2:
            sys.exit(main(sys.argv[1]))
        else:
            print('You should run the script as: PasswordChecker.py <passwords.txt>')
    except Exception as e:
        print(f'An error occurred: {e}')
