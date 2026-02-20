import sqlite3
from datetime import datetime
import config

class Database:
    def __init__(self, db_name=config.DATABASE_NAME):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        """Veritabanı bağlantısı oluştur"""
        return sqlite3.connect(self.db_name)
    
    def init_database(self):
        """Veritabanını başlat ve tabloları oluştur"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Gruplar tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                chat_id INTEGER PRIMARY KEY,
                chat_title TEXT,
                city TEXT,
                notifications_enabled INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Kullanıcılar tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                city TEXT,
                notifications_enabled INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Ezan geçmişi tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prayer_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                prayer_name TEXT,
                prayer_time TEXT,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_group(self, chat_id, chat_title, city=None):
        """Grup ekle veya güncelle"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO groups (chat_id, chat_title, city, last_updated)
            VALUES (?, ?, ?, ?)
        ''', (chat_id, chat_title, city, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def add_user(self, user_id, username, first_name, city=None):
        """Kullanıcı ekle veya güncelle"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO users (user_id, username, first_name, city)
            VALUES (?, ?, ?, ?)
        ''', (user_id, username, first_name, city))
        
        conn.commit()
        conn.close()
    
    def set_city(self, chat_id, city):
        """Grup veya kullanıcı için şehir ayarla"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Önce grup tablosunda dene
        cursor.execute('''
            UPDATE groups SET city = ?, last_updated = ? WHERE chat_id = ?
        ''', (city, datetime.now(), chat_id))
        
        if cursor.rowcount == 0:
            # Grup bulunamazsa kullanıcı tablosunda dene
            cursor.execute('''
                UPDATE users SET city = ? WHERE user_id = ?
            ''', (city, chat_id))
        
        conn.commit()
        conn.close()
    
    def get_city(self, chat_id):
        """Grup veya kullanıcının şehrini al"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Önce grup tablosunda ara
        cursor.execute('SELECT city FROM groups WHERE chat_id = ?', (chat_id,))
        result = cursor.fetchone()
        
        if result is None:
            # Grup bulunamazsa kullanıcı tablosunda ara
            cursor.execute('SELECT city FROM users WHERE user_id = ?', (chat_id,))
            result = cursor.fetchone()
        
        conn.close()
        return result[0] if result and result[0] else None
    
    def get_all_subscribed_chats(self):
        """Bildirimleri açık olan tüm sohbetleri al"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        chats = []
        
        # Grupları al
        cursor.execute('''
            SELECT chat_id, city FROM groups 
            WHERE notifications_enabled = 1 AND city IS NOT NULL
        ''')
        chats.extend(cursor.fetchall())
        
        # Kullanıcıları al
        cursor.execute('''
            SELECT user_id, city FROM users 
            WHERE notifications_enabled = 1 AND city IS NOT NULL
        ''')
        chats.extend(cursor.fetchall())
        
        conn.close()
        return chats
    
    def toggle_notifications(self, chat_id):
        """Bildirimleri aç/kapat"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Önce grup tablosunda dene
        cursor.execute('''
            UPDATE groups 
            SET notifications_enabled = 1 - notifications_enabled 
            WHERE chat_id = ?
        ''', (chat_id,))
        
        if cursor.rowcount == 0:
            # Grup bulunamazsa kullanıcı tablosunda dene
            cursor.execute('''
                UPDATE users 
                SET notifications_enabled = 1 - notifications_enabled 
                WHERE user_id = ?
            ''', (chat_id,))
        
        conn.commit()
        
        # Yeni durumu al
        cursor.execute('SELECT notifications_enabled FROM groups WHERE chat_id = ?', (chat_id,))
        result = cursor.fetchone()
        
        if result is None:
            cursor.execute('SELECT notifications_enabled FROM users WHERE user_id = ?', (chat_id,))
            result = cursor.fetchone()
        
        conn.close()
        return bool(result[0]) if result else False
    
    def log_prayer_notification(self, chat_id, prayer_name, prayer_time):
        """Gönderilen ezan bildirimini kaydet"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO prayer_history (chat_id, prayer_name, prayer_time)
            VALUES (?, ?, ?)
        ''', (chat_id, prayer_name, prayer_time))
        
        conn.commit()
        conn.close()
    
    def get_statistics(self):
        """İstatistikleri al"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM groups')
        total_groups = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM groups WHERE notifications_enabled = 1')
        active_groups = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM prayer_history')
        total_notifications = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_groups': total_groups,
            'total_users': total_users,
            'active_groups': active_groups,
            'total_notifications': total_notifications
        }
