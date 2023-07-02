import os
import math
from colorama import Fore, Style
import re
import time
import getpass
from datetime import datetime
import requests
from requests.exceptions import RequestException

def clear_terminal():
    if os.name == "posix":  # Unix/Linux/MacOS
        os.system("clear")
    elif os.name == "nt":  # Windows
        os.system("cls")

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
print(tool)

password = getpass.getpass(f"{Fore.CYAN}Enter password:{Style.RESET_ALL} ")

if password == "Shredder":
    print(f"{Fore.CYAN}[*] Access granted. Proceeding with the program...\n{Style.RESET_ALL}")
    time.sleep(10)
else:
    print(f"{Fore.MAGENTA}[*] Access Denied!!\n{Style.RESET_ALL}")
    exit(1)

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

def get_exchange_rate(from_currency, to_currency):
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
    url = f"https://min-api.cryptocompare.com/data/price?fsym={from_currency}&tsyms={to_currency}"
    response = requests.get(url)
    data = response.json()
    if to_currency in data:
        conversion_rate = data[to_currency]
        converted_amount = amount * conversion_rate
        return converted_amount
    else:
        return None

def binary_calculator(expression):
    # Separate the binary numbers and operators
    parts = re.findall(r'[01]+|[-+*/]', expression)
    binaries = [part for part in parts if all(bit in '01' for bit in part)]
    operators = [part for part in parts if part not in binaries]

    # Convert the binary numbers to decimal and perform calculations
    decimals = [int(binary, 2) for binary in binaries]
    result_decimal = decimals[0]

    for i in range(1, len(decimals)):
        operator = operators[i - 1]
        if operator == '+':
            result_decimal += decimals[i]
        elif operator == '-':
            result_decimal -= decimals[i]
        elif operator == '*':
            result_decimal *= decimals[i]
        elif operator == '/':
            result_decimal //= decimals[i]

    output = "Binary value:\n"
    output += f"{expression} = {bin(result_decimal)[2:].zfill(max(len(binary) for binary in binaries))}\n"
    output += "Decimal value:\n"
    output += ' + '.join(map(str, decimals)) + f" = {result_decimal}\n"

    return output

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
        print(f"{Fore.MAGENTA}No calculations found.{Style.RESET_ALL}")

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

Currency
53. Currency Converter
54. Crytocurrency Converter

Other Options
55. Binary Calculator
56. Evaluate Mixed Operation
57. View Previous Calculations

Type 'Exit' to quit the program.
    """
    try:
        while True:
            choice = input(f"{Fore.CYAN}\nEnter your choice:{Style.RESET_ALL} ")

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
                    amount = float(input(f"{Fore.CYAN}Enter the amount to be converted:{Style.RESET_ALL} "))
                    from_currency = input(f"{Fore.CYAN}Enter the currency to convert from:{Style.RESET_ALL} ").upper()
                    to_currency = input(f"{Fore.CYAN}Enter the currency to convert to:{Style.RESET_ALL} ").upper()
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    converted_amount = convert_currency(amount, from_currency, to_currency)
                    if converted_amount is None:
                        print(f"{Fore.RED}One of the currencies is invalid or doesn't exist!{Style.RESET_ALL}")
                        print(f"{Fore.RED}Please enter a valid currency!{Style.RESET_ALL}\n")
                    else:
                        print(f"{Fore.BLUE}{amount} {from_currency} = {converted_amount} {to_currency}{Style.RESET_ALL}\n")
                        save_calculation2(f"{amount} {from_currency}", converted_amount, to_currency)
                elif choice == 54:
                    amount = float(input(f"{Fore.CYAN}Enter the amount of cryptocurrency:{Style.RESET_ALL} "))
                    from_currency_acronym = input(f"{Fore.CYAN}Enter the cryptocurrency:{Style.RESET_ALL} ").upper()
                    to_currency = input(f"{Fore.CYAN}Enter the currency to convert to:{Style.RESET_ALL} ").upper()
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
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
                elif choice == 55:
                    expression = input(f"{Fore.CYAN}Enter the binary expression:{Style.RESET_ALL} ")
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    output = binary_calculator(expression)
                    print(Fore.BLUE + output + Style.RESET_ALL)
                    save_calculation4(output)
                elif choice == 56:
                    expression = input(f"{Fore.CYAN}Enter the expression:{Style.RESET_ALL} ")
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    result = evaluate_expression(expression)
                    if result is not None:
                        print(f"{Fore.BLUE}Result: {result}{Style.RESET_ALL}\n")
                        save_calculation(expression, result)
                elif choice == 57:
                    view_calculations()
                else:
                    print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                    print(f"{Fore.MAGENTA}Error: Invalid choice!!! Please enter a valid choice.{Style.RESET_ALL}\n")
            else:
                print(f"{Fore.MAGENTA}----------------------------{Style.RESET_ALL}")
                print(f"{Fore.MAGENTA}Error: Invalid choice! Please enter a valid choice.{Style.RESET_ALL}\n")

    except KeyboardInterrupt:
        print(f"\n{Fore.MAGENTA}Exiting the calculator...{Style.RESET_ALL}")
        time.sleep(5)
        print(f"{Fore.CYAN}You're really suck in math! Well me too!:){Style.RESET_ALL}")

scientific_calculator()
