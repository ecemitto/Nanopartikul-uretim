State Machine Tabanlı Cihaz Kontrol Sistemi
Proje Amacı

Bu proje, bir cihazın çalışma sürecini state machine (durum makinesi) yaklaşımıyla modellemek ve bu yapıyı basit bir Tkinter tabanlı kullanıcı arayüzü ile kontrol edilebilir hale getirmek amacıyla geliştirilmiştir.

Kullanılan Yaklaşım

Cihazın tüm çalışma akışı Enum kullanılarak tanımlanmış durumlar üzerinden ilerlemektedir.
Durum geçişleri merkezi bir DeviceController sınıfı tarafından yönetilmektedir. Bu sayede sistem daha okunabilir, kontrollü ve genişletilebilir bir yapıya sahiptir.

Durum Akışı

IDLE → START → MIXING → HEATING → SEPARATION → CLEANING → FINISH → IDLE

Herhangi bir aşamada hata oluşması durumunda sistem FAIL-SAFE moduna geçerek işlemleri güvenli şekilde durdurur.

Hata ve Güvenlik Yönetimi

Isıtma aşamasında sıcaklık belirli bir eşik değerin üzerine çıkarsa sistem otomatik olarak hata durumuna geçer ve:

Tüm kontrol parametreleri sıfırlanır

Cihaz güvenli duruma alınır

Bu yapı, gerçek sistemlerde kullanılan temel güvenlik mantığını simüle etmektedir.

Kullanıcı Arayüzü

Tkinter kullanılarak geliştirilen arayüz üzerinden:

Sıcaklık, karıştırma hızı ve süre ayarlanabilir

Sistem başlatılabilir veya durdurulabilir

Cihazın anlık durumu canlı olarak izlenebilir

Not

Bu proje bir simülasyon çalışmasıdır ve gerçek donanım kontrolü içermemektedir. Amaç, durum tabanlı kontrol mantığını ve yazılım mimarisini göstermektir.

