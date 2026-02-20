# 🚀 HIZLI BAŞLANGIÇ

## 3 Adımda Bot Kurulumu

### 1️⃣ Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 2️⃣ Bot Token'ını Ayarlayın

1. Telegram'da [@BotFather](https://t.me/BotFather) botunu açın
2. `/newbot` yazın
3. Bot için bir isim verin (örn: "Namaz Vakitleri Bot")
4. Bot için kullanıcı adı verin (örn: "namaz_vakitleri_bot")
5. Aldığınız token'ı kopyalayın

6. `config.py` dosyasını açın ve token'ı yapıştırın:

```python
BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
```

### 3️⃣ Botu Başlatın

```bash
python3 main.py
```

## ✅ Bot Çalışıyor!

Artık Telegram'da botunuzu bulup kullanmaya başlayabilirsiniz:

1. Telegram'da botunuzu bulun (`@kullanici_adiniz`)
2. `/start` yazın
3. `/sehir Istanbul` yazarak şehrinizi ayarlayın
4. `/bildirim` ile bildirimleri açın
5. Tamamdır! 🎉

## 📱 Temel Kullanım

```
/start          → Botu başlat
/sehir Ankara   → Şehir seç
/vakit          → Namaz vakitlerini gör
/sonraki        → Sonraki namaz vakti
/bildirim       → Bildirimleri aç/kapat
/ezan           → Ezan hakkında bilgi
```

## ⚡ Otomatik Bildirimler

Bot her namaz vaktinde otomatik olarak bildirim gönderir:
- 🌙 İmsak
- ☀️ Öğle  
- 🌤️ İkindi
- 🌆 Akşam
- 🌃 Yatsı

## 🔧 Sorun mu var?

### "Bot yanıt vermiyor"
- Token'ın doğru olduğundan emin olun
- İnternet bağlantınızı kontrol edin

### "Bildirimler gelmiyor"
- `/bildirim` ile bildirimleri açın
- `/sehir [şehir]` ile şehri ayarlayın

## 📖 Daha Fazla Bilgi

Detaylı bilgi için `README.md` dosyasını okuyun.

---

**Hayırlı Kullanımlar! 🤲**
