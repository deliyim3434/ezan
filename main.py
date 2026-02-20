import logging
import asyncio
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from telegram.constants import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

import config
from database import Database
from prayer_times import PrayerTimes

# Logging ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global nesneler
db = Database()
prayer_api = PrayerTimes()
scheduler = AsyncIOScheduler()

class EzanBot:
    def __init__(self, token):
        self.token = token
        self.app = None
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Başlangıç komutu"""
        user = update.effective_user
        chat = update.effective_chat
        
        # Kullanıcı/Grup veritabanına ekle
        if chat.type == 'private':
            db.add_user(user.id, user.username, user.first_name)
        else:
            db.add_group(chat.id, chat.title)
        
        welcome_message = f"""
🕌 **Ezan Vakitleri Botuna Hoş Geldiniz!**

Merhaba {user.first_name}! 

Bu bot ile Türkiye'nin 81 ili için namaz vakitlerini öğrenebilir ve otomatik ezan bildirimleri alabilirsiniz.

**📋 Komutlar:**

🔹 /sehir [şehir adı] - Şehrinizi ayarlayın
   Örnek: /sehir Istanbul
   
🔹 /vakit - Güncel namaz vakitlerini görün

🔹 /sonraki - Sonraki namaz vaktini öğrenin

🔹 /ilbul [şehir] - Şehir arayın
   Örnek: /ilbul anka

🔹 /tum - Tüm illeri listeleyin

🔹 /bildirim - Otomatik bildirimleri aç/kapat

🔹 /ezan - Ezan bilgisi

🔹 /yardim - Yardım menüsü

**⚙️ Özellikler:**
✅ 81 il için namaz vakitleri
✅ Otomatik ezan bildirimleri
✅ Hicri takvim desteği
✅ Sonraki namaz bildirimi
✅ Grup desteği

