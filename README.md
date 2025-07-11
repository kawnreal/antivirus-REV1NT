# Güçlü Antivirüs Arayüzü

Python ve CustomTkinter kullanılarak geliştirilmiş, modern ve kullanıcı dostu bir antivirüs programı arayüzü projesi.

![Uygulama Ana Ekranı](https://imgur.com/gBDkvLF)
*(Not: Bu linki kendi ekran görüntünüzle güncelleyin.)*

## Tanıtım

Bu proje, bir antivirüs yazılımının temel kullanıcı arayüzü (UI) ve kullanıcı deneyimi (UX) bileşenlerini göstermek amacıyla oluşturulmuştur. Uygulama, animasyonlu bir başlangıç ekranı, bilgisayar sağlığını görselleştiren dinamik bir gösterge, farklı seviyelerde tarama seçenekleri ve bulunan tehditler için bir onay mekanizması gibi modern özellikler içerir.

Arka plan tarama mantığı, şu anda bilinen ve zararsız olan EICAR test virüsü hash'ini tespit eden bir simülasyon olarak kodlanmıştır. Bu proje, tam teşekküllü bir siber güvenlik çözümü olmaktan çok, karmaşık bir masaüstü uygulamasının nasıl tasarlanıp kodlanabileceğini gösteren bir eğitim materyali niteliğindedir.

## Özellikler

- **Modern ve Duyarlı Arayüz**: `customtkinter` ile oluşturulmuş estetik ve karanlık mod uyumlu tasarım.
- **Animasyonlu Başlangıç Ekranı**: Uygulama açılırken beliren profesyonel bir "Splash Screen".
- **Dinamik Sağlık Göstergesi**: Bilgisayarın güvenlik durumunu bir araba hız göstergesi benzeri bir tasarımla anlık olarak gösterir.
- **Çok Seviyeli Tarama**:
  - **Basit Tarama**: Yalnızca İndirilenler klasörünü tarar.
  - **Orta Düzey Tarama**: İndirilenler, Belgeler ve Temp klasörlerini tarar.
  - **Derin Tarama**: Tüm `C:\` sürücüsünü tarar (uzun sürebilir).
- **Onay Gerektiren Temizleme**: Tespit edilen tehditleri silmeden veya karantinaya almadan önce kullanıcıya bir liste sunar ve onay ister.
- **Donmayan Arayüz**: Tarama işlemleri, arayüzün donmasını engellemek için arka planda (`threading`) çalışır.

## Kurulum ve Çalıştırma

-Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin.

### 1. Projeyi Klonlayın

```bash
git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
cd your-repository-name
2. Sanal Ortam Oluşturun ve Aktive Edin (Önerilir)
```

# Windows
```bash
python -m venv venv
venv\Scripts\activate
```

# macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```
3. Gerekli Kütüphaneleri Yükleyin
- Proje için gerekli olan Python kütüphanelerini yükleyin.

```bash
pip install customtkinter
pip install Pillow
```

4. Logo Dosyasını Ekleyin
- Projenin başlangıç ekranında bir logo gösterebilmesi için, main.py dosyası ile aynı dizine logo.png adında bir resim dosyası ekleyin.

5. Uygulamayı Çalıştırın
- Aşağıdaki komutla uygulamayı başlatın.

```bash
python main.py
```

# Dosya Yapısı
├── venv/                   # Sanal ortam klasörü
├── main.py                 # Uygulamanın ana kodunu içeren dosya
├── logo.png                # Başlangıç ekranında gösterilen logo dosyası
└── README.md               # Bu bilgilendirme dosyası

# Teknik Detaylar ve Sınırlamalar
- Tarama Motoru: Tarama mantığı bir simülasyondur. Yalnızca EICAR standart test dosyasının SHA256 hash değerini arar. Bu program, gerçek dünyadaki virüslere karşı bir koruma sağlamaz.

- Karantina: "Temizle" fonksiyonu şu anda dosyaları silmez veya karantinaya almaz. Yalnızca konsola bir mesaj yazdırır ve arayüzü günceller.

- Veritabanı: Bilinen virüs imzaları için harici veya güncellenebilir bir veritabanı kullanılmamaktadır. Hash değerleri kodun içine gömülmüştür.

## Gelecek Geliştirmeler
- Bu proje, aşağıdaki özelliklerle daha da geliştirilebilir:

[ ] Gerçek İmza Veritabanı: Virüs imzalarını bir SQLite veritabanında saklama ve internet üzerinden güncelleme.

[ ] Gerçek Karantina Mekanizması: Tespit edilen dosyaları şifreleyerek güvenli bir klasöre taşıma.

[ ] Sezgisel (Heuristic) Analiz: Bilinmeyen tehditleri davranışlarına göre tespit etme.

[ ] Ayarlar Penceresi: Kullanıcının program ayarlarını (örneğin, başlangıçta çalışma, tarama zamanlaması) değiştirebileceği bir menü.

[ ] Detaylı Raporlama ve Günlükleme (Logging): Tüm tarama sonuçlarının ve işlemlerin bir dosyaya kaydedilmesi.

**BU UYGULAMA GEMİNİ YARDIMIYLA YAPILMIŞTIR.**
