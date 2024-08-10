# justpaste.it-link-finder


## Uygulama Açıklaması ve Kullanım Kılavuzu

### Uygulama Nedir?

Bu Python uygulaması, belirli bir URL yapısına sahip rastgele linkler oluşturarak bu linklerin geçerliliğini test eder ve geçerli olanları dosyaya kaydeder. Ayrıca, proxy'ler kullanarak bu testleri gerçekleştirir ve proxy kullanırken karşılaşılabilecek rate limitlerini yönetmeye yardımcı olur.

### Uygulamanın Temel Özellikleri:

1. **Rastgele URL Üretimi**: Belirli bir URL yapısına sahip rastgele linkler oluşturur.
2. **URL Geçerliliği Kontrolü**: Oluşturulan linklerin geçerli olup olmadığını kontrol eder.
3. **Proxy Kullanımı**: Proxy'ler kullanarak linklerin geçerliliğini test eder.
4. **Geçerli Linklerin Kaydedilmesi**: Geçerli olan linkleri ve kullanılan proxy'yi dosyaya kaydeder.
5. **Proxy Listesi**: Proxy sağlayıcısının API'sinden proxy listesi alır ve kullanır.
6. **Geçerli URL Sorgulaması**: Kullanıcıdan geçerli bir URL girmesini ister.

### Gereksinimler:

- Python 3.x
- `requests` kütüphanesi
- `colorama` kütüphanesi
- `tkinter` kütüphanesi (Python'un standart kütüphanesi)

### Kurulum ve Kullanım Adımları:

1. **Python ve Kütüphaneleri Kurun**:
   - Python 3.x'in bilgisayarınızda yüklü olduğundan emin olun.
   - Gerekli kütüphaneleri yükleyin:
     ```bash
     pip install requests colorama
     ```

2. **Kodunuzu Kopyalayın**:
   - Aşağıdaki Python kodunu bir dosyaya (örneğin, `proxy_url_checker.py`) yapıştırın:



3. **API Anahtarınızı ve Proxy URL'sini Güncelleyin**:
   - Kodu güncellerken API anahtarınızı (`api_key`) ve proxy sağlayıcısının API URL'sini doğru şekilde ayarladığınızdan emin olun.

4. **Uygulamayı Çalıştırın**:
   - Terminal veya komut istemcisine gidin ve aşağıdaki komutu çalıştırarak uygulamayı başlatın:
     ```bash
     python proxy_url_checker.py
     ```

5. **Geçerli URL'yi Girin**:
   - Uygulama başladığında, bir pencere açılacak ve geçerli bir URL girmeniz istenecek. Doğru URL'yi girene kadar tekrar deneyebilirsiniz.

6. **Proxy Listesi Yükleme**:
   - Proxy listesi, API'den alınacak ve uygulama tarafından kullanılacaktır.

7. **Geçerli Linklerin Kaydedilmesi**:
   - Geçerli linkler, `valid.txt` dosyasına kaydedilecektir. Her geçerli link ve kullanılan proxy bilgisi dosyada saklanacaktır.

### Özet

Bu uygulama, belirli bir URL yapısına sahip rastgele linkler oluşturarak geçerliliklerini test eder ve proxy'ler kullanarak bu testleri gerçekleştirir. Proxy'leri yönetmek ve API rate limitlerini aşmak için proxy havuzunu kullanır. Kullanıcıdan geçerli bir URL girmesi istenir ve geçerli linkler kaydedilir. 

Uygulamanın başarılı bir şekilde çalışabilmesi için API anahtarınızın ve proxy sağlayıcısının URL'sinin doğru olduğundan emin olun. Ayrıca, proxy sağlayıcınızın rate limit politikalarına ve kullanım şartlarına uyduğunuzdan emin olun.