Kullanmaya başlamak için önce şehrinizi ayarlayın:
/sehir [şehir adı]
"""
        
        keyboard = [
            [InlineKeyboardButton("🌆 Şehir Seç", callback_data='select_city')],
            [InlineKeyboardButton("📖 Yardım", callback_data='help')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def set_city_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Şehir ayarlama komutu"""
        chat_id = update.effective_chat.id
        
        if not context.args:
            await update.message.reply_text(
                "❌ Lütfen bir şehir adı girin.\n\n"
                "Kullanım: /sehir [şehir adı]\n"
                "Örnek: /sehir Istanbul"
            )
            return
        
        city_name = ' '.join(context.args)
        
        # Şehir ara
        matches = prayer_api.search_city(city_name)
        
        if not matches:
            await update.message.reply_text(
                f"❌ '{city_name}' bulunamadı.\n\n"
                "Tüm illeri görmek için: /tum\n"
                "Şehir aramak için: /ilbul [şehir]"
            )
            return
        
        if len(matches) > 1:
            # Birden fazla eşleşme varsa listele
            cities_list = "\n".join([f"• {city}" for city in matches[:5]])
            await update.message.reply_text(
                f"🔍 Birden fazla şehir bulundu:\n\n{cities_list}\n\n"
                "Lütfen tam şehir adını yazın."
            )
            return
        
        # Şehri kaydet
        selected_city = matches[0]
        db.set_city(chat_id, selected_city)
        
        # Vakitleri göster
        prayer_data = prayer_api.get_prayer_times(selected_city)
        message = f"✅ Şehir ayarlandı: **{selected_city}**\n\n"
        message += prayer_api.format_prayer_times_message(prayer_data)
        
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    
    async def prayer_times_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Namaz vakitlerini göster"""
        chat_id = update.effective_chat.id
        
        # Şehir bilgisini al
        city = db.get_city(chat_id)
        
        if not city:
            await update.message.reply_text(
                "❌ Önce şehrinizi ayarlayın.\n\n"
                "Kullanım: /sehir [şehir adı]\n"
                "Örnek: /sehir Istanbul"
            )
            return
        
        # Vakitleri al ve göster
        prayer_data = prayer_api.get_prayer_times(city)
        message = prayer_api.format_prayer_times_message(prayer_data)
        
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    
    async def next_prayer_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Sonraki namaz vaktini göster"""
        chat_id = update.effective_chat.id
        city = db.get_city(chat_id)
        
        if not city:
            await update.message.reply_text(
                "❌ Önce şehrinizi ayarlayın: /sehir [şehir adı]"
            )
            return
        
        next_prayer = prayer_api.get_next_prayer(city)
        
        if next_prayer:
            tomorrow_text = " (Yarın)" if next_prayer.get('tomorrow') else ""
            message = f"🕌 **Sonraki Namaz Vakti**\n\n"
            message += f"📍 {next_prayer['city']}\n"
            message += f"⏰ {next_prayer['name']}: **{next_prayer['time']}**{tomorrow_text}"
            
            await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
        else:
            await update.message.reply_text("❌ Sonraki namaz vakti hesaplanamadı.")
    
    async def all_cities_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Tüm illeri listele"""
        cities = prayer_api.get_all_cities_list()
        
        # İlleri 3 sütuna böl
        col_size = len(cities) // 3 + 1
        col1 = cities[:col_size]
        col2 = cities[col_size:col_size*2]
        col3 = cities[col_size*2:]
        
        message = "🇹🇷 **Türkiye'nin 81 İli**\n\n"
        
        for i in range(max(len(col1), len(col2), len(col3))):
            row = ""
            if i < len(col1):
                row += f"{col1[i]:<20}"
            if i < len(col2):
                row += f"{col2[i]:<20}"
            if i < len(col3):
                row += f"{col3[i]:<20}"
            message += f"`{row}`\n"
        
        message += "\n📝 Şehir seçmek için: /sehir [şehir adı]"
        
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    
    async def search_city_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Şehir ara"""
        if not context.args:
            await update.message.reply_text(
                "❌ Arama kelimesi girin.\n\n"
                "Kullanım: /ilbul [arama]\n"
                "Örnek: /ilbul anka"
            )
            return
        
        query = ' '.join(context.args)
        matches = prayer_api.search_city(query)
        
        if not matches:
            await update.message.reply_text(f"❌ '{query}' için sonuç bulunamadı.")
            return
        
        message = f"🔍 '{query}' için bulunan şehirler:\n\n"
        for city in matches:
            message += f"• {city}\n"
        
        message += "\n📝 Seçmek için: /sehir [şehir adı]"
        
        await update.message.reply_text(message)
    
    async def toggle_notifications_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Bildirimleri aç/kapat"""
        chat_id = update.effective_chat.id
        city = db.get_city(chat_id)
        
        if not city:
            await update.message.reply_text(
                "❌ Önce şehrinizi ayarlayın: /sehir [şehir adı]"
            )
            return
        
        enabled = db.toggle_notifications(chat_id)
        
        if enabled:
            message = "🔔 **Bildirimler Açıldı!**\n\n"
            message += f"Artık {city} için ezan vakitleri otomatik olarak bildirilecek.\n\n"
            message += "Her namaz vakti geldiğinde otomatik mesaj alacaksınız."
        else:
            message = "🔕 **Bildirimler Kapatıldı!**\n\n"
            message += "Ezan bildirimleri kapatıldı.\n\n"
            message += "Tekrar açmak için: /bildirim"
        
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    
    async def azan_info_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Ezan hakkında bilgi"""
        message = """
🕌 **Ezan Nedir?**

Ezan, Müslümanları namaza çağıran İslami bir ibadettir. Allah'ın birliğini ve Hz. Muhammed'in peygamberliğini duyuran kutsal bir çağrıdır.

📿 **Ezan Metni:**

اللّٰهُ أَكْبَر، اللّٰهُ أَكْبَر
Allahu Ekber, Allahu Ekber
(Allah en büyüktür, Allah en büyüktür)

أَشْهَدُ أَنْ لَا إِلٰهَ إِلَّا اللّٰه
Eşhedu en la ilahe illallah
(Şahitlik ederim ki, Allah'tan başka ilah yoktur)

أَشْهَدُ أَنَّ مُحَمَّدًا رَسُولُ اللّٰه
Eşhedu enne Muhammeden Resulullah
(Şahitlik ederim ki, Muhammed Allah'ın elçisidir)

حَيَّ عَلَى الصَّلَاة
Hayye ales-salah
(Haydin namaza)

حَيَّ عَلَى الْفَلَاح
Hayye alel-felah
(Haydin kurtuluşa)

اللّٰهُ أَكْبَر، اللّٰهُ أَكْبَر
Allahu Ekber, Allahu Ekber
(Allah en büyüktür, Allah en büyüktür)

لَا إِلٰهَ إِلَّا اللّٰه
La ilahe illallah
(Allah'tan başka ilah yoktur)

**🌙 Sabah Ezanı:**
Sabah ezanına "الصَّلَاةُ خَيْرٌ مِنَ النَّوْم" (Es-salatu hayrun minen-nevm - Namaz uykudan hayırlıdır) cümlesi eklenir.

📱 Bu bot ile ezan vakitlerini takip edebilir, otomatik bildirimler alabilirsiniz.
"""
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Yardım komutu"""
        help_text = """
