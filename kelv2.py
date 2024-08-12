import os
import json
import sys
import requests
import string
import random
import time
import subprocess
import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
from colorama import Fore, init
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

# Konsol renklerini etkinleştir
init(autoreset=True)

# URL yapısının sabit kısmı
base_url = "https://justpaste.it/"

# Geçerli linkleri kaydetmek için dosya
valid_file = "valid.txt"

# Discord Webhook URL'si
discord_webhook_url = "https://discord.com/api/webhooks/1128841469290090496/akVrFH36MOZiSRVEsyRKlqCRm01ltOjupzzujZJ8fof8MPRxoQJgG7IHOsB2vBcO8xI7"

# Yapılandırma dosyası
config_file = "config.json"

def save_config(chromedriver_path, proxy_file):
    config_data = {
        "chromedriver_path": chromedriver_path,
        "proxy_file": proxy_file
    }
    with open(config_file, 'w') as f:
        json.dump(config_data, f)

def load_config():
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    return None

def close_existing_chrome_sessions():
    try:
        # Tüm Chrome tarayıcılarını kapatmak için taskkill komutunu kullan
        subprocess.call(["taskkill", "/F", "/IM", "chrome.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    except Exception as e:
        print(Fore.RED + f"Chrome tarayıcılarını kapatırken hata oluştu: {e}")

def restart_program():
    print(Fore.YELLOW + "Program yeniden başlatılıyor...")

    # Chrome tarayıcılarını kapat
    close_existing_chrome_sessions()

    python = sys.executable
    os.execv(python, [python] + sys.argv)
    os._exit(0)  # Mevcut program sürecini sonlandır

def generate_random_suffix(length=5):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def check_url(link, proxies=None):
    try:
        response = requests.get(link, timeout=5, proxies=proxies)
        if 200 <= response.status_code < 400:
            return True
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Hata: {e}")
        restart_program()  # Hata durumunda programı yeniden başlat
    return False

def load_proxies(file_path):
    with open(file_path, 'r') as file:
        proxies = file.read().splitlines()
    return proxies

def select_file():
    root = tk.Tk()
    root.withdraw()  # Ana pencereyi gizle
    file_path = filedialog.askopenfilename(title="Proxy Listesi Seçin", filetypes=[("Text Files", "*.txt")])
    return file_path

def get_valid_url():
    root = tk.Tk()
    root.withdraw()  # Ana pencereyi gizle
    
    while True:
        url = simpledialog.askstring("Geçerli URL Girin", "Bir geçerli URL girin:")
        if url and check_url(url):
            return url
        print(Fore.RED + "Girdiğiniz URL geçerli değil veya erişilemez. Lütfen tekrar deneyin.")
        restart_program()  # Hata durumunda programı yeniden başlat

def open_chrome_with_chromedriver_path():
    root = tk.Tk()
    root.withdraw()
    chromedriver_path = filedialog.askopenfilename(
        title="Chromedriver Seçin",
        filetypes=[("Executables", "*.exe"), ("All Files", "*.*")]
    )
    
    if not chromedriver_path:
        print(Fore.RED + "Chromedriver dosyası seçilmedi. Program sonlandırılıyor.")
        restart_program()  # Hata durumunda programı yeniden başlat
        return None

    return chromedriver_path

def take_screenshot(url, chromedriver_path, file_path="screenshot.png"):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Tarayıcıyı tam ekran aç
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        driver.save_screenshot(file_path)
    except WebDriverException as e:
        print(Fore.RED + f"WebDriver hatası: {e}")
        close_existing_chrome_sessions()  # Chrome tarayıcılarını kapat
        restart_program()  # Programı yeniden başlat
    finally:
        driver.quit()

def send_to_discord(url, proxy, file_path):
    with open(file_path, 'rb') as file:
        files = {'file': ('screenshot.png', file)}
        data = {
            "content": f"Geçerli URL: {url} (proxy: {proxy})"
        }
        response = requests.post(discord_webhook_url, data=data, files=files)
        if response.status_code == 204 or response.status_code == 200:
            print(Fore.GREEN + "Discord'a başarıyla gönderildi.")
        else:
            print(Fore.RED + "Discord gönderimi başarısız oldu.")
            restart_program()  # Hata durumunda programı yeniden başlat

def main():
    config = load_config()
    if config:
        chromedriver_path = config["chromedriver_path"]
        proxy_file = config["proxy_file"]
        print(Fore.YELLOW + "Önceki ayarlar yüklendi.")
    else:
        chromedriver_path = open_chrome_with_chromedriver_path()
        if not chromedriver_path:
            return

        proxy_file = select_file()
        if not proxy_file:
            print(Fore.RED + "Proxy dosyası seçilmedi. Program sonlandırılıyor.")
            return
        
        save_config(chromedriver_path, proxy_file)

    proxies_list = load_proxies(proxy_file)
    if not proxies_list:
        print(Fore.RED + "Proxy listesi boş. Program sonlandırılıyor.")
        return

    print(Fore.YELLOW + "Proxy listesi yüklendi. URL denemeleri başlayacak...")

    # Sonsuz döngü
    with open(valid_file, "a") as file:  # 'a' ile dosyayı açarak sürekli ekleme yaparız
        while True:
            for proxy in proxies_list:
                proxy_dict = {"http": proxy, "https": proxy}
                # Rastgele bir URL uzantısı oluştur
                suffix = generate_random_suffix()
                link = base_url + suffix
                
                # URL'yi kontrol et
                if check_url(link, proxies=proxy_dict):
                    try:
                        file.write(f"{link} (proxy: {proxy})\n")
                        file.flush()  # Dosyaya hemen yazmak için flush() kullanılır
                        print(Fore.GREEN + "+" + f" {link} (proxy: {proxy}) (kaydedildi)")

                        # Ekran görüntüsü al
                        take_screenshot(link, chromedriver_path)

                        # Discord'a gönder
                        send_to_discord(link, proxy, "screenshot.png")

                    except Exception as e:
                        print(Fore.RED + "-" + f" {link} (proxy: {proxy}) (kaydedilemedi: {e})")
                        restart_program()  # Hata durumunda programı yeniden başlat
                else:
                    print(Fore.RED + "-" + f" {link} (proxy: {proxy})")
                
                time.sleep(1)

if __name__ == "__main__":
    main()
