import os
import signal
import sys
import math
from colorama import Fore, Style
import re
import time
import getpass
from datetime import datetime
import requests
from requests.exceptions import RequestException, ConnectionError
from cryptography.fernet import Fernet
import hashlib
import statistics
from scipy.stats import skew, kurtosis

PASSWORD_FILE = "password.txt"
SALT_LENGTH = 16
MAX_LOGIN_ATTEMPTS = 3
LOGIN_ATTEMPT_DELAY = 2
VERIFICATION_FILE = "verification.txt"
KEY_FILE = "key.key"

def clear_terminal():
    if os.name == "posix":  # Unix/Linux/MacOS
        os.system("clear")
    elif os.name == "nt":  # Windows
        os.system("cls")

def print_with_delay(text, delay_per_letter):
    for letter in text:
        print(letter, end='', flush=True)
        time.sleep(delay_per_letter / 1000)  # Convert milliseconds to seconds

tool = """
\033[36m
    _   __     __  __              __  ___      __  __
   / | / /__  / /_/ /_  ___  _____/  |/  /___ _/ /_/ /_
  /  |/ / _ \/ __/ __ \/ _ \/ ___/ /|_/ / __ `/ __/ __ |
 / /|  /  __/ /_/ / / /  __/ /  / /  / / /_/ / /_/ / / /
/_/ |_/\___/\__/_/ /_/\___/_/  /_/  /_/\__,_/\__/_/ /_/
                                    By Navi
\033[0m
"""
clear_terminal()
print_with_delay(tool, 20)  # Adjust the delay per letter (in milliseconds)
print()


def signal_handler(sig, frame):
    exit_message = "Exiting the calculator..."
    print(f"\n{Fore.MAGENTA}", end='', flush=True)
    print_with_delay(exit_message, 40)  # Adjust the delay per letter (in milliseconds) as desired
    print(Style.RESET_ALL, "\n")
    time.sleep(2)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def generate_salt():
    return os.urandom(SALT_LENGTH)

def hash_password(password, salt):
    salted_password = password.encode() + salt
    hashed_password = hashlib.pbkdf2_hmac("sha256", salted_password, salt, 100000)
    return hashed_password

def encrypt_password(password, key):
    cipher_suite = Fernet(key)
    encrypted_password = cipher_suite.encrypt(password)
    return encrypted_password

def decrypt_password(encrypted_password, key):
    try:
        cipher_suite = Fernet(key)
        decrypted_password = cipher_suite.decrypt(encrypted_password)
        return decrypted_password
    except Exception as e:
        print("Error occurred while decrypting the password:", str(e))
        sys.exit(1)

def encrypt_verification_data(data, key):
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

def decrypt_verification_data(encrypted_data, key):
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    return decrypted_data

def enter_password():
    attempts = 0
    while attempts < MAX_LOGIN_ATTEMPTS:
        clear_terminal()
        print(tool)
        password = getpass.getpass(f"{Fore.CYAN}Enter password:{Style.RESET_ALL} ")
        with open(PASSWORD_FILE, "rb") as file:
            saved_password = file.read()
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
        decrypted_password = decrypt_password(saved_password[SALT_LENGTH:], key)
        if hash_password(password, saved_password[:SALT_LENGTH]) == decrypted_password:
            message = "Access granted! Proceeding with the program..."
            print(f"\n{Fore.GREEN}", end='', flush=True)
            print_with_delay(message, 40)  # Adjust the delay per letter (in milliseconds) as desired
            print(Style.RESET_ALL, "\n")
            time.sleep(10)
            return
        else:
            message = "Password Incorrect! Access Denied.."
            print(f"\n{Fore.RED}", end='', flush=True)
            print_with_delay(message, 40)  # Adjust the delay per letter (in milliseconds) as desired
            print(Style.RESET_ALL, "\n")
            attempts += 1
            if attempts < MAX_LOGIN_ATTEMPTS:
                time.sleep(2)
                message = "Please try again.."
                print(f"\n{Fore.MAGENTA}", end='', flush=True)
                print_with_delay(message, 40)  # Adjust the delay per letter (in milliseconds) as desired
                print(Style.RESET_ALL, "\n")
                time.sleep(LOGIN_ATTEMPT_DELAY)
    time.sleep(2)
    exit_message = "Maximum login attempts exceeded! Exiting..."
    print(f"\n{Fore.RED}", end='', flush=True)
    print_with_delay(exit_message, 40)  # Adjust the delay per letter (in milliseconds) as desired
    print(Style.RESET_ALL, "\n")
    sys.exit(1)

def create_password():
    while True:
        clear_terminal()
        print(tool)
        password = getpass.getpass(f"{Fore.CYAN}Create a new password:{Style.RESET_ALL} ")
        verify_password = getpass.getpass(f"{Fore.CYAN}Verify your password:{Style.RESET_ALL} ")

        if password == verify_password:
            salt = generate_salt()
            hashed_password = hash_password(password, salt)
            key = Fernet.generate_key()

            encrypted_password = encrypt_password(hashed_password, key)
            with open(PASSWORD_FILE, "wb") as file:
                file.write(salt + encrypted_password)

            with open(KEY_FILE, "wb") as key_file:
                key_file.write(key)

            time.sleep(5)
            message = "Password created and saved successfully!"
            print(f"\n{Fore.GREEN}", end='', flush=True)
            print_with_delay(message, 40)  # Adjust the delay per letter (in milliseconds) as desired
            print(Style.RESET_ALL, "\n")
            print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")

            favorite_color = input(f"{Fore.CYAN}Enter your favorite color:{Style.RESET_ALL} ")
            pet_name = input(f"{Fore.CYAN}Enter your pet's name:{Style.RESET_ALL} ")
            city_of_birth = input(f"{Fore.CYAN}Enter the city of your birth:{Style.RESET_ALL} ")

            verification_data = f"{favorite_color},{pet_name},{city_of_birth}"

            message = "Account created successfully"
            print(f"\n{Fore.GREEN}", end='', flush=True)
            print_with_delay(message, 40)  # Adjust the delay per letter (in milliseconds) as desired
            print(Style.RESET_ALL, "\n")
            encrypted_verification_data = encrypt_verification_data(verification_data, key)

            with open(VERIFICATION_FILE, "wb") as verification_file:
                verification_file.write(encrypted_verification_data)

            break
        else:
            message = "Password did not match, please try again.."
            print(f"\n{Fore.RED}", end='', flush=True)
            print_with_delay(message, 40)  # Adjust the delay per letter (in milliseconds) as desired
            print(Style.RESET_ALL, "\n")

