Bu kod, belirli bir URL yapısına sahip rastgele linkler oluşturarak geçerliliklerini test eder ve proxy'ler kullanarak bu testleri gerçekleştirir. Geçerli olan linkleri bir dosyaya kaydeder. Aşağıda kodun işleyişini ve uygulamanın nasıl kullanılacağını adım adım açıklayan bir rehber bulabilirsiniz:
![image](https://github.com/user-attachments/assets/6e0151f6-7231-4849-8845-0631c55995fe)


Code Overview
The code generates random links with a specific URL structure, tests their validity, and performs these tests using proxies. Valid links are saved to a file. Below is a step-by-step guide explaining the functionality of the code and how to use the application.

Required Libraries:

requests: For making HTTP requests.
string and random: For generating random characters.
time: For adding delays between requests.
tkinter: For a graphical interface to get files and URLs from the user.
colorama: For managing console colors.
Functions:

generate_random_suffix(length=5): Generates a random URL suffix of the specified length.
check_url(link, proxies=None): Checks if a URL is valid. Proxy usage is optional.
load_proxies(file_path): Reads proxies from the specified file and returns them as a list.
select_file(): Opens a file selector to choose a proxy list file.
get_valid_url(): Asks the user to enter a valid URL and checks its validity.
Main Function (main):

Retrieves a valid URL from the user.
Selects a file containing the proxy list and loads the proxies.
In an infinite loop, generates random URLs, checks these URLs using the proxies, and saves valid ones to a file.
Steps to Run the Application

Install Python and Libraries:

Ensure Python 3.x is installed on your computer.
Install the required Python libraries:
bash
Kodu kopyala
pip install requests colorama
Save the Python Code:

Copy and paste the following Python code into a file (e.g., proxy_url_checker.py):

python
Kodu kopyala
import requests
import string
import random
import time
import tkinter as tk
from tkinter import simpledialog, filedialog
from colorama import Fore, init

# Enable console colors
init(autoreset=True)

# Base URL part
base_url = "https://justpaste.it/"

# File to save valid links
valid_file = "valid.txt"

# Discord Webhook URL
webhook_url = "YOUR_DISCORD_WEBHOOK_URL"

def generate_random_suffix(length=5):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def check_url(link, proxies=None):
    try:
        response = requests.get(link, timeout=5, proxies=proxies)
        if 200 <= response.status_code < 400:
            return True
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error: {e}")
    return False

def load_proxies(file_path):
    with open(file_path, 'r') as file:
        proxies = file.read().splitlines()
    return proxies

def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title="Select Proxy List", filetypes=[("Text Files", "*.txt")])
    return file_path

def get_valid_url():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    while True:
        url = simpledialog.askstring("Enter Valid URL", "Please enter a valid URL:")
        if url and check_url(url):
            return url
        print(Fore.RED + "The URL you entered is invalid or inaccessible. Please try again.")

def send_to_discord(message):
    try:
        data = {"content": message}
        requests.post(webhook_url, json=data)
    except Exception as e:
        print(Fore.RED + f"Error sending message to Discord: {e}")

def main():
    valid_url = get_valid_url()
    print(Fore.YELLOW + f"Valid URL obtained: {valid_url}")

    proxy_file = select_file()
    if not proxy_file:
        print(Fore.RED + "No proxy file selected. Exiting the program.")
        return

    proxies_list = load_proxies(proxy_file)
    if not proxies_list:
        print(Fore.RED + "Proxy list is empty. Exiting the program.")
        return

    print(Fore.YELLOW + "Proxy list loaded. URL testing will begin...")

    with open(valid_file, "a") as file:
        while True:
            for proxy in proxies_list:
                proxy_dict = {"http": proxy, "https": proxy}
                suffix = generate_random_suffix()
                link = base_url + suffix

                if check_url(link, proxies=proxy_dict):
                    try:
                        file.write(f"{link} (proxy: {proxy})\n")
                        file.flush()
                        message = f"Valid URL: {link} (proxy: {proxy})"
                        send_to_discord(message)
                        print(Fore.GREEN + "+" + f" {link} (proxy: {proxy}) (saved)")
                    except Exception as e:
                        print(Fore.RED + "-" + f" {link} (proxy: {proxy}) (could not be saved: {e})")
                else:
                    print(Fore.RED + "-" + f" {link} (proxy: {proxy})")

                time.sleep(1)

if __name__ == "__main__":
    main()
Required Tools and Settings:

Python: Requires Python 3.x.
Libraries: The code needs some libraries to be installed:
bash
Kodu kopyala
pip install requests selenium colorama
Chromedriver: Necessary for controlling the Chrome browser with Selenium. Download the appropriate version from here.
Prepare Files and Settings:

Chromedriver File: You’ll need the path to the Chromedriver file on your computer. Download it and place it in a local directory.
Proxy List: Create a text file containing proxy addresses. Each line should have one proxy address, for example:
makefile
Kodu kopyala
104.207.38.25:3128
123.456.78.90:8080
Discord Webhook URL: Create a webhook in your Discord server and get the URL. You need to replace YOUR_DISCORD_WEBHOOK_URL in the code with the actual URL of your webhook. Refer to the Discord Webhook Documentation for more information.
Running the Code:

Run the script file (e.g., script.py) using Python:
bash
Kodu kopyala
python script.py
First Run:

On the first run, the program will ask you to select the Chromedriver file and proxy list. These selections will be saved in a config.json file, so you won’t need to make these selections again in future runs.
Procedures:
Proxy List Selection: Choose the file containing your proxy list.
Chromedriver Selection: Choose the path to the Chromedriver file.
URL Validation: The program will ask you to enter a valid URL and test its accessibility.
Continuous Operation:

The program tests randomly generated URLs with each proxy listed. When valid URLs are found, it saves them along with the proxy information to valid.txt and sends a message to Discord.
Program Restart:

The program automatically restarts itself in case of errors to ensure uninterrupted operation.
Important Notes:

High System Resource Usage: Taking screenshots and testing various URLs can consume system resources (CPU and memory).
Legal Considerations: Proxy usage and web scraping may have legal implications. Make sure to check the terms of use of the target websites.
Summary
This application generates random links with a specific URL structure, tests their validity using proxies, and saves valid links to a file. It also sends notifications to Discord for valid URLs. Ensure you provide the correct proxy list and valid URL for the application to work effectively.

### Özet

Bu uygulama, belirli bir URL yapısına sahip rastgele linkler oluşturur ve geçerliliklerini proxy'ler kullanarak test eder. Proxy listesi dosyası ile çalışır ve geçerli linkleri bir dosyaya kaydeder. Uygulamanın başarılı bir şekilde çalışması için doğru proxy listesi ve geçerli URL'nin girilmesi önemlidir.
