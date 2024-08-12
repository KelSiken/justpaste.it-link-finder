import requests
import string
import random
import time
import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
from colorama import Fore, init
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Konsol renklerini etkinleştir
init(autoreset=True)

# URL yapısının sabit kısmı
base_url = "https://justpaste.it/"

# Geçerli linkleri kaydetmek için dosya
valid_file = "valid.txt"

# Discord Webhook URL'si
discord_webhook_url = "https://discord.com/api/webhooks/1128841469290090496/akVrFH36MOZiSRVEsyRKlqCRm01ltOjupzzujZJ8fof8MPRxoQJgG7IHOsB2vBcO8xI7"

def generate_random_suffix(length=5):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def check_url(link, proxies=None):
    try:
        response = requests.get(link, timeout=5, proxies=proxies)
        if 200 <= response.status_code < 400:
            return True
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Hata: {e}")
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

def open_chrome_with_chromedriver_path():
    root = tk.Tk()
    root.withdraw()
    chromedriver_path = filedialog.askopenfilename(
        title="Chromedriver Seçin",
        filetypes=[("Executables", "*.exe"), ("All Files", "*.*")]
    )
    
    if not chromedriver_path:
        print(Fore.RED + "Chromedriver dosyası seçilmedi. Program sonlandırılıyor.")
        return None

    return chromedriver_path

def take_screenshot(url, chromedriver_path, file_path="screenshot.png"):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Tarayıcıyı tam ekran aç
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    driver.save_screenshot(file_path)
    driver.quit()

def send_to_discord(url, proxy, file_path):
    with open(file_path, 'rb') as file:
        files = {'file': ('screenshot.png', file)}
        data = {
            "content": f"Geçerli URL: {url} (proxy: {proxy})"
        }
        response = requests.post(discord_webhook_url, data=data, files=files)
        if response.status_code == 204:
            print(Fore.GREEN + "Discord'a başarıyla gönderildi.")
        else:
            print(Fore.RED + "Discord gönderimi başarısız oldu.")

def show_error(message):
    root = tk.Tk()
    root.withdraw()  # Ana pencereyi gizle
    messagebox.showerror("Hata", message)

def main():
    # Kullanıcıdan geçerli bir URL al
    valid_url = get_valid_url()
    print(Fore.YELLOW + f"Geçerli URL alındı: {valid_url}")

    # Proxy listesini seçme
    proxy_file = select_file()
    if not proxy_file:
        print(Fore.RED + "Proxy dosyası seçilmedi. Program sonlandırılıyor.")
        return
    
    proxies_list = load_proxies(proxy_file)
    if not proxies_list:
        print(Fore.RED + "Proxy listesi boş. Program sonlandırılıyor.")
        return

    # Kullanıcıdan chromedriver yolunu seçmesini isteyin
    chromedriver_path = open_chrome_with_chromedriver_path()
    if not chromedriver_path:
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
                        show_error(f"URL {link} (proxy: {proxy}) ekran görüntüsü alınırken veya Discord'a gönderilirken hata oluştu: {e}")
                else:
                    print(Fore.RED + "-" + f" {link} (proxy: {proxy})")
                
                time.sleep(1)

if __name__ == "__main__":
    main()
