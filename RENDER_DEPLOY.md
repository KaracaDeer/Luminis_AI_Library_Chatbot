# 🚀 Render Deploy Guide

Bu rehber Luminis AI Library Chatbot'u Render.com'da deploy etmek için hazırlanmıştır.

## 📋 Ön Gereksinimler

1. **Render.com hesabı** (ücretsiz)
2. **GitHub repository** bağlantısı
3. **OpenAI API Key** (ücretli)

## 🔧 Deploy Adımları

### 1️⃣ Backend Deploy (Web Service)

1. **Render Dashboard'a git:** https://dashboard.render.com
2. **"New +"** → **"Web Service"** seç
3. **GitHub repository'ni bağla:** `KaracaDeer/Luminis_AI_Library_Chatbot`

**Temel Ayarlar:**
- **Name:** `luminis-backend`
- **Environment:** `Python 3`
- **Region:** `Oregon (US West)`
- **Branch:** `main`
- **Root Directory:** `src/backend`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python render_start.py`

**Environment Variables:**
```
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///luminis_library.db
ENVIRONMENT=production
CORS_ORIGINS=https://luminis-frontend.onrender.com
```

### 2️⃣ Frontend Deploy (Static Site)

1. **"New +"** → **"Static Site"** seç
2. **Aynı repository'yi seç**

**Temel Ayarlar:**
- **Name:** `luminis-frontend`
- **Build Command:** `cd src/frontend && npm install && npm run build`
- **Publish Directory:** `src/frontend/dist`
- **Branch:** `main`

**Environment Variables:**
```
VITE_API_URL=https://luminis-backend.onrender.com
VITE_APP_NAME=Luminis AI Library
VITE_APP_VERSION=1.0.2
VITE_ENVIRONMENT=production
```

## 🔄 Otomatik Deploy

**render.yaml** dosyası ile otomatik deploy:

1. **"New +"** → **"Blueprint"** seç
2. **Repository'ni seç**
3. **render.yaml** otomatik olarak tanınacak
4. **Deploy** butonuna tıkla

## 📊 Deploy Sonrası

### Backend URL:
```
https://luminis-backend.onrender.com
```

### Frontend URL:
```
https://luminis-frontend.onrender.com
```

### Health Check:
```
https://luminis-backend.onrender.com/api/health
```

## 🐛 Troubleshooting

### Backend Sorunları:
- **Build Error:** `requirements.txt` kontrol et
- **Start Error:** `render_start.py` çalışıyor mu?
- **API Error:** Environment variables doğru mu?

### Frontend Sorunları:
- **Build Error:** `package.json` ve `npm install` kontrol et
- **API Connection:** `VITE_API_URL` doğru mu?
- **CORS Error:** Backend'de `CORS_ORIGINS` ayarla

### Free Tier Limitleri:
- **Sleep Mode:** 15 dakika inaktivite sonrası uyku
- **Build Time:** 90 saniye limit
- **Memory:** 512MB limit
- **Bandwidth:** 100GB/ay

## 🔧 Environment Variables

### Backend (.env):
```bash
OPENAI_API_KEY=sk-...
DATABASE_URL=sqlite:///luminis_library.db
ENVIRONMENT=production
CORS_ORIGINS=https://luminis-frontend.onrender.com
```

### Frontend (Vite):
```bash
VITE_API_URL=https://luminis-backend.onrender.com
VITE_APP_NAME=Luminis AI Library
VITE_APP_VERSION=1.0.2
VITE_ENVIRONMENT=production
```

## 📈 Monitoring

Render Dashboard'da:
- **Logs:** Real-time log görüntüleme
- **Metrics:** CPU, Memory, Response time
- **Deployments:** Deploy geçmişi
- **Environment:** Environment variables

## 🚀 Production Tips

1. **Database:** SQLite yerine PostgreSQL kullan (ücretli)
2. **CDN:** Static assets için CDN ekle
3. **Monitoring:** Uptime monitoring ekle
4. **Backup:** Database backup stratejisi
5. **SSL:** HTTPS otomatik aktif

---

**🎉 Deploy tamamlandıktan sonra uygulamanız canlı olacak!**
