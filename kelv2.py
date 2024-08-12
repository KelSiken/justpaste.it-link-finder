import requests
import random
import string
import time
import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
from colorama import Fore, init
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Konsol renklerini etkinleştir
init(autoreset=True)

# URL yapısının sabit kısmı
base_url = "https://discord.gg/"

# Geçerli linkleri kaydetmek için dosya
valid_file = "valid_invites.txt"

# Discord Webhook URL'si
discord_webhook_url = "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"

def generate_random_suffix(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

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

def check_invite_code(invite_code, chromedriver_path, timeout=10):
    url = base_url + invite_code
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Tarayıcıyı başsız modda çalıştır
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)

    try:
        # Sayfanın tamamen yüklenmesini bekle
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
        )
        
        # Geçersiz davet elemanını kontrol et
        invalid_element = driver.find_elements(By.CSS_SELECTOR, "div.contents_dd4f85")
        return not invalid_element  # Eğer eleman yoksa, link geçerlidir

    except Exception as e:
        print(Fore.RED + f"Hata: {e}")
        return False
    finally:
        driver.quit()

def load_proxies(file_path):
    with open(file_path, 'r') as file:
        proxies = file.read().splitlines()
    return proxies

def select_file():
    root = tk.Tk()
    root.withdraw()  # Ana pencereyi gizle
    file_path = filedialog.askopenfilename(title="Proxy Listesi Seçin", filetypes=[("Text Files", "*.txt")])
    return file_path

def show_error(message):
    root = tk.Tk()
    root.withdraw()  # Ana pencereyi gizle
    messagebox.showerror("Hata", message)

def send_to_discord(invite_link, file_path):
    with open(file_path, 'rb') as file:
        files = {'file': ('screenshot.png', file)}
        data = {
            "content": f"Geçerli davet linki: {invite_link}"
        }
        response = requests.post(discord_webhook_url, data=data, files=files)
        if response.status_code == 204:
            print(Fore.GREEN + "Discord'a başarıyla gönderildi.")
        else:
            print(Fore.RED + "Discord gönderimi başarısız oldu.")

def main():
    # Kullanıcıdan chromedriver yolunu seçmesini isteyin
    chromedriver_path = open_chrome_with_chromedriver_path()
    if not chromedriver_path:
        return

    # Proxy listesini seçme
    proxy_file = select_file()
    if not proxy_file:
        print(Fore.RED + "Proxy dosyası seçilmedi. Program sonlandırılıyor.")
        return
    
    proxies_list = load_proxies(proxy_file)
    if not proxies_list:
        print(Fore.RED + "Proxy listesi boş. Program sonlandırılıyor.")
        return

    print(Fore.YELLOW + "Proxy listesi yüklendi. Davet linki denemeleri başlayacak...")

    # Sonsuz döngü
    with open(valid_file, "a") as file:  # 'a' ile dosyayı açarak sürekli ekleme yaparız
        while True:
            for proxy in proxies_list:
                proxy_dict = {"http": proxy, "https": proxy}
                # Rastgele bir davet kodu oluştur
                invite_code = generate_random_suffix()
                link = base_url + invite_code
                
                # Davet kodunu kontrol et
                if check_invite_code(invite_code, chromedriver_path):
                    try:
                        file.write(f"{link} (proxy: {proxy})\n")
                        file.flush()  # Dosyaya hemen yazmak için flush() kullanılır
                        print(Fore.GREEN + "+" + f" {link} (proxy: {proxy}) (kaydedildi)")

                        # Ekran görüntüsü alma ve Discord'a gönderme işlemleri burada yapılabilir
                        # Örneğin, `send_to_discord(link, "screenshot.png")` ile Discord'a gönderim yapılabilir

                    except Exception as e:
                        print(Fore.RED + "-" + f" {link} (proxy: {proxy}) (kaydedilemedi: {e})")
                        show_error(f"Davet linki {link} (proxy: {proxy}) kaydedilirken veya Discord'a gönderilirken hata oluştu: {e}")
                else:
                    print(Fore.RED + "-" + f" {link} (proxy: {proxy})")
                
                time.sleep(1)

if __name__ == "__main__":
    main()
