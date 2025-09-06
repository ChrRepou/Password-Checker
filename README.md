# Password Pwned Checker 🔐

This is a simple Python command-line tool that checks if your passwords have been compromised in data breaches. It uses the [Have I Been Pwned](https://haveibeenpwned.com/Passwords) (HIBP) Pwned Passwords API.

The script respects your privacy by using the **k-Anonymity** model, which means your full password is never sent to the API.

---

## How It Works 🤔

1.  **Hashing**: The script takes a password and hashes it using the **SHA-1** algorithm.
2.  **k-Anonymity**: It sends only the **first 5 characters** of the SHA-1 hash to the Pwned Passwords API.
3.  **Receiving Data**: The API responds with a list of all hash suffixes that start with those same 5 characters and have appeared in data breaches.
4.  **Local Check**: The script then checks this list locally to see if the remaining characters of your password's hash (the "tail") are present.
5.  **Reporting**: If a match is found, it reports how many times that password has been exposed. If no match is found, the password is considered safe from the breaches in the HIBP database.

This process ensures your actual password is never exposed to any online service.

---

## Prerequisites 🛠️

* Python 3.x
* The `requests` library

You can install the necessary library using pip:
```bash
pip install requests
```
---

## Usage 🚀

1.  **Create a text file** (e.g., `passwords.txt`) and list all the passwords you want to check, with **one password per line**.

    *Example `passwords.txt` file:*
    ```
    password123
    hello
    supersecret
    123456
    ```

2.  **Run the script** from your terminal, passing the path to your text file as an argument.

    ```bash
    python PasswordChecker.py passwords.txt
    ```

### Example Output

Running the script with the example file above would produce an output similar to this:
```
"password123" was found 3550170 times... you should probably change your password
"hello" was found 455246 times... you should probably change your password
"supersecret" was not found. Carry on!
"123456" was found 23788094 times... you should probably change your password
```
---

## Code Overview 📝

The script contains the following functions:

* `pwned_api_check(password)`: The main function that orchestrates the check for a single password.
* `request_api_data(query_char)`: Sends the first 5 characters of the hash to the HIBP API.
* `get_password_leaks_count(hashes, hash_to_check)`: Parses the API response and checks for a match with the password's hash tail.
* `main(passwords_file)`: Reads passwords from the input file and calls the checking functions for each one.