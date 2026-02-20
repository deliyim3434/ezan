# Telegram Bot Konfigürasyonu

# Bot Token - BotFather'dan alınacak
BOT_TOKEN = "8598752603:AAGXwCDR1xHr6sskJDH_LSeOdIV9CCuNqxQ"

# API Ayarları
PRAYER_TIMES_API = "https://api.aladhan.com/v1/timingsByCity"
BACKUP_API = "https://ezanvakti.herokuapp.com/vakitler"

# Türkiye'nin 81 İli
TURKISH_CITIES = {
    "adana": {"name": "Adana", "country": "Turkey"},
    "adıyaman": {"name": "Adıyaman", "country": "Turkey"},
    "afyonkarahisar": {"name": "Afyonkarahisar", "country": "Turkey"},
    "ağrı": {"name": "Ağrı", "country": "Turkey"},
    "aksaray": {"name": "Aksaray", "country": "Turkey"},
    "amasya": {"name": "Amasya", "country": "Turkey"},
    "ankara": {"name": "Ankara", "country": "Turkey"},
    "antalya": {"name": "Antalya", "country": "Turkey"},
    "ardahan": {"name": "Ardahan", "country": "Turkey"},
    "artvin": {"name": "Artvin", "country": "Turkey"},
    "aydın": {"name": "Aydın", "country": "Turkey"},
    "balıkesir": {"name": "Balıkesir", "country": "Turkey"},
    "bartın": {"name": "Bartın", "country": "Turkey"},
    "batman": {"name": "Batman", "country": "Turkey"},
    "bayburt": {"name": "Bayburt", "country": "Turkey"},
    "bilecik": {"name": "Bilecik", "country": "Turkey"},
    "bingöl": {"name": "Bingöl", "country": "Turkey"},
    "bitlis": {"name": "Bitlis", "country": "Turkey"},
    "bolu": {"name": "Bolu", "country": "Turkey"},
    "burdur": {"name": "Burdur", "country": "Turkey"},
    "bursa": {"name": "Bursa", "country": "Turkey"},
    "çanakkale": {"name": "Çanakkale", "country": "Turkey"},
    "çankırı": {"name": "Çankırı", "country": "Turkey"},
    "çorum": {"name": "Çorum", "country": "Turkey"},
    "denizli": {"name": "Denizli", "country": "Turkey"},
    "diyarbakır": {"name": "Diyarbakır", "country": "Turkey"},
    "düzce": {"name": "Düzce", "country": "Turkey"},
    "edirne": {"name": "Edirne", "country": "Turkey"},
    "elazığ": {"name": "Elazığ", "country": "Turkey"},
    "erzincan": {"name": "Erzincan", "country": "Turkey"},
    "erzurum": {"name": "Erzurum", "country": "Turkey"},
    "eskişehir": {"name": "Eskişehir", "country": "Turkey"},
    "gaziantep": {"name": "Gaziantep", "country": "Turkey"},
    "giresun": {"name": "Giresun", "country": "Turkey"},
    "gümüşhane": {"name": "Gümüşhane", "country": "Turkey"},
    "hakkari": {"name": "Hakkari", "country": "Turkey"},
    "hatay": {"name": "Hatay", "country": "Turkey"},
    "iğdır": {"name": "Iğdır", "country": "Turkey"},
    "ısparta": {"name": "Isparta", "country": "Turkey"},
    "istanbul": {"name": "Istanbul", "country": "Turkey"},
    "izmir": {"name": "Izmir", "country": "Turkey"},
    "kahramanmaraş": {"name": "Kahramanmaraş", "country": "Turkey"},
    "karabük": {"name": "Karabük", "country": "Turkey"},
    "karaman": {"name": "Karaman", "country": "Turkey"},
    "kars": {"name": "Kars", "country": "Turkey"},
    "kastamonu": {"name": "Kastamonu", "country": "Turkey"},
    "kayseri": {"name": "Kayseri", "country": "Turkey"},
    "kilis": {"name": "Kilis", "country": "Turkey"},
    "kırıkkale": {"name": "Kırıkkale", "country": "Turkey"},
    "kırklareli": {"name": "Kırklareli", "country": "Turkey"},
    "kırşehir": {"name": "Kırşehir", "country": "Turkey"},
    "kocaeli": {"name": "Kocaeli", "country": "Turkey"},
    "konya": {"name": "Konya", "country": "Turkey"},
    "kütahya": {"name": "Kütahya", "country": "Turkey"},
    "malatya": {"name": "Malatya", "country": "Turkey"},
    "manisa": {"name": "Manisa", "country": "Turkey"},
    "mardin": {"name": "Mardin", "country": "Turkey"},
    "mersin": {"name": "Mersin", "country": "Turkey"},
    "muğla": {"name": "Muğla", "country": "Turkey"},
    "muş": {"name": "Muş", "country": "Turkey"},
    "nevşehir": {"name": "Nevşehir", "country": "Turkey"},
    "niğde": {"name": "Niğde", "country": "Turkey"},
    "ordu": {"name": "Ordu", "country": "Turkey"},
    "osmaniye": {"name": "Osmaniye", "country": "Turkey"},
    "rize": {"name": "Rize", "country": "Turkey"},
    "sakarya": {"name": "Sakarya", "country": "Turkey"},
    "samsun": {"name": "Samsun", "country": "Turkey"},
    "şanlıurfa": {"name": "Şanlıurfa", "country": "Turkey"},
    "siirt": {"name": "Siirt", "country": "Turkey"},
    "sinop": {"name": "Sinop", "country": "Turkey"},
    "sivas": {"name": "Sivas", "country": "Turkey"},
    "şırnak": {"name": "Şırnak", "country": "Turkey"},
    "tekirdağ": {"name": "Tekirdağ", "country": "Turkey"},
    "tokat": {"name": "Tokat", "country": "Turkey"},
    "trabzon": {"name": "Trabzon", "country": "Turkey"},
    "tunceli": {"name": "Tunceli", "country": "Turkey"},
    "uşak": {"name": "Uşak", "country": "Turkey"},
    "van": {"name": "Van", "country": "Turkey"},
    "yalova": {"name": "Yalova", "country": "Turkey"},
    "yozgat": {"name": "Yozgat", "country": "Turkey"},
    "zonguldak": {"name": "Zonguldak", "country": "Turkey"}
}

# Ezan İsimleri
PRAYER_NAMES = {
    "Fajr": "İmsak",
    "Sunrise": "Güneş",
    "Dhuhr": "Öğle",
    "Asr": "İkindi",
    "Maghrib": "Akşam",
    "Isha": "Yatsı"
}

# Ezan bildirimi için kullanılacak
PRAYER_NOTIFICATIONS = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]

# Ezan Sesi (Opsiyonel - ses dosyası URL'i)
AZAN_AUDIO_URL = None  # Buraya ezan sesi URL'i eklenebilir

# Veritabanı
DATABASE_NAME = "ezan_bot.db"
