# MockLeap

IELTS mock test platformasi — Listening, Reading, Writing, Speaking bo'limlari bilan.

## Talablar

- Python 3.11+
- Node.js 18+ (faqat CSS build uchun)

## O'rnatish

### 1. Loyihani klonlash yoki nusxalash

```bash
cd /path/to/projects
# loyiha papkasini shu yerga qo'ying
cd mockleap
```

### 2. Virtual muhit yaratish va faollashtirish

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Paketlarni o'rnatish

```bash
pip install -r requirements.txt
```

### 4. .env faylini sozlash

```bash
cp .env.example .env
```

`.env` faylini oching va `SECRET_KEY` ni o'zgartiring:

```
DEBUG=True
SECRET_KEY=o'zingizning-maxfiy-kalitingiz
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### 5. Ma'lumotlar bazasini yaratish

```bash
python manage.py migrate
```

### 6. Admin foydalanuvchi yaratish

```bash
python manage.py createsuperuser
```

### 7. (Ixtiyoriy) Test ma'lumotlarini yuklash

```bash
python manage.py seed_data
```

### 8. Serverni ishga tushirish

```bash
python manage.py runserver
```

Brauzerda oching: [http://127.0.0.1:8000](http://127.0.0.1:8000)

Admin panel: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

## CSS ni qayta build qilish (ixtiyoriy)

Agar `static/css/main.css` mavjud bo'lsa, bu qadam shart emas.
Agar style'larni o'zgartirmoqchi bo'lsangiz:

```bash
npm install
npm run build   # yoki: npx tailwindcss -i static/css/input.css -o static/css/main.css
```

---

## Loyiha tuzilmasi

```
mockleap/
├── apps/
│   ├── accounts/       # Foydalanuvchi profili
│   ├── analytics/      # Faollik statistikasi
│   ├── community/      # Forum / xabarlar
│   ├── core/           # Umumiy sahifalar, templatetags
│   ├── dashboard/      # Bosh sahifa (dashboard)
│   ├── listening/      # Listening test
│   ├── notifications/  # Bildirishnomalar
│   ├── rankings/       # Reyting jadvali
│   ├── reading/        # Reading test
│   ├── speaking/       # Speaking test
│   ├── teachers/       # O'qituvchi panel
│   └── writing/        # Writing test
├── config/             # Django sozlamalari
├── static/             # CSS, JS
├── templates/          # HTML shablonlar
├── .env.example        # .env namunasi
├── manage.py
└── requirements.txt
```

---

## Production uchun

1. `.env` da `DEBUG=False` qiling
2. `SECRET_KEY` ni xavfsiz, tasodifiy kalit bilan almashtiring
3. `ALLOWED_HOSTS` ga serveringiz domenini qo'shing
4. `python manage.py collectstatic` buyrug'ini ishga tushiring
5. PostgreSQL uchun `DATABASE_URL=postgres://user:pass@host/dbname` formatida yozing
