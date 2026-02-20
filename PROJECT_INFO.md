# 📁 PROJE DOSYALARI

## Ana Dosyalar

### `main.py` (18KB)
Bot'un ana dosyası. Tüm komutları, mesaj işleyicilerini ve otomatik bildirim sistemini içerir.

**İçerdikleri:**
- Tüm Telegram komut işleyicileri (/start, /sehir, /vakit, vb.)
- Otomatik ezan bildirimi sistemi
- Zamanlayıcı (scheduler) yapılandırması
- Mesaj ve callback işleyicileri

### `config.py` (5.3KB)
Bot yapılandırma dosyası.

**İçerdikleri:**
- Bot token ayarı
- Türkiye'nin 81 ilinin listesi
- API ayarları
- Namaz isimleri
- Veritabanı ayarları

**ÖNEMLİ:** Bu dosyayı GitHub'a yüklemeyin! Token bilgisi içerir.

### `database.py` (6.9KB)
SQLite veritabanı yönetim modülü.

**İşlevleri:**
- Grup ve kullanıcı kayıtları
- Şehir ayarları
- Bildirim tercih yönetimi
- Ezan geçmişi kayıtları
- İstatistik verileri

### `prayer_times.py` (6.6KB)
Namaz vakitleri API entegrasyonu.

**İşlevleri:**
- Aladhan API entegrasyonu
- Yedek API desteği
- Şehir arama ve eşleştirme
- Namaz vakitleri formatlama
- Sonraki namaz hesaplama

## Yardımcı Dosyalar

### `requirements.txt` (63B)
Python bağımlılıkları listesi:
- python-telegram-bot (Telegram Bot API)
- requests (HTTP istekleri)
- APScheduler (Zamanlama sistemi)

### `README.md` (6.2KB)
Detaylı kullanım kılavuzu ve dokümantasyon.

### `QUICK_START.md` (1.7KB)
3 adımda hızlı başlangıç rehberi.

### `config_example.py` (416B)
Örnek config dosyası. Kullanıcılar bunu `config.py` olarak kopyalayıp token'larını girecek.

### `.gitignore` (239B)
Git için yok sayılacak dosyalar (veritabanı, config, vb.)

### `install.sh` (1.3KB)
Otomatik kurulum scripti (Linux/Mac).

### `ezanbot.service` (996B)
Linux sistemd servisi template'i. Botu sistem servisi olarak çalıştırmak için.

## Otomatik Oluşacak Dosyalar

### `ezan_bot.db`
SQLite veritabanı. Bot ilk çalıştırıldığında otomatik oluşturulur.

**Tablolar:**
- `groups` - Grup bilgileri
- `users` - Kullanıcı bilgileri  
- `prayer_history` - Gönderilen bildirim geçmişi

## Proje Yapısı

```
ezan_bot/
│
├── 📄 main.py                  # Ana bot dosyası
├── 📄 config.py                # Yapılandırma (GİZLİ)
├── 📄 database.py              # Veritabanı yönetimi
├── 📄 prayer_times.py          # Namaz vakitleri API
├── 📄 requirements.txt         # Python bağımlılıkları
│
├── 📖 README.md                # Detaylı dokümantasyon
├── 📖 QUICK_START.md           # Hızlı başlangıç
├── 📖 PROJECT_INFO.md          # Bu dosya
│
├── 🔧 config_example.py        # Config örneği
├── 🔧 install.sh               # Kurulum scripti
├── 🔧 ezanbot.service          # Systemd servisi
├── 🔧 .gitignore              # Git yok sayma
│
└── 💾 ezan_bot.db             # Veritabanı (otomatik)
```

## Kod Satır Sayıları

```
main.py:         ~500 satır
database.py:     ~180 satır
prayer_times.py: ~200 satır
config.py:       ~100 satır
─────────────────────────
TOPLAM:         ~980 satır
```

## Özellikler

✅ **Profesyonel Kod Yapısı**
- Modüler tasarım
- Hata yönetimi
- Logging sistemi
- Dokümantasyon

✅ **Veritabanı Sistemi**
- SQLite entegrasyonu
- Kullanıcı/grup yönetimi
- Bildirim tercihleri
- Geçmiş kayıtları

✅ **API Entegrasyonu**
- Aladhan API (ana)
- Yedek API desteği
- Hata yönetimi
- Türkçe karakter desteği

✅ **Otomatik Bildirim**
- Her dakika kontrol
- APScheduler kullanımı
- Çoklu grup desteği
- Log kayıtları

✅ **Kullanıcı Dostu**
- Türkçe arayüz
- Akıllı şehir arama
- Klavye butonları
- Yardım sistemi

## Gereksinimler

- **Python:** 3.8+
- **RAM:** 128MB (minimum)
- **Disk:** 50MB (veritabanı dahil)
- **Network:** İnternet bağlantısı

## Deployment Seçenekleri

1. **Lokal** - Kendi bilgisayarınızda
2. **VPS** - Cloud sunucu (Ubuntu/Debian)
3. **Heroku** - Ücretsiz hosting
4. **Docker** - Container ortamı
5. **Systemd** - Linux sistem servisi

## Güvenlik

🔒 **Dikkat Edilmesi Gerekenler:**
- Bot token'ını paylaşmayın
- config.py dosyasını GitHub'a yüklemeyin
- .gitignore kullanın
- Sunucuda güvenlik güncellemelerini yapın

## Destek

📧 Sorularınız için Telegram'dan iletişime geçin.
⭐ Projeyi beğendiyseniz GitHub'da yıldız vermeyi unutmayın!

---

**Hayırlı Kullanımlar! 🕌**
