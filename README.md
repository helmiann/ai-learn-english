# 🤖 English Grammar Chatbot

Aplikasi chatbot berbasis web untuk membantu **Siswa SMP** belajar grammar Bahasa Inggris secara interaktif. Dibangun menggunakan FastAPI, PostgreSQL, Redis, dan Llama AI.

---

## 📋 Fitur

- 🔐 Login & autentikasi pengguna
- 💬 Percakapan interaktif dengan AI untuk belajar grammar
- 📚 Rekomendasi topik percakapan
- 🧠 Context manager untuk menjaga konsistensi percakapan
- 📖 Riwayat percakapan
- 🗂️ Ringkasan otomatis percakapan sebelumnya

---

## 🛠️ Tech Stack

| Layer | Teknologi |
|---|---|
| Frontend | React / Vue + Vite |
| Backend | FastAPI (Python) |
| Database | PostgreSQL |
| Cache | Redis |
| AI | Llama API (External) |
| Web Server | Nginx |
| Container | Docker & Docker Compose |

---

## 📁 Struktur Proyek

```
english-grammar-chatbot/
├── backend/              # FastAPI server
├── frontend/             # Web app
├── nginx/                # Konfigurasi Nginx
├── logs/                 # Output log aplikasi
├── docker-compose.yml    # Production setup
└── docker-compose.dev.yml # Development setup
```

---

## 🚀 Cara Menjalankan

### Prasyarat

Pastikan sudah menginstall:
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Python 3.11+](https://python.org)
- [Node.js LTS](https://nodejs.org)
- [Git](https://git-scm.com)

### 1. Clone Repository

```bash
git clone https://github.com/username/english-grammar-chatbot.git
cd english-grammar-chatbot
```

### 2. Setup Environment Variables

```bash
cp .env.example .env
```

Edit file `.env` dan isi semua variabel yang dibutuhkan (lihat bagian [Environment Variables](#-environment-variables)).

### 3. Jalankan dengan Docker (Rekomendasi)

**Mode Production:**
```bash
docker-compose up --build
```

**Mode Development:**
```bash
docker-compose -f docker-compose.dev.yml up --build
```

### 4. Jalankan Manual (Tanpa Docker)

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## 🌐 Akses Aplikasi

| Service | URL |
|---|---|
| Web App | http://localhost |
| API Backend | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| API Docs (ReDoc) | http://localhost:8000/redoc |

---

## 🔑 Environment Variables

| Variabel | Deskripsi | Contoh |
|---|---|---|
| `POSTGRES_USER` | Username PostgreSQL | `postgres` |
| `POSTGRES_PASSWORD` | Password PostgreSQL | `rahasia123` |
| `POSTGRES_DB` | Nama database | `grammar_chatbot` |
| `DATABASE_URL` | URL koneksi database | `postgresql://...` |
| `REDIS_URL` | URL koneksi Redis | `redis://redis:6379` |
| `SECRET_KEY` | Secret key JWT | `your-secret-key` |
| `ALGORITHM` | Algoritma JWT | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Durasi token login | `60` |
| `LLAMA_API_URL` | URL Llama API | `https://api.llama...` |
| `LLAMA_API_KEY` | API Key Llama | `llm-xxx...` |
| `LLAMA_MODEL` | Nama model Llama | `llama-3-8b` |

---

## 📊 Database

Skema database terdiri dari 5 tabel utama:

- **user** — Data akun pengguna
- **chats** — Sesi percakapan
- **chat_massages** — Pesan dalam percakapan
- **chat_summary** — Ringkasan otomatis percakapan
- **context_metadata** — Metadata konteks untuk AI

---

## 🧪 Testing API

Setelah backend berjalan, buka browser dan akses:
```
http://localhost:8000/docs
```

---

## 📝 Kontribusi

1. Fork repository ini
2. Buat branch fitur baru: `git checkout -b fitur/nama-fitur`
3. Commit perubahan: `git commit -m 'Menambahkan fitur X'`
4. Push ke branch: `git push origin fitur/nama-fitur`
5. Buat Pull Request

---

## 📄 Lisensi

MIT License — bebas digunakan untuk keperluan pendidikan.