📖 **Yardım Menüsü**

**🔹 Temel Komutlar:**

/start - Botu başlat
/sehir [şehir] - Şehir ayarla
/vakit - Namaz vakitlerini göster
/sonraki - Sonraki namaz vakti
/ezan - Ezan hakkında bilgi

**🔹 Şehir İşlemleri:**

/tum - Tüm illeri listele
/ilbul [arama] - Şehir ara
/sehir [şehir] - Şehir değiştir

**🔹 Bildirimler:**

/bildirim - Bildirimleri aç/kapat

**🔹 Örnekler:**

/sehir Istanbul
/sehir Ankara
/ilbul izma
/vakit
/sonraki

**💡 İpuçları:**

• Önce şehrinizi ayarlayın
• Bildirimleri açın
• Her namaz vaktinde otomatik bildirim alın
• Grup sohbetlerinde de kullanabilirsiniz

**🌟 Özellikler:**

✅ 81 il desteği
✅ Otomatik ezan bildirimleri
✅ Hicri takvim
✅ Sonraki namaz bildirimi
✅ Grup ve özel mesaj desteği

Herhangi bir sorunuz için: @YourSupportUsername
"""
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Mesaj işleyici"""
        text = update.message.text.lower() if update.message.text else ""
        chat_id = update.effective_chat.id
        
        # "ezan" kelimesini içeriyorsa ezan bilgisini göster
        if 'ezan' in text and len(text) < 20:
            await self.azan_info_command(update, context)
            return
        
        # Şehir ismi gibi görünüyorsa şehir ayarla
        matches = prayer_api.search_city(text)
        if matches and len(matches) == 1:
            db.set_city(chat_id, matches[0])
            prayer_data = prayer_api.get_prayer_times(matches[0])
            message = f"✅ Şehir: **{matches[0]}**\n\n"
            message += prayer_api.format_prayer_times_message(prayer_data)
            await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Buton callback işleyici"""
        query = update.callback_query
        await query.answer()
        
        if query.data == 'help':
            await self.help_command(update, context)
        elif query.data == 'select_city':
            await query.message.reply_text(
                "🌆 Şehir seçmek için:\n\n"
                "/sehir [şehir adı]\n\n"
                "Örnek:\n"
                "/sehir Istanbul\n"
                "/sehir Ankara\n"
                "/sehir Izmir\n\n"
                "Tüm illeri görmek için: /tum"
            )
    
    async def send_prayer_notification(self, chat_id, city, prayer_name, prayer_time):
        """Ezan bildirimi gönder"""
        try:
            emojis = {
                'İmsak': '🌙',
                'Öğle': '☀️',
                'İkindi': '🌤️',
                'Akşam': '🌆',
                'Yatsı': '🌃'
            }
            
            emoji = emojis.get(prayer_name, '🕌')
            
            message = f"{emoji} **{prayer_name} Vakti Girdi!**\n\n"
            message += f"📍 {city}\n"
            message += f"⏰ {prayer_time}\n\n"
            message += f"🤲 Haydi namaza!\n\n"
            message += "اَلصَّلَاةُ خَيْرٌ مِنَ النَّوْمِ"
            
            await self.app.bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Log kaydı
            db.log_prayer_notification(chat_id, prayer_name, prayer_time)
            logger.info(f"Bildirim gönderildi: {city} - {prayer_name} - Chat {chat_id}")
            
        except Exception as e:
            logger.error(f"Bildirim gönderilemedi (Chat {chat_id}): {e}")
    
    async def check_prayer_times(self):
        """Tüm kayıtlı sohbetler için namaz vakitlerini kontrol et"""
        logger.info("Namaz vakitleri kontrol ediliyor...")
        
        # Bildirimleri açık olan tüm sohbetleri al
        chats = db.get_all_subscribed_chats()
        
        current_time = datetime.now().strftime('%H:%M')
        
        for chat_id, city in chats:
            try:
                # Namaz vakitlerini al
                prayer_data = prayer_api.get_prayer_times(city)
                if not prayer_data:
                    continue
                
                timings = prayer_data.get('timings', {})
                
                # Her namaz vakti için kontrol et
                for prayer_name, prayer_time in timings.items():
                    # Güneş doğuşu haricindekiler için bildirim gönder
                    if prayer_name == 'Güneş':
                        continue
                    
                    clean_time = prayer_time.split(' ')[0] if ' ' in prayer_time else prayer_time
                    
                    # Şu anki dakika ile eşleşiyorsa bildirim gönder
                    if clean_time == current_time:
                        await self.send_prayer_notification(
                            chat_id, city, prayer_name, clean_time
                        )
                
            except Exception as e:
                logger.error(f"Chat {chat_id} için kontrol hatası: {e}")
        
        logger.info("Namaz vakitleri kontrolü tamamlandı")
    
    def setup_scheduler(self):
        """Zamanlayıcıyı ayarla - her dakika kontrol et"""
        scheduler.add_job(
            self.check_prayer_times,
            CronTrigger(second=0),  # Her dakikanın başında çalış
            id='prayer_check',
            replace_existing=True
        )
        
        logger.info("Zamanlayıcı ayarlandı - Her dakika namaz vakti kontrolü yapılacak")
    
    def run(self):
        """Botu çalıştır"""
        # Application oluştur
        self.app = Application.builder().token(self.token).build()
        
        # Komut işleyicileri ekle
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("sehir", self.set_city_command))
        self.app.add_handler(CommandHandler("vakit", self.prayer_times_command))
        self.app.add_handler(CommandHandler("sonraki", self.next_prayer_command))
        self.app.add_handler(CommandHandler("tum", self.all_cities_command))
        self.app.add_handler(CommandHandler("ilbul", self.search_city_command))
        self.app.add_handler(CommandHandler("bildirim", self.toggle_notifications_command))
        self.app.add_handler(CommandHandler("ezan", self.azan_info_command))
        self.app.add_handler(CommandHandler("yardim", self.help_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        
        # Mesaj ve callback işleyicileri
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.app.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Zamanlayıcıyı başlat
        self.setup_scheduler()
        scheduler.start()
        
        logger.info("Bot başlatılıyor...")
        
        # Botu çalıştır
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    if not config.BOT_TOKEN or config.BOT_TOKEN == "BURAYA_BOT_TOKEN_GİRİN":
        print("❌ HATA: Bot token'ı ayarlanmamış!")
        print("config.py dosyasındaki BOT_TOKEN değerini BotFather'dan aldığınız token ile değiştirin.")
    else:
        bot = EzanBot(config.BOT_TOKEN)
        bot.run()
