# Quran Tafsir

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

**Platform pencarian tafsir Al-Qur'an yang terverifikasi dan tervalidasi, bersumber dari ulama-ulama Ahlus Sunnah wal Jamaah yang terpercaya.**

*"Sesungguhnya Al-Qur'an ini memberikan petunjuk ke jalan yang paling lurus"*
-- QS. Al-Isra: 9

[Tentang](#tentang) | [Fitur](#fitur) | [Instalasi](#instalasi) | [API Docs](#api-documentation) | [Kontribusi](#kontribusi)

</div>

---

## Tentang

Quran Tafsir adalah platform open-source untuk belajar Al-Qur'an dengan tafsir yang bersumber langsung dari ulama-ulama Ahlus Sunnah yang terpercaya. Semua tafsir yang ada di sini sudah melalui proses verifikasi ketat untuk memastikan kesesuaian dengan pemahaman para ulama terdahulu yang diakui.

Project ini dibangun untuk siapa saja yang ingin belajar tafsir dengan cara yang lebih modern, mudah diakses, dan mudah dicari -- tanpa harus membuka belasan kitab fisik sekaligus.

### Sumber Tafsir yang Tersedia

| Ulama | Kitab | Status |
|-------|-------|--------|
| Ibnu Katsir (w. 774 H) | Tafsir Al-Qur'an Al-'Azhim | Terverifikasi |
| Ath-Thabari (w. 310 H) | Jami' Al-Bayan | Terverifikasi |
| As-Sa'di (w. 1376 H) | Taisir Al-Karim Ar-Rahman | Terverifikasi |
| Al-Baghawi (w. 516 H) | Ma'alim At-Tanzil | Terverifikasi |
| Al-Qurthubi (w. 671 H) | Al-Jami' li Ahkam Al-Qur'an | Terverifikasi |

> Semua tafsir yang ada di sini sudah diseleksi berdasarkan kesesuaian aqidah dengan Ahlus Sunnah wal Jamaah. Kalau sumbernya meragukan, langsung ditolak.

---

## Fitur

### Yang Sudah Berjalan

- **Pencarian Cerdas** -- Cari ayat, surah, tema, atau topik. Menggunakan BM25 hybrid search, bukan sekadar pencarian biasa.
- **Multi-Tafsir** -- Lihat tafsir dari beberapa mufassir sekaligus untuk satu ayat.
- **Kutipan Ayat Relevan** -- Setiap pencarian otomatis menampilkan ayat-ayat lain yang relevan dengan topik yang dicari.
- **Sumber Terverifikasi** -- Sistem validator otomatis yang menolak tafsir dari sumber yang tidak sesuai.
- **Mode Gelap** -- Tampilan gelap yang nyaman untuk membaca di malam hari.
- **Kutipan Harian** -- Kutipan acak dari Al-Qur'an setiap kali membuka halaman.
- **Analitik Tematik** -- Visualisasi distribusi tema besar dalam Al-Qur'an.

### Fitur yang Sedang Dibangun

- **Asisten Tafsir AI** -- Tanya jawab konteks ayat berbasis RAG, jawabannya merujuk ke tafsir ulama yang terverifikasi.
- **Grafik Hubungan Ayat** -- Visualisasi interaktif hubungan antar ayat secara tematik.
- **Audio Murattal** -- Murattal dengan sinkronisasi ke teks.
- **Catatan Belajar** -- Catatan pribadi per ayat.
- **Pelacak Progres** -- Lacak seberapa jauh progres belajar tafsir.
- **Mode Offline** -- Akses tanpa internet melalui PWA.

---

## Struktur Project

```
quran-tafsir/
├── backend/
│   ├── api/
│   │   ├── tafsir.py          # Mesin pencarian utama
│   │   ├── quotes.py          # Mesin kutipan relevan
│   │   ├── analytics.py       # Analitik tematik
│   │   └── ai_assistant.py    # AI tanya jawab (arsitektur RAG)
│   ├── data/
│   │   └── quotes_db.py       # Database kutipan Al-Qur'an
│   ├── utils/
│   │   ├── validator.py       # Validator sumber
│   │   └── search_engine.py   # Mesin pencarian hybrid BM25
│   └── main.py                # FastAPI entry point
├── frontend/
│   └── index.html             # Tampilan utama (Tailwind CSS)
├── tests/
│   └── test_tafsir.py         # Unit tests
├── docs/
│   ├── API.md                 # Dokumentasi endpoint
│   └── CONTRIBUTING.md        # Panduan kontribusi
├── data/
│   └── sources.md             # Daftar sumber terverifikasi
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

### Tech Stack

| Layer | Teknologi |
|-------|-----------| 
| Backend | Python 3.10+, FastAPI, Pydantic |
| Search | BM25 (rank-bm25), Semantic Search (sentence-transformers) |
| Frontend | HTML, Tailwind CSS, Vanilla JS |
| Database | SQLite (lokal) / PostgreSQL (production) |
| Cache | Redis (opsional) |
| Deployment | Nginx, systemd, Cloudflare |

---

## Instalasi

Pilih sistem operasi:
- [Windows](#windows)
- [macOS](#macos)
- [Linux -- Ubuntu 24.04 LTS](#linux----ubuntu-2404-lts) (direkomendasikan)

---

### Windows

**1. Install Python**

Download Python 3.11+ dari [python.org/downloads](https://www.python.org/downloads/).

Pastikan centang **"Add Python to PATH"** waktu install. Verifikasi:

```cmd
python --version
```

**2. Install Git**

Download dari [git-scm.com](https://git-scm.com/download/win). Install dengan semua default settings.

**3. Clone dan Setup**

Buka **Command Prompt** atau **PowerShell**, lalu:

```cmd
git clone https://github.com/bushidoways/quran-tafsir.git
cd quran-tafsir
```

Buat virtual environment:

```cmd
python -m venv venv
venv\Scripts\activate
```

Kalau muncul error soal execution policy di PowerShell, jalankan dulu:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Install dependencies:

```cmd
pip install -r requirements.txt
```

**4. Jalankan Server**

```cmd
uvicorn backend.main:app --reload --port 8000
```

Buka browser ke `http://127.0.0.1:8000`.

---

### macOS

**1. Install Homebrew** (kalau belum ada)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**2. Install Python dan Git**

```bash
brew install python git
```

Verifikasi:

```bash
python3 --version
git --version
```

**3. Clone dan Setup**

```bash
git clone https://github.com/bushidoways/quran-tafsir.git
cd quran-tafsir
```

Buat virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

**4. Jalankan Server**

```bash
uvicorn backend.main:app --reload --port 8000
```

Buka browser ke `http://127.0.0.1:8000`.

---

### Linux -- Ubuntu 24.04 LTS

Ini yang paling direkomendasikan. Ubuntu 24.04 sudah menyertakan Python 3.12 secara bawaan.

**1. Update System**

```bash
sudo apt update && sudo apt upgrade -y
```

**2. Install Dependencies**

```bash
sudo apt install -y python3 python3-pip python3-venv git curl
```

Verifikasi:

```bash
python3 --version
git --version
```

**3. Clone Repository**

```bash
git clone https://github.com/bushidoways/quran-tafsir.git
cd quran-tafsir
```

**4. Setup Virtual Environment**

```bash
python3 -m venv venv
source venv/bin/activate
```

Akan muncul `(venv)` di awal baris terminal. Itu tandanya virtual environment aktif.

**5. Install Dependencies**

```bash
pip install -r requirements.txt
```

**6. Jalankan Server**

```bash
uvicorn backend.main:app --reload --port 8000
```

Output yang benar:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Started reloader process using StatReload
INFO:     Application startup complete.
```

Buka browser ke `http://127.0.0.1:8000`.

**7. (Opsional) Jalankan Tests**

```bash
pytest tests/ -v
```

---

## API Documentation

Setelah server jalan, buka `http://127.0.0.1:8000/docs` untuk interactive Swagger UI.

### Endpoints Utama

#### Search Tafsir
```
GET /search?q={kata_kunci}
```

Parameter:
| Nama | Tipe | Wajib | Keterangan |
|------|------|-------|------------|
| q | string | ya | Kata kunci pencarian |
| mufassir | string | tidak | ibnu_katsir / as_sadi / al_baghawi / all (default: all) |
| limit | int | tidak | Jumlah hasil, max 50 (default: 10) |

Contoh response:
```json
{
  "query": "tauhid",
  "total": 3,
  "results": [
    {
      "surah": 112,
      "ayat": 1,
      "surah_name": "Al-Ikhlas",
      "arabic": "...",
      "translation": "...",
      "tafsir": "...",
      "mufassir": "ibnu_katsir",
      "relevance_score": 0.98
    }
  ],
  "relevant_quotes": [...]
}
```

#### Tafsir per Ayat
```
POST /tafsir/ayat
```

Request body:
```json
{
  "surah": 2,
  "ayat": 255,
  "mufassir": "ibnu_katsir"
}
```

#### Kutipan Relevan
```
GET /quotes/random
```

#### Analitik Tematik
```
GET /analytics/topics
```

#### Health Check
```
GET /health
```

---

## Prinsip Verifikasi Sumber

Bukan semua tafsir diterima. Ini kriteria yang harus dipenuhi supaya tafsir bisa masuk ke database:

1. **Aqidah** -- Harus sesuai dengan aqidah Ahlus Sunnah wal Jamaah. Tidak ada kompromi di sini.
2. **Manhaj** -- Berdasarkan pemahaman ulama terdahulu (tiga generasi pertama umat Islam).
3. **Sanad** -- Ada jalur keilmuan yang bisa dilacak ke sumber aslinya.
4. **Mufassir** -- Penulisnya diakui oleh para ulama sebagai ahli tafsir yang tsiqah (terpercaya).
5. **Penerbit** -- Data diambil dari penerbit mu'tabar yang dikenal di kalangan ahli ilmu.

Sumber yang otomatis ditolak: tafsir Qadiyaniyah, tafsir Batiniyyah, dan tafsir yang melandaskan penafsirannya pada hawa nafsu bukan dalil.

---

## Kontribusi

Baca [CONTRIBUTING.md](./docs/CONTRIBUTING.md) dulu sebelum submit apapun.

Alur kontribusi standar:

```bash
# Fork repo ini dulu di GitHub, lalu:
git clone https://github.com/USERNAME_KAMU/quran-tafsir.git
cd quran-tafsir

git checkout -b feat/nama-fitur-kamu

# Kerjakan perubahannya...

git add .
git commit -m "feat: deskripsi singkat perubahan"
git push origin feat/nama-fitur-kamu

# Lalu buka Pull Request di GitHub
```

Prioritas kontribusi yang paling dibutuhkan sekarang:
- Data tafsir dalam format JSON untuk surah-surah yang belum ada
- Peningkatan relevance score di search engine
- Perbaikan bug
- Terjemahan UI ke bahasa lain

---

## Troubleshooting

**ModuleNotFoundError: No module named 'backend'**

Kemungkinan menjalankan uvicorn dari folder yang salah, atau PYTHONPATH belum mengenali struktur project ini.

```bash
# Pastikan berada di root folder project
pwd
# Output harus: /path/ke/quran-tafsir

# Kalau masih error, jalankan dengan explicit PYTHONPATH
PYTHONPATH=. uvicorn backend.main:app --reload
```

**Port 8000 already in use**

```bash
# Ganti ke port lain
uvicorn backend.main:app --reload --port 8001
```

**pip install gagal di scikit-learn**

Versi Python kemungkinan terlalu lama. Pastikan Python 3.10+ yang dipakai:

```bash
python3 --version

# Kalau masih error, skip scikit-learn dulu
pip install -r requirements.txt --ignore-requires-python
```

---

## Lisensi

[MIT License](LICENSE) -- bebas digunakan, dimodifikasi, dan disebarkan untuk kebaikan.

---

<div align="center">

*"Dan Kami turunkan Al-Qur'an sebagai penawar dan rahmat bagi orang-orang yang beriman"*

-- QS. Al-Isra: 82

Open source untuk umat.

</div>
