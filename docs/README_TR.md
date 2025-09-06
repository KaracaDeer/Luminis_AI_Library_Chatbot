# Luminis.AI - Kütüphane Asistanı

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/React-18.0+-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-blue.svg)](https://github.com/features/actions)

> **AI destekli kütüphane asistanı** - OpenAI GPT-4 ve LangChain ile güçlendirilmiş akıllı kitap önerileri, sesli etkileşimler ve semantik arama.

[🇺🇸 English README](README.md)

## 🚀 Canlı Demo

https://luminis-frontend.onrender.com

## 🎯 Demo

![Luminis.AI Demo](docs/demo.gif)


## ✨ Özellikler

- 🤖 **AI Destekli Öneriler** - OpenAI GPT-4 kullanarak kişiselleştirilmiş kitap önerileri
- 🎤 **Sesli Etkileşim** - Whisper entegrasyonu ile doğal sesli iletişim
- 🔍 **Semantik Arama** - ChromaDB vektör arama ile akıllı kitap keşfi
- 🌍 **Çok Dilli Destek** - Türkçe ve İngilizce dil desteği
- 📱 **Responsive Tasarım** - Tüm cihazlarda çalışan modern, minimalist arayüz
- 🚀 **Gerçek Zamanlı Sohbet** - Akış özellikli anlık AI yanıtları
- 📚 **RAG Sistemi** - Doğru bilgi için Retrieval-Augmented Generation
- 🔐 **Kullanıcı Kimlik Doğrulama** - Güvenli kullanıcı yönetimi ve sohbet geçmişi
- 🔑 **JWT Kimlik Doğrulama** - Güvenli token tabanlı kimlik doğrulama sistemi
- 🌐 **OAuth 2.0 Entegrasyonu** - Google, GitHub ve Microsoft ile sosyal giriş
- 📚 **Open Library Entegrasyonu** - Open Library API'den milyonlarca kitaba erişim
- 🔄 **Dinamik Kitap Veritabanı** - Gerçek zamanlı kitap veri senkronizasyonu
- 🎯 **Gelişmiş Tür Eşleştirme** - Kitap türü ve ruh haline göre akıllı kategorilendirme

## 🏗️ Teknoloji Stack

### Frontend
- **React 18** + **TypeScript** - Modern UI framework
- **Vite** - Yıldırım hızında build tool
- **TailwindCSS** - Utility-first CSS framework
- **Framer Motion** - Production-ready motion library
- **GSAP** - Profesyonel seviye animasyonlar
- **Zustand** - Kalıcılık ile hafif state management
- **React Router** - Declarative routing
- **Kimlik Doğrulama Bileşenleri** - Giriş/Kayıt modalları ve OAuth entegrasyonu

### Backend
- **FastAPI** - Yüksek performanslı Python web framework
- **SQLAlchemy** - SQL toolkit ve ORM
- **ChromaDB** - AI-native vektör veritabanı
- **LangChain** - LLM uygulama framework'ü
- **OpenAI Entegrasyonu** - GPT-4, Whisper ve Embeddings
- **JWT & OAuth2** - Kimlik doğrulama ve yetkilendirme servisleri

### AI & ML
- **RAG Pipeline** - Retrieval-Augmented Generation
- **Vektör Embeddings** - Semantik benzerlik arama
- **Doğal Dil İşleme** - Gelişmiş metin anlama
- **Ses Tanıma** - Konuşma-metin dönüşümü

## 🚀 Hızlı Başlangıç

### Gereksinimler
- **Node.js** 18+
- **Python** 3.11+
- **OpenAI API Key** gerçek AI için

### Kurulum

1. **Repository'yi klonlayın**
   ```bash
   git clone https://github.com/KaracaDeer/Luminis_AI_Library_Chatbot.git
   cd Luminis_AI_Library_Chatbot
   ```

2. **Bağımlılıkları yükleyin**
   ```bash
   # Node.js bağımlılıkları
   npm install

   # Python bağımlılıkları
   pip install -r requirements.txt
   ```

3. **Ortam değişkenlerini yapılandırın**
   ```bash
   cp env.example .env
   # .env dosyasını OpenAI API key ile düzenleyin
   ```

### Çalıştır & Test & Deploy

4. **Uygulamayı başlatın**
    ```bash
    # Her iki sunucuyu da başlatın
    npm run dev

         # Veya ayrı ayrı:
     npm run server    # Backend (port 8000)
     npm run client    # Frontend (port 5173)
    ```

5. **Uygulamaya erişin**
   - **Frontend (dev)**: http://localhost:5173
   - **Backend (dev)**: http://127.0.0.1:8000
   - **API Dokümantasyonu (dev)**: http://127.0.0.1:8000/docs

6. **Hızlı komutlar**
   ```bash
   # Test
   npm test                    # Tüm testleri çalıştır
   npm run test:python        # Backend testleri
   npm run test:backend       # Backend servis testleri
   npm run test:integration   # Entegrasyon testleri
   npm run test:build         # Build testi

   # Veritabanı
   npm run db:init            # Veritabanını başlat
   npm run db:reset           # Veritabanını sıfırla
   npm run db:test            # Veritabanı bağlantısını test et

   # Geliştirme
   npm run build              # Frontend build
   npm run start              # Üretim sunucusunu başlat
   npm run install-deps       # Tüm bağımlılıkları yükle

   # Docker
   docker-compose up -d
   ```

### Postman API Testi

1. **Postman koleksiyonu ve environment'ı içe aktarın:**
   - Koleksiyon: `docs/Luminis_AI_Library_API.postman_collection.json`
   - Environment: `docs/Luminis_AI_Library_API.postman_environment.json`

2. **Environment değişkenlerini yapılandırın:**
   - `base_url` değerini API endpoint'inize ayarlayın:
     - Lokal geliştirme: `http://localhost:8000`
     - Docker: `http://localhost:8000`
     - Üretim: `https://your-domain.com`

3. **API endpoint'lerini test edin:**
   - Sağlık kontrolü: `GET {{base_url}}/api/health`
   - AI ile sohbet: `POST {{base_url}}/api/chat`
   - Kitapları listele: `GET {{base_url}}/api/books`
   - Kimlik doğrulama: `POST {{base_url}}/api/auth/login`

4. **Mevcut koleksiyonlar:**
   - **Health & Status** - API sağlık kontrolleri
   - **Authentication** - Kullanıcı kayıt, giriş, OAuth
   - **Chat & AI** - AI sohbet ve ses dönüştürme
   - **Books** - Kitap tarama ve öneriler
   - **Open Library Integration** - Harici kitap veritabanı
   - **RAG** - Gelişmiş AI özellikleri
   - **Vector Search** - Semantik arama işlevselliği

### Docker (Üretim Hazır)
```bash
# Tüm servisleri başlat
docker-compose up -d

# Veya script'leri kullan
./docker-scripts.sh start          # Linux/Mac
docker-scripts.bat start           # Windows

# Log'ları görüntüle
docker-compose logs -f

# Servisleri durdur
docker-compose down
```

**Docker Özellikleri:**
- **Multi-stage builds** - Optimize edilmiş imajlar
- **Health checks** - Servis izleme
- **Volume persistence** - Veritabanı ve ChromaDB kalıcılığı
- **Nginx reverse proxy** - Güvenlik başlıkları ile
- **Redis caching** - Gelişmiş performans

## 📖 Kullanım

### Temel Sohbet
1. Sohbet arayüzüne gidin
2. Kitaplar, yazarlar veya türler hakkında sorunuzu yazın
3. AI destekli öneriler ve içgörüler alın

### Sesli Etkileşim
1. Mikrofon butonuna tıklayın
2. Sorunuzu doğal bir şekilde söyleyin
3. Anlık ses-metin dönüşümü ve AI yanıtları alın

### Kitap Keşfi
1. Kitapları bulmak için semantik arama kullanın
2. Tercihlerinize göre önerileri keşfedin
3. Benzer başlıkları ve yazarları keşfedin

### Open Library Entegrasyonu
1. **Milyonlarca Kitaba Erişim**
   - Open Library API'den gerçek zamanlı kitap arama
   - Güncel kitap bilgileri ve yayın tarihleri
   - Çok dilli kitap desteği

2. **Akıllı Tür Kategorilendirme**
   - 28 farklı kitap türü
   - Ruh haline göre kitap önerileri
   - Otomatik tür eşleştirme

3. **Dinamik Veritabanı Senkronizasyonu**
   - Yeni kitapları otomatik ekleme
   - Kitap detaylarını güncelleme
   - Açıklama ve puan bilgileri

### Kimlik Doğrulama ve Kullanıcı Yönetimi
1. **Yerel Kayıt/Giriş**
   - Kullanıcı adı, e-posta ve şifre ile hesap oluşturun
   - Bcrypt ile güvenli şifre hashleme
   - JWT token tabanlı kimlik doğrulama

2. **OAuth 2.0 Sosyal Giriş**
   - Google, GitHub ve Microsoft entegrasyonu
   - Durum doğrulaması ile güvenli OAuth akışı
   - OAuth kullanıcıları için otomatik hesap oluşturma

3. **Kullanıcı Profil Yönetimi**
   - Profil bilgilerini görüntüleyin ve güncelleyin
   - Giriş geçmişini ve kimlik doğrulama sağlayıcısını takip edin
   - Güvenli token yenileme mekanizması

## 🔧 Yapılandırma

### Ortam Değişkenleri
```bash
# OpenAI Yapılandırması
OPENAI_API_KEY=your_openai_api_key_here

# Sunucu Yapılandırması
PORT=8000
HOST=127.0.0.1

# Geliştirme
NODE_ENV=development
VITE_API_URL=http://localhost:8000

# JWT Kimlik Doğrulama
JWT_SECRET_KEY=your_jwt_secret_key_here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# OAuth 2.0 Yapılandırması
OAUTH2_CLIENT_ID=your_oauth2_client_id
OAUTH2_CLIENT_SECRET=your_oauth2_client_secret
OAUTH2_REDIRECT_URI=http://localhost:5173/auth/callback

# İsteğe bağlı: Sağlayıcıya özel OAuth kimlik bilgileri
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
MICROSOFT_CLIENT_ID=your_microsoft_client_id
MICROSOFT_CLIENT_SECRET=your_microsoft_client_secret
```

### Veritabanı Kurulumu
Uygulama geliştirme için varsayılan olarak SQLite kullanır. Üretim için, ortam değişkenlerinde tercih ettiğiniz veritabanını yapılandırın.

### API Endpoints

#### Kimlik Doğrulama Endpoints
- `POST /api/auth/register` - Kullanıcı kaydı
- `POST /api/auth/login` - Kullanıcı girişi
- `POST /api/auth/refresh` - Access token yenileme
- `GET /api/auth/profile` - Kullanıcı profili alma
- `PUT /api/auth/profile` - Kullanıcı profili güncelleme
- `POST /api/auth/logout` - Kullanıcı çıkışı

#### OAuth 2.0 Endpoints
- `GET /api/auth/oauth/{provider}/url` - OAuth yetkilendirme URL'si alma
- `GET /api/auth/oauth/{provider}/callback` - OAuth callback işleme

#### Sohbet ve Kütüphane Endpoints
- `POST /api/chat` - Sohbet mesajı gönderme
- `GET /api/books` - Kitap önerileri alma
- `GET /api/search` - Kitapları semantik olarak arama

#### Open Library API Endpoints
- `GET /api/openlibrary/search` - Open Library'de kitap arama
- `GET /api/openlibrary/popular` - Popüler kitapları getirme
- `POST /api/openlibrary/sync` - Kitapları yerel veritabanına senkronize etme
- `GET /api/openlibrary/health` - Open Library API sağlık kontrolü
- `GET /api/openlibrary/genres` - Mevcut türleri listeleme

## 📁 Proje Yapısı

```
Luminis_AI_Library_Chatbot/
├── .github/                     # GitHub Actions ve templates
│   └── workflows/               # CI/CD YAML dosyaları
│
├── docs/                        # Proje dokümantasyonu
│   ├── README.md                # Ana README (İngilizce)
│   ├── README_TR.md             # Türkçe README
│   ├── CHANGELOG.md             # Değişiklik kayıtları
│   ├── CODE_OF_CONDUCT.md       # Davranış kuralları
│   └── CONTRIBUTING.md          # Katkı rehberi
│
├── src/                         # Kaynak kod
│   ├── backend/                 # Backend (FastAPI)
│   │   ├── main_minimal.py      # Ana minimal API
│   │   ├── main.py              # Tam özellikli API
│   │   └── enhanced_responses.py # Gelişmiş yanıtlar
│   │
│   ├── frontend/                # Frontend (React + Vite)
│   │   ├── components/          # React bileşenleri
│   │   │   ├── AuthModal.tsx    # Kimlik doğrulama modalı
│   │   │   └── OAuthCallback.tsx # OAuth callback işleyicisi
│   │   ├── stores/              # Zustand state yönetimi
│   │   │   └── authStore.ts     # Kimlik doğrulama state store'u
│   │   ├── services/            # API servisleri
│   │   ├── hooks/               # Özel React hooks
│   │   ├── contexts/            # React context'leri
│   │   └── assets/              # Statik dosyalar
│   │
│   ├── database/                # Veritabanı yönetimi
│   │   ├── database.py          # Veritabanı bağlantısı
│   │   └── init_database.py     # Veritabanı başlatma
│   │
│   └── services/                # Paylaşılan servisler
│       ├── auth_service.py      # JWT & OAuth2 kimlik doğrulama
│       ├── openlibrary_service.py # Open Library API entegrasyonu
│       ├── rag_service.py       # RAG implementasyonu
│       └── vector_service.py    # Vektör arama servisi
│
├── tests/                       # Test dosyaları
│   ├── test_backend.py          # Backend testleri
│   ├── test_frontend.py         # Frontend testleri
│   └── test_integration.py      # Entegrasyon testleri
│
├── scripts/                     # Yardımcı scriptler
│   ├── create_real_audio.py     # Audio oluşturma
│   └── debug_audio.py           # Audio debug
│
├── docker/                      # Docker dosyaları
│
├── .gitignore                   # Git ignore dosyası
├── requirements.txt             # Python bağımlılıkları
├── package.json                 # Node.js bağımlılıkları
├── pyproject.toml               # Python paketleme dosyası
├── setup.cfg                    # Python setup konfigürasyonu
├── README.md                    # Projenin genel açıklaması
├── LICENSE                      # Lisans dosyası
├── CONTRIBUTING.md              # Katkıda bulunma rehberi
└── Makefile                     # Build/test/run komutları
```

*Bu yapı endüstri standartlarına uygun olarak düzenlenmiştir. Detaylı bilgi için [CONTRIBUTING.md](CONTRIBUTING.md) sayfasına bakın.*

## 🔒 Güvenlik Özellikleri

### Kimlik Doğrulama ve Yetkilendirme
- **JWT Token'ları**: Güvenli access ve refresh token sistemi
- **Şifre Güvenliği**: Salt rounds ile Bcrypt hashleme
- **OAuth 2.0**: Endüstri standardı sosyal kimlik doğrulama
- **Token Yenileme**: Kesintisiz UX için otomatik token yenileme
- **Oturum Yönetimi**: Güvenli kullanıcı oturum işleme

### Veri Koruması
- **HTTPS Hazır**: Güvenli iletişim protokolleri
- **Girdi Doğrulama**: Kapsamlı istek doğrulama
- **SQL Injection Koruması**: SQLAlchemy ORM güvenliği
- **CORS Yapılandırması**: Cross-origin resource sharing kontrolü

## 🤝 Katkıda Bulunma & Destek

### Katkıda Bulunma
1. **Repository'yi fork edin**
2. **Feature branch oluşturun**: `git checkout -b feature/harika-ozellik`
3. **Değişikliklerinizi yapın**
4. **Pull request gönderin**

**Detaylı rehber için [CONTRIBUTING.md](CONTRIBUTING.md) sayfasına bakın**

### Destek
- **Issues**: [GitHub Issues](https://github.com/KaracaDeer/Luminis_AI_Library_Chatbot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/KaracaDeer/Luminis_AI_Library_Chatbot/discussions)
- **LinkedIn**: [Profil](https://www.linkedin.com/in/fatma-karaca-erdogan-32201a378)
- **Email**: fatmakaracaerdogan@gmail.com

## 📝 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır - detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🙏 Teşekkürler

- **OpenAI** - En son AI modellerini sağladığı için
- **LangChain** - RAG framework'ü için
- **FastAPI** - Yüksek performanslı backend framework için
- **React Ekibi** - Harika frontend library için
