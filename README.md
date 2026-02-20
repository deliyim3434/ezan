# 🕌 Ezan Vakitleri Telegram Botu

Türkiye'nin 81 ili için namaz vakitlerini gösteren ve otomatik ezan bildirimleri yapan profesyonel Telegram botu.

## ✨ Özellikler

- ✅ **81 İl Desteği**: Türkiye'nin tüm illeri için namaz vakitleri
- ✅ **Otomatik Bildirimler**: Her namaz vaktinde otomatik bildirim
- ✅ **Hicri Takvim**: Miladi ve Hicri tarih desteği
- ✅ **Sonraki Namaz**: Bir sonraki namaz vaktini gösterme
- ✅ **Grup Desteği**: Hem özel mesaj hem de grup sohbetlerinde çalışır
- ✅ **Akıllı Arama**: Şehir isimlerini Türkçe karakterlerle arayabilme
- ✅ **Veritabanı**: SQLite ile kullanıcı ve grup ayarlarını kaydetme
- ✅ **API Yedekleme**: Ana API çalışmazsa yedek API'ye geçiş

## 📋 Gereksinimler

- Python 3.8 veya üzeri
- Telegram Bot Token (BotFather'dan alınacak)
- İnternet bağlantısı

## 🚀 Kurulum

### 1. Projeyi İndirin

```bash
# Projeyi klonlayın veya indirin
cd ezan_bot
```

### 2. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 3. Bot Token'ı Alın

1. Telegram'da [@BotFather](https://t.me/BotFather) botunu açın
2. `/newbot` komutunu gönderin
3. Bot için bir isim ve kullanıcı adı belirleyin
4. Aldığınız token'ı kopyalayın

### 4. Yapılandırma

`config.py` dosyasını açın ve `BOT_TOKEN` değerini BotFather'dan aldığınız token ile değiştirin:

```python
BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
```

### 5. Botu Başlatın

```bash
python main.py
```

## 📱 Kullanım

### Temel Komutlar

| Komut | Açıklama | Örnek |
|-------|----------|-------|
| `/start` | Botu başlatır | `/start` |
| `/sehir [şehir]` | Şehir ayarlar | `/sehir Istanbul` |
| `/vakit` | Namaz vakitlerini gösterir | `/vakit` |
| `/sonraki` | Sonraki namaz vaktini gösterir | `/sonraki` |
| `/tum` | Tüm illeri listeler | `/tum` |
| `/ilbul [arama]` | Şehir arar | `/ilbul anka` |
| `/bildirim` | Bildirimleri aç/kapat | `/bildirim` |
| `/ezan` | Ezan hakkında bilgi | `/ezan` |
| `/yardim` | Yardım menüsü | `/yardim` |

### Hızlı Başlangıç

1. Botu başlatın: `/start`
2. Şehrinizi ayarlayın: `/sehir Istanbul`
3. Bildirimleri açın: `/bildirim`
4. Artık her namaz vaktinde otomatik bildirim alacaksınız! 🎉

### Örnek Kullanım

```
Kullanıcı: /sehir Ankara
Bot: ✅ Şehir ayarlandı: Ankara

🕌 Ankara - Namaz Vakitleri

📅 20 Feb 2026
🌙 Hicri: 21 Şaban 1447

🌙 İmsak: 05:42
🌅 Güneş: 07:08
☀️ Öğle: 12:45
🌤️ İkindi: 15:38
🌆 Akşam: 18:12
🌃 Yatsı: 19:33
```

## 🔧 Gelişmiş Ayarlar

### Veritabanı

Bot, kullanıcı ve grup ayarlarını `ezan_bot.db` SQLite veritabanında saklar. Bu dosya otomatik olarak oluşturulur.

### API Ayarları

`config.py` dosyasında iki farklı API kullanılır:

1. **Ana API**: Aladhan API (Uluslararası)
2. **Yedek API**: Türk Ezan Vakitleri API

Ana API çalışmazsa otomatik olarak yedek API'ye geçiş yapılır.

### Otomatik Bildirimler

Bot, her dakika tüm kayıtlı sohbetler için namaz vakitlerini kontrol eder. Namaz vakti geldiğinde otomatik olarak bildirim gönderir.

Bildirim sistemi:
- Her dakikanın başında çalışır
- Bildirimi açık olan tüm sohbetlere gönderir
- Her namaz vaktinde bir kez bildirim yapar
- Güneş doğuşu için bildirim göndermez

### Özelleştirme

#### Ezan Sesi Eklemek

`config.py` dosyasında `AZAN_AUDIO_URL` değişkenini bir ezan sesi URL'si ile güncelleyebilirsiniz:

```python
AZAN_AUDIO_URL = "https://example.com/azan.mp3"
```

Ardından `main.py` dosyasındaki `send_prayer_notification` fonksiyonuna ses gönderme özelliğini ekleyin.

## 📊 Dosya Yapısı

```
ezan_bot/
│
├── main.py              # Ana bot dosyası
├── config.py            # Yapılandırma ayarları
├── database.py          # Veritabanı yönetimi
├── prayer_times.py      # Namaz vakitleri API'si
├── requirements.txt     # Python bağımlılıkları
├── README.md           # Bu dosya
└── ezan_bot.db         # SQLite veritabanı (otomatik oluşur)
```

## 🔒 Güvenlik

- Bot token'ınızı asla paylaşmayın
- `config.py` dosyasını GitHub'a yüklemeyin
- Gerekirse `.gitignore` dosyası oluşturun:

```
ezan_bot.db
config.py
__pycache__/
*.pyc
```

## 🌐 Deployment (Sunucuya Kurulum)

### Heroku

1. Heroku hesabı oluşturun
2. Yeni bir uygulama oluşturun
3. Git repository'sini bağlayın
4. Config Vars'a `BOT_TOKEN` ekleyin
5. Deploy edin

### VPS (Ubuntu/Debian)

```bash
# Projeyi sunucuya yükleyin
cd /home/user/ezan_bot

# Sanal ortam oluşturun
python3 -m venv venv
source venv/bin/activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Systemd servisi oluşturun
sudo nano /etc/systemd/system/ezanbot.service
```

Servis dosyası içeriği:
```ini
[Unit]
Description=Ezan Vakitleri Telegram Bot
After=network.target

[Service]
Type=simple
User=user
WorkingDirectory=/home/user/ezan_bot
ExecStart=/home/user/ezan_bot/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Servisi başlatın:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ezanbot
sudo systemctl start ezanbot
sudo systemctl status ezanbot
```

## 🐛 Sorun Giderme

### Bot yanıt vermiyor
- Token'ın doğru girildiğinden emin olun
- İnternet bağlantınızı kontrol edin
- Bot loglarını kontrol edin

### Bildirimler gelmiyor
- `/bildirim` komutu ile bildirimlerin açık olduğundan emin olun
- Şehir ayarının yapıldığını kontrol edin (`/sehir [şehir]`)
- Bot loglarını kontrol edin

### API hatası
- İnternet bağlantısını kontrol edin
- API'lerin çalıştığından emin olun
- Yedek API otomatik devreye girecektir

## 📝 Lisans

Bu proje açık kaynaklıdır ve özgürce kullanılabilir.

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Pull request göndermekten çekinmeyin.

## 📧 İletişim

Sorularınız için: [Telegram: @YourUsername]

## 🙏 Teşekkürler

- [Aladhan API](https://aladhan.com/prayer-times-api) - Namaz vakitleri API'si
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot API wrapper

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!

**Hayırlı Kullanımlar! 🤲**
