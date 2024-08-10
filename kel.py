import requests
import string
import random
import time
import tkinter as tk
from tkinter import simpledialog, filedialog
from colorama import Fore, init

# Konsol renklerini etkinleştir
init(autoreset=True)

# URL yapısının sabit kısmı
base_url = "https://justpaste.it/"

# Geçerli linkleri kaydetmek için dosya
valid_file = "valid.txt"

def generate_random_suffix(length=5):
    # Rastgele bir URL uzantısı üretir (küçük harfler, büyük harfler ve rakamlar)
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
                    except Exception as e:
                        print(Fore.RED + "-" + f" {link} (proxy: {proxy}) (kaydedilemedi: {e})")
                else:
                    print(Fore.RED + "-" + f" {link} (proxy: {proxy})")
                
                time.sleep(1)


if __name__ == "__main__":
    main()