def create_new_password():
    while True:
        clear_terminal()
        print(tool)
        password = getpass.getpass(f"{Fore.CYAN}Create a new password:{Style.RESET_ALL} ")
        verify_password = getpass.getpass(f"{Fore.CYAN}Verify your password:{Style.RESET_ALL} ")

        if password == verify_password:
            salt = generate_salt()
            hashed_password = hash_password(password, salt)
            key = Fernet.generate_key()

            encrypted_password = encrypt_password(hashed_password, key)
            with open(PASSWORD_FILE, "wb") as file:
                file.write(salt + encrypted_password)

            with open(KEY_FILE, "wb") as key_file:
                key_file.write(key)

            time.sleep(5)
            message = "Password created and saved successfully!"
            print(f"\n{Fore.GREEN}", end='', flush=True)
            print_with_delay(message, 40)  # Adjust the delay per letter (in milliseconds) as desired
            print(Style.RESET_ALL, "\n")
            print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")

            favorite_color = input(f"{Fore.CYAN}Enter your favorite color:{Style.RESET_ALL} ")
            pet_name = input(f"{Fore.CYAN}Enter your pet's name:{Style.RESET_ALL} ")
            city_of_birth = input(f"{Fore.CYAN}Enter the city of your birth:{Style.RESET_ALL} ")

            verification_data = f"{favorite_color},{pet_name},{city_of_birth}"
            message = "Password successfully changed!!"
            print(f"\n{Fore.GREEN}", end='', flush=True)
            print_with_delay(message, 40)  # Adjust the delay per letter (in milliseconds) as desired
            print(Style.RESET_ALL, "\n")
            encrypted_verification_data = encrypt_verification_data(verification_data, key)

            with open(VERIFICATION_FILE, "wb") as verification_file:
                verification_file.write(encrypted_verification_data)

            break
        else:
            message = "Password did not match, please try again.."
            print(f"\n{Fore.RED}", end='', flush=True)
            print_with_delay(message, 40)  # Adjust the delay per letter (in milliseconds) as desired
            print(Style.RESET_ALL, "\n")

def verify_user():
    attempts = 0
    while attempts < MAX_LOGIN_ATTEMPTS:
        favorite_color = input(f"{Fore.CYAN}Enter your favorite color:{Style.RESET_ALL} ")
        pet_name = input(f"{Fore.CYAN}Enter your pet's name:{Style.RESET_ALL} ")
        city_of_birth = input(f"{Fore.CYAN}Enter the city of your birth:{Style.RESET_ALL} ")

        with open(VERIFICATION_FILE, "rb") as verification_file:
            encrypted_verification_data = verification_file.read()

        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()

        decrypted_verification_data = decrypt_verification_data(encrypted_verification_data, key)
        saved_favorite_color, saved_pet_name, saved_city_of_birth = decrypted_verification_data.split(",")

        if (
            favorite_color.lower() == saved_favorite_color.lower()
            and pet_name.lower() == saved_pet_name.lower()
            and city_of_birth.lower() == saved_city_of_birth.lower()
        ):
            time.sleep(3)
            message = "User successfully verified!!"
            print(f"\n{Fore.GREEN}", end='', flush=True)
            print_with_delay(message, 40)  # Adjust the delay per letter (in milliseconds) as desired
            print(Style.RESET_ALL, "\n")
            break
        else:
            time.sleep(3)
            message = "Verification failed!!"
            print(f"\n{Fore.RED}", end='', flush=True)
            print_with_delay(message, 40)  # Adjust the delay per letter (in milliseconds) as desired
            print(Style.RESET_ALL, "\n")
            attempts += 1
            if attempts < MAX_LOGIN_ATTEMPTS:
                message = "Please try again.."
                print(f"\n{Fore.MAGENTA}", end='', flush=True)
                print_with_delay(exit_message, 40)  # Adjust the delay per letter (in milliseconds) as desired
                print(Style.RESET_ALL, "\n")
                time.sleep(LOGIN_ATTEMPT_DELAY)
    else:
        exit_message = "Maximum login attempts exceeded. Exiting..."
        print(f"\n{Fore.RED}", end='', flush=True)
        print_with_delay(exit_message, 40)  # Adjust the delay per letter (in milliseconds) as desired
        print(Style.RESET_ALL, "\n")
        sys.exit(1)

def forgot_password():
    choice = input(f"{Fore.YELLOW}Do you want to reset your password? (y/n):{Style.RESET_ALL} ").lower()
    if choice == "y":
        clear_terminal()
        print(tool)
        verify_user()
        time.sleep(3)
        create_new_password()
        enter_password()
    else:
        exit_message = "Password reset canceled. Exiting...."
        print(f"\n{Fore.MAGENTA}", end='', flush=True)
        print_with_delay(exit_message, 40)  # Adjust the delay per letter (in milliseconds) as desired
        print(Style.RESET_ALL, "\n")
        sys.exit(0)

def password_already_created():
    return os.path.exists(PASSWORD_FILE)

def login_form():
    if password_already_created():
        enter_password()
    else:
        message = "You haven't created an account yet!!"
        print(f"{Fore.RED}", end='', flush=True)
        print_with_delay(message, 40)  # Adjust the delay per letter (in milliseconds) as desired
        print(Style.RESET_ALL, "\n")
        time.sleep(2)
        choice = input(f"{Fore.YELLOW}Do you want to create a password now? (y/n):{Style.RESET_ALL} ").lower()
        if choice == "y":
            create_password()
            enter_password()
        else:
            exit_message = "Login cancelled. Exiting...."
            print(f"\n{Fore.MAGENTA}", end='', flush=True)
            print_with_delay(exit_message, 40)  # Adjust the delay per letter (in milliseconds) as desired
            print(Style.RESET_ALL, "\n")
            sys.exit(0)

def main():
    while True:
        choice = input(f"{Fore.CYAN}1. Login\n2. Forgot Password\n3. Exit\n\n>{Style.RESET_ALL} ")
        if choice == "1":
            login_form()
        elif choice == "2":
            forgot_password()
        elif choice == "3":
            exit_message = "Exiting the calculator..."
            print(f"\n{Fore.MAGENTA}", end='', flush=True)
            print_with_delay(exit_message, 40)  # Adjust the delay per letter (in milliseconds) as desired
            print(Style.RESET_ALL, "\n")
            sys.exit(1)
        else:
            exit_message = "Invalid choice!!"
            print(f"\n{Fore.MAGENTA}", end='', flush=True)
            print_with_delay(exit_message, 40)  # Adjust the delay per letter (in milliseconds) as desired
            print(Style.RESET_ALL, "\n")
            clear_terminal()
            print(tool)

if __name__ == "__main__":
    main()

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        print(f"{Fore.MAGENTA}Error: You can't divide a number by zero.{Style.RESET_ALL}")
        return None
    return x / y

def power(x, y):
    return x ** y

def square_root(x):
    return math.sqrt(x)

def logarithm(x, base):
    return math.log(x, base)

def sin(x):
    return math.sin(math.radians(x))

def cos(x):
    return math.cos(math.radians(x))

def tan(x):
    return math.tan(math.radians(x))

def remainder(x, y):
    return x % y

def evaluate_expression(expression):
    expression = re.sub(r'\s', '', expression)
    pattern = r'(\d+\.?\d*)|([+\-*/^])'
    tokens = re.findall(pattern, expression)
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    numbers = []
    operators = []

    def perform_operation():
        operator = operators.pop()
        num2 = float(numbers.pop())
        num1 = float(numbers.pop())

        if operator == '+':
            numbers.append(num1 + num2)
        elif operator == '-':
            numbers.append(num1 - num2)
        elif operator == '*':
            numbers.append(num1 * num2)
        elif operator == '/':
            numbers.append(num1 / num2)
        elif operator == '^':
            numbers.append(num1 ** num2)

    for token in tokens:
        if re.match(pattern, token[0]):
            numbers.append(token[0])
        else:
            while operators and precedence[token[1]] <= precedence[operators[-1]]:
                perform_operation()
            operators.append(token[1])

    while operators:
        perform_operation()

    return numbers[0]

def calculate_pi(iterations):
    pi = 0.0
    sign = 1

    for i in range(iterations):
        denominator = (2 * i) + 1
        pi += sign * (1 / denominator)
        sign *= -1

    pi *= 4

    return pi

