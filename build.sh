#!/usr/bin/env bash
# ==============================================================================
# MockLeap — Render.com Build Script
# Render Web Service: Build Command -> ./build.sh
# ==============================================================================

# Exit immediately if a command exits with a non-zero status
set -o errexit

echo "🚀 [1/4] Python paketlari o'rnatilmoqda (requirements.txt)..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🎨 [2/4] Tailwind CSS tekshirilmoqda..."
if command -v npm &> /dev/null; then
    npm install --production=false
    npm run build:css || true
fi

echo "📦 [3/4] Statik fayllar yig'ilmoqda (collectstatic)..."
python manage.py collectstatic --noinput

echo "🗄️ [4/4] Ma'lumotlar bazasi migratsiyalari bajarilmoqda..."
python manage.py migrate --noinput

echo "🌱 Test ma'lumotlari tekshirilmoqda..."
python manage.py seed_data || true
python manage.py seed_cambridge9_test4 || true

echo "=============================================================================="
echo "✅ MockLeap Render.com uchun muvaffaqiyatli qurildi (Build OK)!"
echo "=============================================================================="
