import requests
from datetime import datetime
import config
import logging

logger = logging.getLogger(__name__)

class PrayerTimes:
    def __init__(self):
        self.api_url = config.PRAYER_TIMES_API
        self.backup_api = config.BACKUP_API
    
    def get_prayer_times(self, city_name):
        """
        Belirli bir şehir için namaz vakitlerini al
        
        Args:
            city_name: Şehir adı (Türkçe karakterler desteklenir)
        
        Returns:
            dict: Namaz vakitleri bilgisi veya None
        """
        # Şehir adını normalize et
        city_key = city_name.lower().replace('ı', 'i').replace('ş', 's').replace('ğ', 'g').replace('ü', 'u').replace('ö', 'o').replace('ç', 'c')
        
        # Config'den şehir bilgisini al
        city_info = None
        for key, info in config.TURKISH_CITIES.items():
            if key.startswith(city_key[:3]) or city_key.startswith(key[:3]):
                city_info = info
                break
        
        if not city_info:
            return None
        
        try:
            # Aladhan API'yi kullan
            params = {
                'city': city_info['name'],
                'country': city_info['country'],
                'method': 13  # Diyanet İşleri Başkanlığı metodu
            }
            
            response = requests.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('code') == 200 and 'data' in data:
                timings = data['data']['timings']
                date_info = data['data']['date']
                
                # Vakitleri formatla
                prayer_times = {
                    'city': city_info['name'],
                    'date': date_info['readable'],
                    'hijri': date_info['hijri']['date'],
                    'timings': {
                        'İmsak': timings.get('Fajr', timings.get('Imsak', 'N/A')),
                        'Güneş': timings.get('Sunrise', 'N/A'),
                        'Öğle': timings.get('Dhuhr', 'N/A'),
                        'İkindi': timings.get('Asr', 'N/A'),
                        'Akşam': timings.get('Maghrib', 'N/A'),
                        'Yatsı': timings.get('Isha', 'N/A')
                    }
                }
                
                return prayer_times
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API hatası: {e}")
            # Backup API'yi dene
            return self._get_from_backup_api(city_info['name'])
        
        return None
    
    def _get_from_backup_api(self, city_name):
        """Yedek API'den namaz vakitlerini al"""
        try:
            url = f"{self.backup_api}/{city_name}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data:
                return {
                    'city': city_name,
                    'date': datetime.now().strftime('%d %B %Y'),
                    'hijri': data.get('MiladiTarihKisa', ''),
                    'timings': {
                        'İmsak': data.get('Imsak', 'N/A'),
                        'Güneş': data.get('Gunes', 'N/A'),
                        'Öğle': data.get('Ogle', 'N/A'),
                        'İkindi': data.get('Ikindi', 'N/A'),
                        'Akşam': data.get('Aksam', 'N/A'),
                        'Yatsı': data.get('Yatsi', 'N/A')
                    }
                }
        except Exception as e:
            logger.error(f"Backup API hatası: {e}")
        
        return None
    
    def format_prayer_times_message(self, prayer_data):
        """Namaz vakitlerini mesaj formatında düzenle"""
        if not prayer_data:
            return "❌ Namaz vakitleri alınamadı."
        
        city = prayer_data.get('city', 'Bilinmeyen')
        date = prayer_data.get('date', '')
        hijri = prayer_data.get('hijri', '')
        timings = prayer_data.get('timings', {})
        
        message = f"🕌 **{city} - Namaz Vakitleri**\n\n"
        message += f"📅 {date}\n"
        if hijri:
            message += f"🌙 Hicri: {hijri}\n"
        message += "\n"
        
        # Emoji'ler
        emojis = {
            'İmsak': '🌙',
            'Güneş': '🌅',
            'Öğle': '☀️',
            'İkindi': '🌤️',
            'Akşam': '🌆',
            'Yatsı': '🌃'
        }
        
        for prayer_name, prayer_time in timings.items():
            emoji = emojis.get(prayer_name, '🕌')
            # Saat bilgisini temizle (timezone bilgisini kaldır)
            clean_time = prayer_time.split(' ')[0] if ' ' in prayer_time else prayer_time
            message += f"{emoji} **{prayer_name}:** {clean_time}\n"
        
        return message
    
    def get_next_prayer(self, city_name):
        """Sonraki namaz vaktini al"""
        prayer_data = self.get_prayer_times(city_name)
        if not prayer_data:
            return None
        
        current_time = datetime.now().strftime('%H:%M')
        timings = prayer_data.get('timings', {})
        
        # Namaz sırasına göre kontrol et
        prayer_order = ['İmsak', 'Güneş', 'Öğle', 'İkindi', 'Akşam', 'Yatsı']
        
        for prayer in prayer_order:
            prayer_time = timings.get(prayer, '').split(' ')[0]
            if prayer_time > current_time:
                return {
                    'name': prayer,
                    'time': prayer_time,
                    'city': prayer_data['city']
                }
        
        # Eğer bugünün tüm namazları geçtiyse, yarının ilk namazını dön
        return {
            'name': 'İmsak',
            'time': timings.get('İmsak', '').split(' ')[0],
            'city': prayer_data['city'],
            'tomorrow': True
        }
    
    def get_all_cities_list(self):
        """Tüm şehirlerin listesini al"""
        cities = []
        for city_info in config.TURKISH_CITIES.values():
            cities.append(city_info['name'])
        return sorted(cities)
    
    def search_city(self, query):
        """Şehir ara (fuzzy search)"""
        query = query.lower().replace('ı', 'i').replace('ş', 's').replace('ğ', 'g').replace('ü', 'u').replace('ö', 'o').replace('ç', 'c')
        
        matches = []
        for key, city_info in config.TURKISH_CITIES.items():
            if query in key or key in query:
                matches.append(city_info['name'])
        
        return matches