def calculate_e(iterations2):
    e = 0
    for i in range(iterations2):
        e += 1 / math.factorial(i)
    return e

def meters_to_kilometers(meters):
    kilometers = meters / 1000
    return kilometers

def kilometers_to_meters(kilometers):
    meters = kilometers * 1000
    return meters

speed_of_light = 299792458

def calculate_light_years(distance):
    time = distance / speed_of_light
    light_years = time / (365 * 24 * 60 * 60)
    return light_years

def convert_light_years(light_years):
    time = light_years * (365 * 24 * 60 * 60)
    distance = time * speed_of_light
    return distance

def avogadro(number):
    exponent = 0

    while abs(number) < 1:
        number *= 10
        exponent -= 1

    while abs(number) >= 10:
        number /= 10
        exponent += 1

    return number, exponent

def decimal_to_binary(decimal):
    binary = ""
    while decimal > 0:
        binary = str(decimal % 2) + binary
        decimal //= 2
    return binary

def binary_to_decimal(binary):
    decimal = 0
    power = 0
    for digit in reversed(binary):
        decimal += int(digit) * (2 ** power)
        power += 1
    return decimal

def decimal_to_hexadecimal(decimal):
    hexadecimal = ""
    while decimal > 0:
        remainder = decimal % 16
        if remainder < 10:
            hexadecimal = str(remainder) + hexadecimal
        else:
            hexadecimal = chr(ord('A') + remainder - 10) + hexadecimal
        decimal //= 16
    return hexadecimal

def hexadecimal_to_decimal(hexadecimal):
    decimal = 0
    power = 0
    for digit in reversed(hexadecimal):
        if digit.isdigit():
            decimal += int(digit) * (16 ** power)
        else:
            decimal += (ord(digit.upper()) - ord('A') + 10) * (16 ** power)
        power += 1
    return decimal

def decimal_to_octal(decimal):
    octal = ""
    while decimal > 0:
        octal = str(decimal % 8) + octal
        decimal //= 8
    return octal

def octal_to_decimal(octal):
    for digit in str(octal):
        if digit not in "01234567":
            print(f"{Fore.RED}Error: Invalid octal number. Please enter a number within the range of 0-7.{Style.RESET_ALL}")
            return None

    decimal = 0
    power = 0
    for digit in reversed(octal):
        decimal += int(digit) * (8 ** power)
        power += 1
    return decimal

def binary_to_octal(binary):
    decimal = binary_to_decimal(binary)
    octal = decimal_to_octal(decimal)
    return octal

def octal_to_binary(octal):
    for digit in str(octal):
        if digit not in "01234567":
            print(f"{Fore.RED}Error: Invalid octal number. Please enter a number within the range of 0-7.{Style.RESET_ALL}")
            return None

    decimal = octal_to_decimal(octal)
    binary = decimal_to_binary(decimal)
    return binary

def hexadecimal_to_binary(hexadecimal):
    decimal = hexadecimal_to_decimal(hexadecimal)
    binary = decimal_to_binary(decimal)
    return binary

def binary_to_hexadecimal(binary):
    decimal = binary_to_decimal(binary)
    hexadecimal = decimal_to_hexadecimal(decimal)
    return hexadecimal

def miles_to_km(miles):
    km = miles * 1.60934
    return km

def km_to_miles(km):
    miles = km / 1.60934
    return miles

def meters_to_miles(meters):
    miles = meters / 1609.34
    return miles

def miles_to_meters(miles):
    meters = miles * 1609.34
    return meters

def text_to_binary(text):
    binary = ''
    for char in text:
        binary += format(ord(char), '08b') + ' '  # Convert each character to 8-bit binary representation
    return binary.rstrip()  # Remove trailing whitespace

def binary_to_text(binary):
    binary = binary.replace(' ', '')  # Remove any whitespace
    text = ''
    for i in range(0, len(binary), 8):
        char_binary = binary[i:i+8]
        text += chr(int(char_binary, 2))  # Convert 8-bit binary representation to character
    return text

def octal_to_hexadecimal(octal_number):
    for digit in str(octal_number):
        if digit not in "01234567":
            print(f"{Fore.RED}Error: Invalid octal number. Please enter a number within the range of 0-7.{Style.RESET_ALL}")
            return None

    decimal_number = int(str(octal_number), 8)
    hexadecimal_number = hex(decimal_number)[2:].upper()
    return hexadecimal_number

def hexadecimal_to_octal(hexadecimal_number):
    decimal_number = int(str(hexadecimal_number), 16)
    octal_number = oct(decimal_number)[2:]  # Remove the prefix "0o"
    return octal_number

def meters_to_feet(meters):
    feet = meters * 3.28084
    return feet

def feet_to_meters(feet):
    meters = feet / 3.28084
    return meters

def kg_to_lb(weight):
    return weight * 2.20462

def lb_to_kg(weight):
    return weight * 0.453592

def kg_to_g(weight):
    return weight * 1000

def g_to_kg(weight):
    return weight * 0.001

def kg_to_ton(weight):
    return weight * 0.00110231

def ton_to_kg(weight):
    return weight * 907.185

def lb_to_g(weight):
    return kg_to_g(lb_to_kg(weight))

def g_to_lb(weight):
    return kg_to_lb(g_to_kg(weight))

def lb_to_ton(weight):
    return kg_to_ton(lb_to_kg(weight))

def ton_to_lb(weight):
    return kg_to_lb(ton_to_kg(weight))

def g_to_ton(weight):
    return kg_to_ton(g_to_kg(weight))

def ton_to_g(weight):
    return kg_to_g(ton_to_kg(weight))

def stone_to_kg(weight):
    return weight * 6.35029

def kg_to_stone(weight):
    return weight * 0.157473

def has_internet_connection():
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except requests.ConnectionError:
        return False

def get_exchange_rate(from_currency, to_currency):
    if not has_internet_connection():
        print(f"{Fore.RED}No internet connection!{Style.RESET_ALL}")
        return None

    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(url)
        data = response.json()
        rates = data["rates"]
        exchange_rate = rates[to_currency]
        return exchange_rate
    except (RequestException, KeyError):
        return None

def convert_currency(amount, from_currency, to_currency):
    exchange_rate = get_exchange_rate(from_currency, to_currency)
    if exchange_rate is None:
        return None
    converted_amount = amount * exchange_rate
    return converted_amount

def convert_to_currency(amount, from_currency, to_currency):
    if not has_internet_connection():
        print(f"{Fore.RED}No internet connection!{Style.RESET_ALL}")
        return None

    try:
        url = f"https://min-api.cryptocompare.com/data/price?fsym={from_currency}&tsyms={to_currency}"
        response = requests.get(url)
        data = response.json()
        if to_currency in data:
            conversion_rate = data[to_currency]
            converted_amount = amount * conversion_rate
            return converted_amount
    except RequestException:
        return None

