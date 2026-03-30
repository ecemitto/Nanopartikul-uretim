State Machine Tabanlı Cihaz Kontrol Sistemi
Proje Amacı

Bu proje, gümüş nanopartikül sentezi gerçekleştiren bir cihazın **State Machine (Durum Makinesi)** mimarisi ile tam otomatik kontrolünü ve süreç simülasyonunu içerir. Kullanıcıdan alınan parametrelere göre otonom bir akış yönetir ve olası donanım arızalarına karşı gelişmiş güvenlik protokolleri sunar.

##  Öne Çıkan Özellikler

### 1. Otomatik Proses Akışı (Automation)
Süreç, manuel müdahale gerektirmeden aşağıdaki adımları sırasıyla takip eder:
* **MIXING:** Belirlenen süre boyunca karıştırma.
* **HEATING:** Hedef sıcaklığa ulaşana kadar ısıtma (Event-based transition).
* **SEPARATION & CLEANING:** Süre bazlı otomatik ayrıştırma ve temizleme adımları.
* **FINISH:** Süreç özeti ve parçacık boyutu hesaplaması.

### 2. Parametre Etkileşimi & Simülasyon
Sentez sonucu, girilen parametrelerin (RPM, Sıcaklık, Süre) bir fonksiyonu olarak hesaplanır:
- **Kinetik Etki:** Yüksek RPM değerleri, daha homojen dağılım ve küçük parçacık boyutu ($nm$) simüle eder.
- **Termal Etki:** İdeal sentez sıcaklığından (70°C) sapmalar, modelde parçacık büyümesine (aglomerasyon) neden olur.

### 3. Gelişmiş Hata Yönetimi & Fail-Safe
Endüstriyel güvenlik standartlarına uygun olarak sistemde **Safety Interlock (Güvenlik Kilidi)** mekanizması bulunmaktadır:
* **Hata Tipleri:** Aşırı Isınma (>115°C), Yüksek RPM Kararsızlığı (>1800), Düşük Tork/Motor Sıkışması (<50 RPM).
* **Interlock:** Hata oluştuğunda sistem `FAIL_SAFE` moduna geçer; hata sıfırlanmadan (`RESET`) sistemin yeniden başlatılması engellenir.
* **Logging:** Tüm süreç adımları ve hata raporları zaman damgalı olarak `process_log.txt` dosyasına kaydedilir.

## 🛠️ Teknik Detaylar
- **Dil:** Python 3.x
- **Kütüphaneler:** `tkinter` (UI), `enum`, `datetime`
- **Mimari:** Event-Driven State Machine

## 🚀 Kurulum ve Çalıştırma
1. Proje dosyalarını bilgisayarınıza indirin.
2. Terminal veya komut satırına `python main.py` yazarak uygulamayı başlatın.
3. Arayüz üzerinden parametreleri (Sıcaklık, RPM, Süre) belirleyin ve **BAŞLAT** butonuna tıklayın.

---

### 💡 Geliştirici Notu
Bu çalışma; sadece bir kod prototipi değil, hata payını minimize eden, izlenebilir (logging) ve bilimsel varsayımlara dayalı bir **Sistem Tasarımı** yaklaşımıyla geliştirilmiştir.
