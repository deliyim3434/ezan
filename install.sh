#!/bin/bash

echo "🕌 Ezan Vakitleri Telegram Bot - Kurulum"
echo "========================================="
echo ""

# Python kontrolü
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 bulunamadı. Lütfen Python 3.8 veya üzeri yükleyin."
    exit 1
fi

echo "✅ Python bulundu: $(python3 --version)"
echo ""

# Bağımlılıkları yükle
echo "📦 Bağımlılıklar yükleniyor..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Bağımlılıklar yüklenemedi!"
    exit 1
fi

echo ""
echo "✅ Bağımlılıklar başarıyla yüklendi!"
echo ""

# Config kontrolü
if [ ! -f "config.py" ]; then
    echo "⚠️  config.py dosyası bulunamadı!"
    echo ""
    echo "Lütfen şu adımları takip edin:"
    echo "1. config_example.py dosyasını config.py olarak kopyalayın"
    echo "2. config.py dosyasındaki BOT_TOKEN değerini BotFather'dan aldığınız token ile değiştirin"
    echo ""
    echo "Komut: cp config_example.py config.py"
    echo "Ardından: nano config.py"
    echo ""
    exit 1
fi

echo "✅ Kurulum tamamlandı!"
echo ""
echo "🚀 Botu başlatmak için:"
echo "   python3 main.py"
echo ""
echo "📖 Detaylı bilgi için README.md dosyasını okuyun"
echo ""