def binary_calculator(expression):
    # Separate the binary numbers and operators
    parts = re.findall(r'[01]+|[-+*/]', expression)
    binaries = [part for part in parts if all(bit in '01' for bit in part)]
    operators = [part for part in parts if part not in binaries]

    # Convert the binary numbers to decimal and perform calculations
    decimals = [int(binary.rstrip('b'), 2) for binary in binaries]
    result_decimal = decimals[0]

    is_division = False  # Variable to track if division operation is used

    for i in range(1, len(decimals)):
        operator = operators[i - 1]
        if operator == '+':
            result_decimal += decimals[i]
        elif operator == '-':
            result_decimal -= decimals[i]
        elif operator == '*':
            result_decimal *= decimals[i]
        elif operator == '/':
            if decimals[i] == 0:
                print(f"{Fore.RED}Error: Cannot divide by zero.{Style.RESET_ALL}")
                return ""
            result_decimal //= decimals[i]
            is_division = True  # Set is_division to True for division operation

    output = "Binary value:\n"
    for j in range(len(binaries)):
        output += f"{binaries[j]} "
        if j < len(operators):
            output += f"{operators[j]} "
    output += f"= {bin(result_decimal)[2:]}\n"

    if is_division:
        remainder = decimals[0] % decimals[1]
        output += f"Remainder(Binary): {bin(remainder)[2:]}\n\n"
    else:
        output += "\n"

    output += "Decimal value:\n"
    for j in range(len(decimals)):
        output += f"{decimals[j]} "
        if j < len(operators):
            output += f"{operators[j]} "
    output += f"= {result_decimal}\n"

    if is_division:
        remainder = decimals[0] % decimals[1]
        output += f"Remainder(Decimal): {remainder}\n"
    else:
        output += "\n"

    return output.replace("b", "")  # Remove 'b' from the binary result

def calculate_mean(data):
    return sum(data) / len(data)

def calculate_median(data):
    return statistics.median(data)

def calculate_mode(data):
    return statistics.mode(data)

def calculate_standard_deviation(data):
    return statistics.stdev(data)

def calculate_variance(data):
    return statistics.variance(data)

def calculate_range(data):
    return max(data) - min(data)

