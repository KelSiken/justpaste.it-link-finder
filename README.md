Bu kod, belirli bir URL yapısına sahip rastgele linkler oluşturarak geçerliliklerini test eder ve proxy'ler kullanarak bu testleri gerçekleştirir. Geçerli olan linkleri bir dosyaya kaydeder. Aşağıda kodun işleyişini ve uygulamanın nasıl kullanılacağını adım adım açıklayan bir rehber bulabilirsiniz:
![image](https://github.com/user-attachments/assets/6e0151f6-7231-4849-8845-0631c55995fe)


### Kodun Açıklaması

1. **Gerekli Kütüphaneler**:
   - `requests`: HTTP istekleri yapmak için.
   - `string` ve `random`: Rastgele karakterler üretmek için.
   - `time`: İstekler arasında bekleme süresi eklemek için.
   - `tkinter`: Kullanıcıdan dosya ve URL almak için grafiksel arayüz.
   - `colorama`: Konsol renklerini yönetmek için.

2. **Fonksiyonlar**:
   - `generate_random_suffix(length=5)`: Belirtilen uzunlukta rastgele bir URL uzantısı üretir.
   - `check_url(link, proxies=None)`: URL'nin geçerli olup olmadığını kontrol eder. Proxy kullanımı opsiyoneldir.
   - `load_proxies(file_path)`: Belirtilen dosyadan proxy'leri okur ve bir liste olarak döner.
   - `select_file()`: Proxy listesi içeren bir dosya seçmek için bir dosya seçici açar.
   - `get_valid_url()`: Kullanıcıdan geçerli bir URL girmesini ister ve bu URL'nin geçerli olup olmadığını kontrol eder.

3. **Ana Fonksiyon (`main`)**:
   - Kullanıcıdan geçerli bir URL alır.
   - Proxy listesi içeren dosyayı seçer ve proxy'leri yükler.
   - Sonsuz döngüde rastgele URL'ler oluşturur, bu URL'leri proxy'ler kullanarak kontrol eder ve geçerli olanları dosyaya kaydeder.

### Uygulamanın Çalışması İçin Adımlar

1. **Python ve Kütüphaneleri Kurun**:
   - Python 3.x'in bilgisayarınızda yüklü olduğundan emin olun.
   - Gerekli Python kütüphanelerini yükleyin:
     ```bash
     pip install requests colorama
     ```

2. **Python Kodunu Kaydedin**:
   - Aşağıdaki Python kodunu bir dosyaya (örneğin, `proxy_url_checker.py`) yapıştırın ve kaydedin:

     ```python
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
         valid_url = get_valid_url()
         print(Fore.YELLOW + f"Geçerli URL alındı: {valid_url}")

         proxy_file = select_file()
         if not proxy_file:
             print(Fore.RED + "Proxy dosyası seçilmedi. Program sonlandırılıyor.")
             return

         proxies_list = load_proxies(proxy_file)
         if not proxies_list:
             print(Fore.RED + "Proxy listesi boş. Program sonlandırılıyor.")
             return

         print(Fore.YELLOW + "Proxy listesi yüklendi. URL denemeleri başlayacak...")

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
                             print(Fore.GREEN + "+" + f" {link} (proxy: {proxy}) (kaydedildi)")
                         except Exception as e:
                             print(Fore.RED + "-" + f" {link} (proxy: {proxy}) (kaydedilemedi: {e})")
                     else:
                         print(Fore.RED + "-" + f" {link} (proxy: {proxy})")

                     time.sleep(1)

     if __name__ == "__main__":
         main()
     ```

1. Gerekli Kütüphaneler ve Araçlar
Python: Python 3.x versiyonu gereklidir.

Kütüphaneler: Kodun çalışması için bazı kütüphaneler yüklenmiş olmalıdır:

requests
selenium
colorama
tkinter (Python'un standart kütüphanesi olarak gelir, ayrıca yüklenmesine gerek yoktur)
webdriver-manager (Opsiyonel, Chromedriver için alternatif bir yöntem)
Bu kütüphaneleri yüklemek için terminalde şu komutu çalıştırabilirsiniz:

bash
Kodu kopyala
pip install requests selenium colorama
Chromedriver: Selenium ile Chrome tarayıcısını kontrol etmek için gerekli. Buradan uygun versiyonu indirebilirsiniz.

2. Dosya ve Ayarların Hazırlanması
Chromedriver Dosyası: Chromedriver'ın bilgisayarınızdaki yolu gerekecek. Bu dosyayı indirip yerel bir dizine koyun.

Proxy Listesi: Proxy adreslerini içeren bir metin dosyası oluşturun. Her satıra bir proxy adresi olacak şekilde düzenleyin. Örneğin:

makefile
Kodu kopyala
104.207.38.25:3128
123.456.78.90:8080
Discord Webhook URL'si: Discord sunucunuzda bir webhook oluşturun ve URL'yi alın. Discord Webhook Dokümantasyonu ile ilgili bilgi alabilirsiniz.

3. Kodun Kullanımı
Kodun Çalıştırılması:

Kod dosyasını (örneğin script.py olarak kaydedin) Python ile çalıştırın:
bash
Kodu kopyala
python script.py
İlk Çalıştırma:

İlk kez çalıştırdığınızda, program sizden Chromedriver dosyasını ve proxy listesini seçmenizi ister. Bu seçimler config.json dosyasına kaydedilir, böylece sonraki çalıştırmalarda bu seçimleri tekrar yapmanız gerekmez.
Prosedürler:

Proxy Listesi Seçimi: Proxy liste dosyanızın yolunu seçin.
Chromedriver Seçimi: Chromedriver dosyanızın yolunu seçin.
URL Doğrulama: Program, geçerli bir URL girmenizi isteyecek ve URL'nin erişilebilirliğini test edecektir.
Sürekli Çalışma:

Program, proxy listesinde belirtilen her proxy ile rastgele oluşturulmuş URL'leri test eder.
Geçerli URL'leri bulduğunda, ekran görüntüsünü alır ve Discord'a gönderir.
Geçerli URL'leri ve proxy bilgilerini valid.txt dosyasına kaydeder.
4. Programın Yeniden Başlatılması
Program bir hata ile karşılaştığında otomatik olarak kendini yeniden başlatır. Bu, kodun kesintisiz bir şekilde çalışmasını sağlar.

5. Önemli Notlar
Yüksek Sistem Kaynağı Kullanımı: Ekran görüntüsü almak ve çeşitli URL'leri test etmek, sistem kaynaklarını (CPU ve bellek) tüketebilir.
Yasal Durum: Proxy kullanımı ve web scraping işlemleri yasal sorunlara yol açabilir. Hedef sitelerin kullanım şartlarını kontrol ettiğinizden emin olun.

### Özet

Bu uygulama, belirli bir URL yapısına sahip rastgele linkler oluşturur ve geçerliliklerini proxy'ler kullanarak test eder. Proxy listesi dosyası ile çalışır ve geçerli linkleri bir dosyaya kaydeder. Uygulamanın başarılı bir şekilde çalışması için doğru proxy listesi ve geçerli URL'nin girilmesi önemlidir.
