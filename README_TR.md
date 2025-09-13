# Luminis.AI - Akıllı Kütüphane Asistanı

[![Versiyon](https://img.shields.io/badge/versiyon-1.0.2-blue.svg)](https://github.com/KaracaDeer/Luminis_AI_Library_Chatbot)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![Node.js](https://img.shields.io/badge/node.js-18+-green.svg)](https://nodejs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3+-blue.svg)](https://www.typescriptlang.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)](https://openai.com/)
[![Lisans](https://img.shields.io/badge/lisans-MIT-green.svg)](LICENSE)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Fatma%20Karaca%20Erdogan-blue.svg)](https://www.linkedin.com/in/fatma-karaca-erdogan-32201a378/)

> **AI destekli kütüphane asistanı** - OpenAI GPT-4 ve LangChain ile desteklenen akıllı kitap önerileri, sesli etkileşimler ve anlamsal arama.

[🇬🇧 English README](README.md)

## 🎯 TL;DR

**Luminis.AI, kullanıcıların saniye altı yanıt süreleriyle akıllı AI konuşmaları yoluyla mükemmel kitapları keşfetmelerini sağlar.** Modern full-stack mimarisi ile inşa edilmiş olup, GPT-4, ChromaDB vektör arama ve ses tanıma özelliklerini birleştirerek çok dilli destekle kişiselleştirilmiş, doğru kitap önerileri sunar.

🇬🇧 [English README](README.md)

## 🎯 Demo

![Luminis.AI Demo](docs/demo.gif)

## 🚀 Hızlı Başlangıç

```bash
# 1. Klonla ve kur
git clone https://github.com/KaracaDeer/Luminis_AI_Library_Chatbot.git
cd Luminis_AI_Library_Chatbot
make install

# 2. Ortamı yapılandır
echo "OPENAI_API_KEY=anahtarınız_burada" > .env

# 3. Geliştirmeyi başlat
make dev
```

**Erişim**: Frontend (http://localhost:5173) | Backend (http://localhost:5000) | API Dokümantasyonu (http://localhost:5000/docs)

### Docker Hızlı Başlangıç
```bash
docker-compose up -d
```

## 🏗️ Mimari

```
Kullanıcı → Frontend → API → Backend → AI Modelleri → Öneriler
    ↓         ↓        ↓       ↓         ↓           ↓
React    Sohbet   FastAPI  RAG     GPT-4      Kişiselleştirilmiş
UI      Giriş    Sunucu   Sistemi ChromaDB      Sonuçlar
```

📖 [Detaylı Mimari](docs/architecture.md)

## ✨ Ana Özellikler

- 🎤 **Ses İşleme** - OpenAI Whisper ile gerçek zamanlı konuşma-metin dönüşümü
- 🤖 **AI/ML Entegrasyonu** - GPT-4, ChromaDB vektör arama, RAG sistemi
- 🔄 **Gerçek Zamanlı Sohbet** - WebSocket tabanlı canlı konuşmalar
- 🚀 **Anlamsal Arama** - Kitapları anahtar kelimeler yerine anlamlarıyla bulun
- 🔐 **Güvenli Kimlik Doğrulama** - JWT, OAuth2 ile Google, GitHub, Microsoft
- 📊 **Açık Kütüphane** - API entegrasyonu ile milyonlarca kitaba erişim

## 🤖 AI/ML Performansı

### Model Performansı
| Model | Doğruluk | Gecikme | Güven | Diller |
|-------|----------|---------|--------|--------|
| **GPT-4** | %95.8 | 1.2s | 0.94 | 50+ |
| **ChromaDB Vektör Arama** | %89.3 | 0.3s | 0.87 | Çok Dilli |
| **OpenAI Whisper** | %92.1 | 0.8s | 0.91 | 50+ |

### Örnek Konuşmalar

**Kitap Önerisi Sorgusu:**
- Giriş: "Yapay zeka ve etik hakkında bir şeyler okumak istiyorum"
- Çıkış: "Isaac Asimov'un 'Ben, Robot' ve Philip K. Dick'in 'Androidler Elektrikli Koyun Düşler mi?' kitaplarını öneririm. Her ikisi de AI bilincini ve etik sonuçlarını keşfediyor..."
- Güven: 0.94 | İşlem Süresi: 1.1s

**Anlamsal Arama Sorgusu:**
- Giriş: "Hayatın anlamını düşündüren kitaplar"
- Çıkış: "Alchemist", "Siddhartha", "İnsanın Anlam Arayışı" dahil olmak üzere 15 anlamsal olarak benzer kitap bulundu
- Güven: 0.89 | İşlem Süresi: 0.4s

### MLflow Dashboard
- **Yerel**: http://localhost:5000
- **Özellikler**: Model versiyonlama, deney takibi, performans metrikleri
- **Vektör gömme ve benzerlik takibi**

📊 [Detaylı ML Performans Raporu](docs/ml_performance.md)

## 🛠️ Teknoloji Yığını

### Frontend
- React 18, TypeScript, TailwindCSS, Framer Motion
- Ses desteği ile gerçek zamanlı sohbet arayüzü

### Backend
- FastAPI, Python 3.11+, WebSocket streaming
- SQLAlchemy, ChromaDB vektör veritabanı

### AI/ML
- **OpenAI GPT-4** akıllı konuşmalar için
- **OpenAI Whisper** konuşma-metin dönüşümü için
- **ChromaDB** anlamsal vektör arama için
- **RAG Sistemi** geri getirme-artırılmış üretim için
- **LangChain** AI iş akışı orkestrasyonu için

### Altyapı
- Docker, Redis, SQLite, Nginx

## 📁 Proje Yapısı

```
Luminis_AI_Library_Chatbot/
├── src/                    # Backend kaynak kodu
│   ├── backend/           # FastAPI uygulaması
│   ├── frontend/          # React uygulaması
│   ├── services/          # AI/ML servisleri
│   ├── database/          # Veritabanı modelleri
│   └── services/          # API servisleri
├── tests/                 # Test paketi
├── docs/                  # Dokümantasyon
├── docker/                # Docker yapılandırmaları
└── scripts/               # Yardımcı scriptler
```

📖 [Detaylı Proje Yapısı](docs/architecture.md)

## 🧪 Test ve Geliştirme

```bash
make test          # Tüm testleri çalıştır (%85+ kapsam)
make lint          # Kod linting
make format        # Kod formatlama
make type-check    # TypeScript tip kontrolü
```

📋 [Test Dokümantasyonu](tests/README.md)

## 📚 Dokümantasyon

- 📖 [Mimari Rehberi](docs/architecture.md)
- 🤖 [AI/ML Özellikleri Rehberi](README_TR.md#ai-ml-performansı)
- 🧪 [Test Dokümantasyonu](tests/README.md)
- 🚀 [Dağıtım Rehberi](docs/deployment.md)
- 📋 [API Dokümantasyonu](http://localhost:5000/docs)

## 🔧 Yapılandırma

### Ortam Değişkenleri

```bash
# Gerekli
OPENAI_API_KEY=openai_api_anahtarınız_burada

# İsteğe bağlı
PORT=5000
HOST=127.0.0.1
DATABASE_URL=sqlite:///./luminis_library.db
CHROMA_PERSIST_DIRECTORY=./chroma_db
JWT_SECRET_KEY=jwt_gizli_anahtarınız_burada
```

📝 [Tam Yapılandırma Rehberi](docs/configuration.md)

## 📋 Mevcut Komutlar

| Komut | Açıklama |
|-------|----------|
| `make install` | Tüm bağımlılıkları yükle |
| `make dev` | Geliştirme sunucularını başlat |
| `make test` | Tüm testleri çalıştır |
| `make lint` | Kod linting |
| `make format` | Kod formatlama |
| `make type-check` | TypeScript tip kontrolü |
| `make docker-up` | Docker servislerini başlat |
| `make health` | Servis sağlığını kontrol et |

📋 [Tam Komut Referansı](docs/commands.md)

## 🤝 Katkıda Bulunma ve Destek

### 🚀 Katkıda Bulunma
1. **Repository'yi fork edin**
2. **Özellik dalı oluşturun**: `git checkout -b feature/harika-ozellik`
3. **Değişikliklerinizi yapın**
4. **Testleri çalıştırın**: `make test`
5. **Pull request gönderin**

**Detaylı rehberler için [CONTRIBUTING.md](CONTRIBUTING.md) dosyasına bakın**

### 💬 Destek
- **🐛 Sorunlar**: [GitHub Issues](https://github.com/KaracaDeer/Luminis_AI_Library_Chatbot/issues)
- **💭 Tartışmalar**: [GitHub Discussions](https://github.com/KaracaDeer/Luminis_AI_Library_Chatbot/discussions)
- **💼 LinkedIn**: [Fatma Karaca Erdogan](https://www.linkedin.com/in/fatma-karaca-erdogan-32201a378/)
- **📧 E-posta**: fatmakaracaerdogan@gmail.com

## 📝 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır - detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🙏 Teşekkürler

* **OpenAI** - En son teknoloji AI modelleri sağladığı için
* **FastAPI** - Yüksek performanslı backend framework'ü için
* **React Ekibi** - Harika frontend kütüphanesi için
* **ChromaDB** - Vektör veritabanı ve anlamsal arama için
* **LangChain** - LLM uygulama framework'ü için
* **Docker** - Konteynerleştirme ve dağıtım için