def calculate_quartiles(data):
    sorted_data = sorted(data)
    n = len(data)
    q1 = sorted_data[n // 4]
    q2 = sorted_data[n // 2]
    q3 = sorted_data[(3 * n) // 4]
    return q1, q2, q3

def calculate_interquartile_range(data):
    q1, _, q3 = calculate_quartiles(data)
    return q3 - q1

def calculate_skewness(data):
    return skew(data)

def calculate_kurtosis(data):
    return kurtosis(data)

def determine_kurtosis_type(kurtosis_value):
    if kurtosis_value > 0:
        return "Leptokurtic"
    elif kurtosis_value < 0:
        return "Platykurtic"
    else:
        return "Mesokurtic"

def calculate_z_test(data, hypothesized_mean, population_std_dev):
    sample_mean = calculate_mean(data)
    n = len(data)
    z_score = (sample_mean - hypothesized_mean) / (population_std_dev / math.sqrt(n))
    return z_score

def save_calculation(expression, result):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    calculation = f"{timestamp}: {expression} = {result}\n"

    with open("calculations.txt", "a") as file:
        file.write(calculation)

    print(f"{Fore.GREEN}Calculation saved to calculations.txt.{Style.RESET_ALL}")

def save_calculation2(expression, result, statement):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    calculation = f"{timestamp}: {expression} = {result} {statement}\n"

    with open("calculations.txt", "a") as file:
        file.write(calculation)

    print(f"{Fore.GREEN}Calculation saved to calculations.txt.{Style.RESET_ALL}")

def save_calculation3(expression, result, statement):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    calculation = f"{timestamp}: {expression} = {result:.3f} * 10^{statement}\n"

    with open("calculations.txt", "a") as file:
        file.write(calculation)

    print(f"{Fore.GREEN}Calculation saved to calculations.txt.{Style.RESET_ALL}")

def save_calculation4(expression):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    calculation = f"{timestamp}: {expression}\n"

    with open("calculations.txt", "a") as file:
        file.write(calculation)

    print(f"{Fore.GREEN}Calculation saved to calculations.txt.{Style.RESET_ALL}")

def view_calculations():
    try:
        with open("calculations.txt", "r") as file:
            calculations = file.read()
            clear_terminal()
            print(tool)
            print(f"{Fore.BLUE}Previous Calculations:{Style.RESET_ALL}{Fore.YELLOW}\n{calculations}{Style.RESET_ALL}")
    except FileNotFoundError:
        clear_terminal()
        print(tool)
        print(f"{Fore.MAGENTA}No calculations found.{Style.RESET_ALL}\n")

def scientific_calculator():
    options = """
Mathematical Operators
1. Add
2. Subtract
3. Multiply
4. Divide
5. Remainder
6. Power
7. Square Root

Mathematical Functions
8. Logarithm
9. Sin
10. Cos
11. Tangent
12. Pi
13. Euler's Number
14. Avogadros's Number

Conversion Methods
15. Decimal to Binary
16. Binary to Decimal
17. Binary to Hexadecimal
18. Hexadecimal to Binary
19. Binary to Octal
20. Octal to Binary
21. Decimal to Hexadecimal
22. Hexadecimal to Decimal
23. Decimal to Octal
24. Octal to Decimal
25. Text to Binary
26. Binary to Text
27. Octal to Hexadecimal
28. Hexadecimal to Octal

Distance Measures
29. Meters to Kilometers
30. Kilometers to Meters
31. Kilometers to Light-years
32. Light-years to Kilometers
33. Miles to Kilometers
34. Kilometers to Miles
35. Meters to Miles
36. Miles to Meters
37. Meters to Feet
38. Feet to Meters

Weighing Scales
39. Kilograms to Pounds
40. Pounds to Kilograms
41. Kilograms to Grams
42. Grams to Kilograms
43. Kilograms to Ton
44. Ton to Kilograms
45. Pounds to Grams
46. Grams to Pounds
47. Pounds to Ton
48. Ton to Pounds
49. Grams To Ton
50. Ton to Grams
51. Stone to Kilograms
52. Kilograms to Stone

Statistics and Probability
53. Mean
54. Median
55. Mode
56. Standard Deviation
57. Variance
58. Range
59. Quartiles
60. Interquartile Range
61. Skewness
62. Kurtosis
63. Z-test

Currency
64. Currency Converter
65. Crytocurrency Converter

Other Options
66. Binary Calculator
67. Evaluate Mixed Operation
68. View Previous Calculations

Type 'Exit' to quit the program.
    """
    try:
        clear_terminal()
        while True:
            choice = input(f"{Fore.CYAN}\n>{Style.RESET_ALL} ")

            if choice.lower() == "exit":
                print(f"{Fore.MAGENTA}Exiting the calculator...{Style.RESET_ALL}")
                time.sleep(5)
                print(f"{Fore.CYAN}You're really suck in math! Well me too!:){Style.RESET_ALL}")
                break
            elif choice.lower() == "h" or choice.lower() == "help":
                clear_terminal()
                print(tool)
                print(f"{Fore.BLUE}", options)
            elif choice.isdigit():
                choice = int(choice)
                if choice >= 1 and choice <= 11:
                    if choice <= 5:
                        x = float(input(f"{Fore.CYAN}Enter the first number:{Style.RESET_ALL} "))
                        y = float(input(f"{Fore.CYAN}Enter the second number:{Style.RESET_ALL} "))

                        if choice == 1:
                            print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                            result = add(x, y)
                            print(f"{Fore.BLUE}Result: {add(x, y)}{Style.RESET_ALL}\n")
                            save_calculation(f"{x} + {y}", result)
                        elif choice == 2:
                            print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                            result = subtract(x, y)
                            print(f"{Fore.BLUE}Result: {subtract(x, y)}{Style.RESET_ALL}\n")
                            save_calculation(f"{x} - {y}", result)
                        elif choice == 3:
                            print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                            result = multiply(x, y)
                            print(f"{Fore.BLUE}Result: {multiply(x, y)}{Style.RESET_ALL}\n")
                            save_calculation(f"{x} * {y}", result)
                        elif choice == 4:
                            print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                            result = divide(x, y)
                            if result is not None:
                                print(f"{Fore.BLUE}Result: {result}{Style.RESET_ALL}\n")
                                save_calculation(f"{x} / {y}", result)
                        elif choice == 5:
                            print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                            result = remainder(x, y)
                            print(f"{Fore.BLUE}Result: {remainder(x, y)}{Style.RESET_ALL}\n")
                            save_calculation(f"{x} % {y}", result)
                    else:
                        x = float(input(f"{Fore.CYAN}Enter the number:{Style.RESET_ALL} "))

                        if choice == 6:
                            y = float(input(f"{Fore.CYAN}Enter the exponent:{Style.RESET_ALL} "))
                            print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                            result = power(x, y)
                            print(f"{Fore.BLUE}Result: {power(x, y)}{Style.RESET_ALL}\n")
                            save_calculation(f"{x} ^ {y}", result)
                        elif choice == 7:
                            print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                            result = square_root(x)
                            print(f"{Fore.BLUE}Result: {square_root(x)}{Style.RESET_ALL}\n")
                            save_calculation(f"√{x}", result)
                        elif choice == 8:
                            base = float(input(f"{Fore.CYAN}Enter the base:{Style.RESET_ALL} "))
                            print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                            result = logarithm(x, base)
                            print(f"{Fore.BLUE}Result: {logarithm(x, base)}{Style.RESET_ALL}\n")
                            save_calculation(f"log{base}({x})", result)
                        elif choice == 9:
                            print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                            result = sin(x)
                            print(f"{Fore.BLUE}Result: {sin(x)}{Style.RESET_ALL}\n")
                            save_calculation(f"sin({x})", result)
                        elif choice == 10:
                            print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                            result = cos(x)
                            print(f"{Fore.BLUE}Result: {cos(x)}{Style.RESET_ALL}\n")
                            save_calculation(f"cos({x})", result)
                        elif choice == 11:
                            print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                            result = tan(x)
                            print(f"{Fore.BLUE}Result: {tan(x)}{Style.RESET_ALL}\n")
                            save_calculation(f"tan({x})", result)
                elif choice == 12:
                    iterations = int(input(f"{Fore.CYAN}Enter the number of iterations to approximate π:{Style.RESET_ALL} "))
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    result = calculate_pi(iterations)
                    print(f"{Fore.BLUE}Approximation of π:{Style.RESET_ALL} {Fore.YELLOW}{result}{Style.RESET_ALL}\n")
                    save_calculation("π", result)
                elif choice == 13:
                    iterations2 = int(input(f"{Fore.CYAN}Enter the number of iterations to approximate e:{Style.RESET_ALL} "))
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    result = calculate_e(iterations2)
                    print(f"{Fore.BLUE}Approximation of e:{Style.RESET_ALL} {Fore.YELLOW}{result}{Style.RESET_ALL}\n")
                    save_calculation("e", result)
                elif choice == 14:
                    number = float(input(f"{Fore.CYAN}Enter a number:{Style.RESET_ALL} "))
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    result, exponent = avogadro(number)
                    print(f"{Fore.BLUE}The number {number} can be represented as {result:.3f} * 10^{exponent}{Style.RESET_ALL}\n")
                    save_calculation3(f"{number}", result, exponent)
                elif choice == 15:
                    decimal_number = int(input(f"{Fore.CYAN}Enter a decimal number:{Style.RESET_ALL} "))
                    binary_number = decimal_to_binary(decimal_number)
                    print(f"{Fore.MAGENTA}------------------------------------{Style.RESET_ALL}")
                    print(f"{Fore.BLUE}Binary representation:", binary_number, "\n")
                    save_calculation(decimal_number, binary_number)
                elif choice == 16:
                    binary_number = input(f"{Fore.CYAN}Enter a binary number:{Style.RESET_ALL} ")
                    decimal_number = binary_to_decimal(binary_number)
                    print(f"{Fore.MAGENTA}------------------------------------{Style.RESET_ALL}")
                    print(f"{Fore.BLUE}Decimal representation:", decimal_number, "\n")
                    save_calculation(binary_number, decimal_number)
                elif choice == 17:
                    binary_number = input(f"{Fore.CYAN}Enter a binary number:{Style.RESET_ALL} ")
                    hexadecimal_number = binary_to_hexadecimal(binary_number)
                    print(f"{Fore.MAGENTA}------------------------------------{Style.RESET_ALL}")
                    print(f"{Fore.BLUE}Hexadecimal representation:", hexadecimal_number, "\n")
                    save_calculation(binary_number, hexadecimal_number)
                elif choice == 18:
                    hexadecimal_number = input(f"{Fore.CYAN}Enter a hexadecimal number:{Style.RESET_ALL} ")
                    binary_number = hexadecimal_to_binary(hexadecimal_number)
                    print(f"{Fore.MAGENTA}------------------------------------{Style.RESET_ALL}")
                    print(f"{Fore.BLUE}Binary representation:", binary_number, "\n")
                    save_calculation(hexadecimal_number, binary_number)
                elif choice == 19:
                    binary_number = input(f"{Fore.CYAN}Enter a binary number:{Style.RESET_ALL} ")
                    octal_number = binary_to_octal(binary_number)
                    print(f"{Fore.MAGENTA}------------------------------------{Style.RESET_ALL}")
                    print(f"{Fore.BLUE}Octal representation:", octal_number, "\n")
                    save_calculation(binary_number, octal_number)
                elif choice == 20:
                    octal_number = input(f"{Fore.CYAN}Enter an octal number:{Style.RESET_ALL} ")
                    print(f"{Fore.MAGENTA}------------------------------------{Style.RESET_ALL}")
                    binary_number = octal_to_binary(octal_number)
                    if binary_number is not None:
                        print(f"{Fore.BLUE}Binary representation:", binary_number, "\n")
                        save_calculation(octal_number, binary_number)
                elif choice == 21:
                    decimal_number = int(input(f"{Fore.CYAN}Enter a decimal number:{Style.RESET_ALL} "))
                    hexadecimal_number = decimal_to_hexadecimal(decimal_number)
                    print(f"{Fore.MAGENTA}------------------------------------{Style.RESET_ALL}")
                    print(f"{Fore.BLUE}Hexadecimal representation:", hexadecimal_number, "\n")
                    save_calculation(decimal_number, hexadecimal_number)
                elif choice == 22:
                    hexadecimal_number = input(f"{Fore.CYAN}Enter a hexadecimal number:{Style.RESET_ALL} ")
                    decimal_number = hexadecimal_to_decimal(hexadecimal_number)
                    print(f"{Fore.MAGENTA}------------------------------------{Style.RESET_ALL}")
                    print(f"{Fore.BLUE}Decimal representation:", decimal_number, "\n")
                    save_calculation(hexadecimal_number, decimal_number)
                elif choice == 23:
                    decimal_number = int(input(f"{Fore.CYAN}Enter a decimal number:{Style.RESET_ALL} "))
                    octal_number = decimal_to_octal(decimal_number)
                    print(f"{Fore.MAGENTA}------------------------------------{Style.RESET_ALL}")
                    print(f"{Fore.BLUE}Octal representation:", octal_number, "\n")
                    save_calculation(decimal_number, octal_number)
                elif choice == 24:
                    octal_number = input(f"{Fore.CYAN}Enter an octal number:{Style.RESET_ALL} ")
                    print(f"{Fore.MAGENTA}------------------------------------{Style.RESET_ALL}")
                    decimal_number = octal_to_decimal(octal_number)
                    if decimal_number is not None:
                        print(f"{Fore.BLUE}Decimal representation:", decimal_number, "\n")
                        save_calculation(octal_number, decimal_number)
                elif choice == 25:
                    text = input(f"{Fore.CYAN}Enter the text to convert to binary:{Style.RESET_ALL} ")
                    print(f"{Fore.MAGENTA}------------------------------------{Style.RESET_ALL}")
                    binary = text_to_binary(text)
                    print(f"{Fore.BLUE}Binary format of {text}:", binary, "\n")
                    save_calculation(f"{text}", binary)
                elif choice == 26:
                    binary = input(f"{Fore.CYAN}Enter the binary to convert to text:{Style.RESET_ALL} ")
                    print(f"{Fore.MAGENTA}------------------------------------{Style.RESET_ALL}")
                    text_decoded = binary_to_text(binary)
                    print(f"{Fore.BLUE}Text format of {binary}:", text_decoded, "\n")
                    save_calculation(f"{binary}", text_decoded)
                elif choice == 27:
                    octal_number = input(f"{Fore.CYAN}Enter an octal number:{Style.RESET_ALL} ")
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    hexadecimal_number = octal_to_hexadecimal(octal_number)
                    if hexadecimal_number is not None:
                        print(f"{Fore.BLUE}Hexadecimal representation: ", hexadecimal_number, "\n")
                        save_calculation(f"{octal_number}", hexadecimal_number)
                elif choice == 28:
                    hexadecimal_number = input(f"{Fore.CYAN}Enter a hexadecimal number:{Style.RESET_ALL} ")
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    octal_number = hexadecimal_to_octal(hexadecimal_number)
                    print(f"{Fore.BLUE}Octal representation: ", octal_number, "\n")
                    save_calculation(f"{hexadecimal_number}", octal_number)
                elif choice == 29:
                    meters = float(input(f"{Fore.CYAN}Enter the distance in meters:{Style.RESET_ALL} "))
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    kilometers = meters_to_kilometers(meters)
                    print(f"{Fore.BLUE}{meters} meters is equal to {kilometers} kilometers.{Style.RESET_ALL}\n")
                    save_calculation2(f"{meters} meters", kilometers, "kilometers")
                elif choice == 30:
                    kilometers = float(input(f"{Fore.CYAN}Enter the distance in kilometers:{Style.RESET_ALL} "))
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    meters = kilometers_to_meters(kilometers)
                    print(f"{Fore.BLUE}{kilometers} kilometers is equal to {meters} meters.{Style.RESET_ALL}\n")
                    save_calculation2(f"{kilometers} kilometers", meters, "meters")
                elif choice == 31:
                    distance_kilometers = float(input(f"{Fore.CYAN}Enter distance in kilometers:{Style.RESET_ALL} "))
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    light_years = calculate_light_years(distance_kilometers)
                    print(f"{Fore.BLUE}Distance in light-years: {light_years:.16f}{Style.RESET_ALL}\n")
                    save_calculation2(f"{distance_kilometers} kilometers", light_years, "light-years")
                elif choice == 32:
                    light_years = float(input(f"{Fore.CYAN}Enter distance in light-years:{Style.RESET_ALL} "))
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    distance_km = convert_light_years(light_years) / 1000
                    distance_exact = "{:.3e}".format(distance_km)
                    distance_exact = distance_exact.replace("e+12", "e+15")
                    print(f"{Fore.BLUE}Distance in kilometers: {distance_exact}{Style.RESET_ALL}\n")
                    save_calculation2(f"{light_years} light-years", distance_exact, "kilometers")
                elif choice == 33:
                    miles = float(input(f"{Fore.CYAN}Enter the distance in miles:{Style.RESET_ALL} "))
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    kilometers = miles_to_km(miles)
                    print(f"{Fore.BLUE}{miles} miles is equal to {kilometers} kilometers.{Style.RESET_ALL}\n")
                    save_calculation2(f"{miles} miles", kilometers, "kilometers")
                elif choice == 34:
                    kilometers = float(input(f"{Fore.CYAN}Enter the distance in kilometers:{Style.RESET_ALL} "))
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    miles = km_to_miles(kilometers)
                    print(f"{Fore.BLUE}{kilometers} kilometers is equal to {miles} miles.{Style.RESET_ALL}\n")
                    save_calculation2(f"{kilometers} kilometers", miles, "miles")
                elif choice == 35:
                    meters = float(input(f"{Fore.CYAN}Enter the distance in meters:{Style.RESET_ALL} "))
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    miles = meters_to_miles(meters)
                    print(f"{Fore.BLUE}{meters} meters is equal to {miles} miles.{Style.RESET_ALL}\n")
                    save_calculation2(f"{meters} meters", miles, "miles")
                elif choice == 36:
                    miles = float(input(f"{Fore.CYAN}Enter the distance in miles:{Style.RESET_ALL} "))
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    meters = miles_to_meters(miles)
                    print(f"{Fore.BLUE}{miles} miles is equal to {meters} meters.{Style.RESET_ALL}\n")
                    save_calculation2(f"{miles} miles", meters, "meters")
                elif choice == 37:
                    meters = float(input(f"{Fore.CYAN}Enter the distance in meters:{Style.RESET_ALL} "))
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    feet = meters_to_feet(meters)
                    print(f"{Fore.BLUE}{meters} meters is equal to {feet} feet.{Style.RESET_ALL}\n")
                    save_calculation2(f"{meters} meters", feet, "feet")
                elif choice == 38:
                    feet = float(input(f"{Fore.CYAN}Enter the distance in feet:{Style.RESET_ALL} "))
                    meters = feet_to_meters(feet)
                    print(f"{Fore.BLUE}{feet} feet is equal to {meters} meters.{Style.RESET_ALL}\n")
                    save_calculation2(f"{feet} feet", meters, "meters")
                elif choice == 39:
                    weight = float(input(f"{Fore.CYAN}Enter weight in kilograms:{Style.RESET_ALL} "))
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    result = kg_to_lb(weight)
                    print(f"{Fore.BLUE}Weight in pounds: {result}{Style.RESET_ALL}\n")
                    save_calculation2(f"{weight} kilograms", result, "pounds")
                elif choice == 40:
                    weight = float(input(f"{Fore.CYAN}Enter weight in pounds:{Style.RESET_ALL} "))
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    result = lb_to_kg(weight)
                    print(f"{Fore.BLUE}Weight in kilograms: {result}{Style.RESET_ALL}\n")
                    save_calculation2(f"{weight} pounds", result, "kilograms")
                elif choice == 41:
                    weight = float(input(f"{Fore.CYAN}Enter weight in kilograms:{Style.RESET_ALL} "))
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    result = kg_to_g(weight)
                    print(f"{Fore.BLUE}Weight in grams: {result}{Style.RESET_ALL}\n")
                    save_calculation2(f"{weight} kilograms", result, "grams")
                elif choice == 42:
                    weight = float(input(f"{Fore.CYAN}Enter weight in grams:{Style.RESET_ALL} "))
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    result = g_to_kg(weight)
                    print(f"{Fore.BLUE}Weight in kilograms: {result}{Style.RESET_ALL}\n")
                    save_calculation2(f"{weight} grams", result, "kilograms")
                elif choice == 43:
                    weight = float(input(f"{Fore.CYAN}Enter weight in kilograms:{Style.RESET_ALL} "))
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    result = kg_to_ton(weight)
                    print(f"{Fore.BLUE}Weight in ton: {result}{Style.RESET_ALL}\n")
                    save_calculation2(f"{weight} kilograms", result, "tons")
                elif choice == 44:
                    weight = float(input(f"{Fore.CYAN}Enter weight in tons:{Style.RESET_ALL} "))
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    result = ton_to_kg(weight)
                    print(f"{Fore.BLUE}Weight in kilograms: {result}{Style.RESET_ALL}\n")
                    save_calculation2(f"{weight} tons", result, "kilograms")
                elif choice == 45:
                    weight = float(input(f"{Fore.CYAN}Enter weight in pounds:{Style.RESET_ALL} "))
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    result = lb_to_g(weight)
                    print(f"{Fore.BLUE}Weight in grams: {result}{Style.RESET_ALL}\n")
                    save_calculation2(f"{weight} pounds", result, "grams")
                elif choice == 46:
                    weight = float(input(f"{Fore.CYAN}Enter weight in grams:{Style.RESET_ALL} "))
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    result = g_to_lb(weight)
                    print(f"{Fore.BLUE}Weight in pounds: {result}{Style.RESET_ALL}\n")
                    save_calculation2(f"{weight} grams", result, "pounds")
                elif choice == 47:
                    weight = float(input(f"{Fore.CYAN}Enter weight in pounds:{Style.RESET_ALL} "))
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    result = lb_to_ton(weight)
                    print(f"{Fore.BLUE}Weight in tons: {result}{Style.RESET_ALL}\n")
                    save_calculation2(f"{weight} pounds", result, "tons")
                elif choice == 48:
                    weight = float(input(f"{Fore.CYAN}Enter weight in tons:{Style.RESET_ALL} "))
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    result = ton_to_lb(weight)
                    print(f"{Fore.BLUE}Weight in pounds: {result}{Style.RESET_ALL}\n")
                    save_calculation2(f"{weight} tons", result, "pounds")
                elif choice == 49:
                    weight = float(input(f"{Fore.CYAN}Enter weight in grams:{Style.RESET_ALL} "))
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    result = g_to_ton(weight)
                    print(f"{Fore.BLUE}Weight in tons: {result}{Style.RESET_ALL}\n")
                    save_calculation2(f"{weight} grams", result, "tons")
                elif choice == 50:
                    weight = float(input(f"{Fore.CYAN}Enter weight in tons:{Style.RESET_ALL} "))
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    result = ton_to_g(weight)
                    print(f"{Fore.BLUE}Weight in grams: {result}{Style.RESET_ALL}\n")
                    save_calculation2(f"{weight} tons", result, "grams")
                elif choice == 51:
                    weight = float(input(f"{Fore.CYAN}Enter weight in stone:{Style.RESET_ALL} "))
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    result = stone_to_kg(weight)
                    print(f"{Fore.BLUE}Weight in kilograms: {result}{Style.RESET_ALL}\n")
                    save_calculation2(f"{weight} stone", result, "kilograms")
                elif choice == 52:
                    weight = float(input(f"{Fore.CYAN}Enter weight in kilograms:{Style.RESET_ALL} "))
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    result = kg_to_stone(weight)
                    print(f"{Fore.BLUE}Weight in stone: {result}{Style.RESET_ALL}\n")
                    save_calculation2(f"{weight} kilograms", result, "stone")
                elif choice == 53:
                    data_str = input(f"{Fore.CYAN}Enter the dataset (comma-separated values):{Style.RESET_ALL} ")
                    if ',' not in data_str or ' ' not in data_str:
                        print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                        print(f"{Fore.RED}Error: Incorrect dataset format. Please separate values with commas and spaces.{Style.RESET_ALL} ")
                    else:
                        dataset = [float(x) for x in data_str.split(",")]
                        print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                        print(f"{Fore.BLUE}Mean:", calculate_mean(dataset), "\n")
                        save_calculation(f"Mean:", calculate_mean(dataset))
                elif choice == 54:
                    data_str = input(f"{Fore.CYAN}Enter the dataset (comma-separated values):{Style.RESET_ALL} ")
                    if ',' not in data_str or ' ' not in data_str:
                        print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                        print(f"{Fore.RED}Error: Incorrect dataset format. Please separate values with commas and spaces.{Style.RESET_ALL} ")
                    else:
                        dataset = [float(x) for x in data_str.split(",")]
                        print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                        print(f"{Fore.BLUE}Median:", calculate_median(dataset), "\n")
                        save_calculation(f"Median:", calculate_median(dataset))
                elif choice == 55:
                    data_str = input(f"{Fore.CYAN}Enter the dataset (comma-separated values):{Style.RESET_ALL} ")
                    if ',' not in data_str or ' ' not in data_str:
                        print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                        print(f"{Fore.RED}Error: Incorrect dataset format. Please separate values with commas and spaces.{Style.RESET_ALL} ")
                    else:
                        dataset = [float(x) for x in data_str.split(",")]
                        print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                        print(f"{Fore.BLUE}Mode:", calculate_mode(dataset), "\n")
                        save_calculation(f"Mode:", calculate_mode(dataset))
                elif choice == 56:
                    data_str = input(f"{Fore.CYAN}Enter the dataset (comma-separated values):{Style.RESET_ALL} ")
                    if ',' not in data_str or ' ' not in data_str:
                        print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                        print(f"{Fore.RED}Error: Incorrect dataset format. Please separate values with commas and spaces.{Style.RESET_ALL} ")
                    else:
                        dataset = [float(x) for x in data_str.split(",")]
                        print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                        print(f"{Fore.BLUE}Standard Deviation:", calculate_standard_deviation(dataset), "\n")
                        save_calculation(f"Standard Deviation:", calculate_standard_deviation(dataset))
                elif choice == 57:
                    data_str = input(f"{Fore.CYAN}Enter the dataset (comma-separated values):{Style.RESET_ALL} ")
                    if ',' not in data_str or ' ' not in data_str:
                        print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                        print(f"{Fore.RED}Error: Incorrect dataset format. Please separate values with commas and spaces.{Style.RESET_ALL} ")
                    else:
                        dataset = [float(x) for x in data_str.split(",")]
                        print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                        print(f"{Fore.BLUE}Variance:", calculate_variance(dataset), "\n")
                        save_calculation(f"Variance:", calculate_variance(dataset))
                elif choice == 58:
                    data_str = input(f"{Fore.CYAN}Enter the dataset (comma-separated values):{Style.RESET_ALL} ")
                    if ',' not in data_str or ' ' not in data_str:
                        print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                        print(f"{Fore.RED}Error: Incorrect dataset format. Please separate values with commas and spaces.{Style.RESET_ALL} ")
                    else:
                        dataset = [float(x) for x in data_str.split(",")]
                        print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                        print(f"{Fore.BLUE}Range:", calculate_range(dataset), "\n")
                        save_calculation(f"Range:", calculate_range(dataset))
                elif choice == 59:
                    data_str = input(f"{Fore.CYAN}Enter the dataset (comma-separated values):{Style.RESET_ALL} ")
                    if ',' not in data_str or ' ' not in data_str:
                        print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                        print(f"{Fore.RED}Error: Incorrect dataset format. Please separate values with commas and spaces.{Style.RESET_ALL} ")
                    else:
                        dataset = [float(x) for x in data_str.split(",")]
                        print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                        print(f"{Fore.BLUE}Quartiles:", calculate_quartiles(dataset), "\n")
                        save_calculation(f"Quartiles:", calculate_quartiles(dataset))
                elif choice == 60:
                    data_str = input(f"{Fore.CYAN}Enter the dataset (comma-separated values):{Style.RESET_ALL} ")
                    if ',' not in data_str or ' ' not in data_str:
                        print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                        print(f"{Fore.RED}Error: Incorrect dataset format. Please separate values with commas and spaces.{Style.RESET_ALL} ")
                    else:
                        dataset = [float(x) for x in data_str.split(",")]
                        print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                        print(f"{Fore.BLUE}Interquartile Range:", calculate_interquartile_range(dataset), "\n")
                        save_calculation(f"Interquartile Range:", calculate_interquartile_range(dataset))
                elif choice == 61:
                    data_str = input(f"{Fore.CYAN}Enter the dataset (comma-separated values):{Style.RESET_ALL} ")
                    if ',' not in data_str or ' ' not in data_str:
                        print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                        print(f"{Fore.RED}Error: Incorrect dataset format. Please separate values with commas and spaces.{Style.RESET_ALL} ")
                    else:
                        dataset = [float(x) for x in data_str.split(",")]
                        print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                        print(f"{Fore.BLUE}Skewness:", calculate_skewness(dataset), "\n")
                        save_calculation(f"Skewness:", calculate_skewness(dataset))
                elif choice == 62:
                    data_str = input(f"{Fore.CYAN}Enter the dataset (comma-separated values):{Style.RESET_ALL} ")
                    if ',' not in data_str or ' ' not in data_str:
                        print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                        print(f"{Fore.RED}Error: Incorrect dataset format. Please separate values with commas and spaces.{Style.RESET_ALL} ")
                    else:
                        dataset = [float(x) for x in data_str.split(",")]
                        print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                        kurtosis_value = calculate_kurtosis(dataset)
                        kurtosis_type = determine_kurtosis_type(kurtosis_value)
                        print(f"{Fore.BLUE}Kurtosis: {kurtosis_value} ({kurtosis_type})\n")
                        save_calculation2(f"Kurtosis:", kurtosis_value, kurtosis_type)
                elif choice == 63:
                    data_str = input(f"{Fore.CYAN}Enter the dataset (comma-separated values):{Style.RESET_ALL} ")
                    if ',' not in data_str or ' ' not in data_str:
                        print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                        print(f"{Fore.RED}Error: Incorrect dataset format. Please separate values with commas and spaces.{Style.RESET_ALL} ")
                    else:
                        dataset = [float(x) for x in data_str.split(",")]
                        hypothesized_mean = float(input(f"{Fore.CYAN}Enter the hypothesized mean:{Style.RESET_ALL} "))
                        population_std_dev = float(input(f"{Fore.CYAN}Enter the population standard deviation:{Style.RESET_ALL} "))
                        print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                        print(f"{Fore.BLUE}Z-test:", calculate_z_test(dataset, hypothesized_mean, population_std_dev), "\n")
                        save_calculation(f"Z-test:", calculate_z_test(dataset, hypothesized_mean, population_std_dev))
                elif choice == 64:
                    amount = float(input(f"{Fore.CYAN}Enter the amount to be converted:{Style.RESET_ALL} "))
                    from_currency = input(f"{Fore.CYAN}Enter the currency to convert from:{Style.RESET_ALL} ").upper()
                    to_currency = input(f"{Fore.CYAN}Enter the currency to convert to:{Style.RESET_ALL} ").upper()
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    if not has_internet_connection():
                        print(f"{Fore.RED}No internet connection!{Style.RESET_ALL}")
                    else:
                        converted_amount = convert_currency(amount, from_currency, to_currency)
                        if converted_amount is None:
                            print(f"{Fore.RED}One of the currencies is invalid or doesn't exist!{Style.RESET_ALL}")
                            print(f"{Fore.RED}Please enter a valid currency!{Style.RESET_ALL}\n")
                        else:
                            print(f"{Fore.BLUE}{amount} {from_currency} = {converted_amount} {to_currency}{Style.RESET_ALL}\n")
                            save_calculation2(f"{amount} {from_currency}", converted_amount, to_currency)
                elif choice == 65:
                    amount = float(input(f"{Fore.CYAN}Enter the amount of cryptocurrency:{Style.RESET_ALL} "))
                    from_currency_acronym = input(f"{Fore.CYAN}Enter the cryptocurrency:{Style.RESET_ALL} ").upper()
                    to_currency = input(f"{Fore.CYAN}Enter the currency to convert to:{Style.RESET_ALL} ").upper()
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    if not has_internet_connection():
                        print(f"{Fore.RED}No internet connection!{Style.RESET_ALL}")
                    else:
                        conversion_data = convert_to_currency(amount, from_currency_acronym, to_currency)
                        if conversion_data is not None:
                            converted_amount = conversion_data
                            print(f"{Fore.BLUE}{amount} {from_currency_acronym} = {converted_amount} {to_currency}{Style.RESET_ALL}\n")
                            save_calculation2(f"{amount} {from_currency_acronym}", converted_amount, to_currency)
                        else:
                            error_message = ""
                            error_message2 = ""
                            if conversion_data is None:
                                error_message += f"{Fore.RED}Invalid cryptocurrency or currency!{Style.RESET_ALL}"
                                error_message2 += f"{Fore.RED}Please enter a valid one.{Style.RESET_ALL}\n"
                            print(error_message)
                            print(error_message2)
                elif choice == 66:
                    expression = input(f"{Fore.CYAN}Enter the binary expression:{Style.RESET_ALL} ")
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    output = binary_calculator(expression)
                    if output != "":
                        print(Fore.BLUE + output + Style.RESET_ALL)
                        save_calculation4(output)
                elif choice == 67:
                    expression = input(f"{Fore.CYAN}Enter the expression:{Style.RESET_ALL} ")
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    result = evaluate_expression(expression)
                    if result is not None:
                        print(f"{Fore.BLUE}Result: {result}{Style.RESET_ALL}\n")
                        save_calculation(expression, result)
                elif choice == 68:
                    view_calculations()
                else:
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    exit_message = "Invalid choice!! Please enter a valid option!!"
                    print(f"\n{Fore.RED}", end='', flush=True)
                    print_with_delay(exit_message, 40)  # Adjust the delay per letter (in milliseconds) as desired
                    print(Style.RESET_ALL, "\n")
            else:
                exit_message = "Exiting the calculator..."
                print(f"\n{Fore.RED}", end='', flush=True)
                print_with_delay(exit_message, 40)  # Adjust the delay per letter (in milliseconds) as desired
                print(Style.RESET_ALL, "\n")
    except ValueError as e:
        print(e)
    except Exception as e:
        print("An error occurred:", e)

    except KeyboardInterrupt:
        exit_message = "Exiting the calculator..."
        print(f"\n{Fore.MAGENTA}", end='', flush=True)
        print_with_delay(exit_message, 40)  # Adjust the delay per letter (in milliseconds) as desired
        print(Style.RESET_ALL, "\n")
        time.sleep(5)

scientific_calculator()
