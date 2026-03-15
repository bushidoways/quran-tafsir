# Dokumentasi API Quran Tafsir

Dokumentasi lengkap untuk semua endpoint API yang tersedia.

## URL Dasar

```
http://localhost:8000/api/v1
```

## Autentikasi

Saat ini API bersifat publik dan tidak memerlukan autentikasi. Pada versi mendatang, beberapa endpoint mungkin memerlukan API key.

---

## Endpoint

### 1. Pencarian Tafsir

**GET** `/api/v1/search`

Cari ayat dan tafsir berdasarkan kata kunci.

**Parameter:**

| Parameter | Tipe | Wajib | Default | Keterangan |
|-----------|------|-------|---------|------------|
| `q` | string | Ya | - | Kata kunci pencarian |
| `mufassir` | string | Tidak | `ibn-kathir` | ID mufassir |
| `page` | integer | Tidak | `1` | Nomor halaman |
| `limit` | integer | Tidak | `10` | Hasil per halaman (maks 50) |

**Contoh:**

```bash
curl "http://localhost:8000/api/v1/search?q=sabar&mufassir=ibn-kathir"
```

**Response:**

```json
{
  "query": "sabar",
  "mufassir": "ibn-kathir",
  "total_results": 15,
  "results": [
    {
      "surah": 2,
      "ayah": 153,
      "text": "Wahai orang-orang yang beriman, mohonlah pertolongan dengan sabar dan shalat...",
      "tafsir_snippet": "Ibnu Katsir menjelaskan bahwa sabar adalah..."
    }
  ],
  "quote": "Sesungguhnya bersama kesulitan ada kemudahan. (QS. Al-Insyirah: 6)"
}
```

---

### 2. Tafsir per Ayat

**GET** `/api/v1/tafsir/{surah}/{ayah}`

Ambil tafsir lengkap untuk ayat tertentu.

**Parameter:**

| Parameter | Tipe | Wajib | Keterangan |
|-----------|------|-------|------------|
| `surah` | integer | Ya | Nomor surah (1-114) |
| `ayah` | integer | Ya | Nomor ayat |
| `mufassir` | string | Tidak | ID mufassir (default: `ibn-kathir`) |

**Contoh:**

```bash
curl "http://localhost:8000/api/v1/tafsir/1/1?mufassir=ibn-kathir"
```

**Response:**

```json
{
  "surah": 1,
  "ayah": 1,
  "text_arab": "...",
  "terjemahan": "Dengan nama Allah Yang Maha Pengasih, Maha Penyayang.",
  "tafsir": "Konten tafsir lengkap...",
  "mufassir": {
    "id": "ibn-kathir",
    "name": "Ibnu Katsir",
    "kitab": "Tafsir Al-Qur'an Al-'Azhim"
  }
}
```

---

### 3. Daftar Mufassir

**GET** `/api/v1/mufassireen`

Tampilkan semua mufassir yang tersedia dan terverifikasi.

**Contoh:**

```bash
curl "http://localhost:8000/api/v1/mufassireen"
```

---

### 4. Daftar Surah

**GET** `/api/v1/surah`

Tampilkan seluruh 114 surah dalam Al-Qur'an.

**GET** `/api/v1/surah/{surah_number}`

Ambil detail surah tertentu.

---

### 5. Quotes Al-Qur'an

**GET** `/api/v1/quotes/random`

Ambil quotes Al-Qur'an secara acak.

**GET** `/api/v1/quotes/daily`

Ambil ayat harian untuk inspirasi.

---

### 6. Analitik Tematik

**GET** `/api/v1/analytics/themes`

Tampilkan distribusi tema dan topik dalam Al-Qur'an.

---

### 7. Asisten AI (Beta)

**GET** `/api/v1/ai/ask`

Ajukan pertanyaan seputar tafsir Al-Qur'an. Jawaban dihasilkan berdasarkan konteks tafsir ulama.

**Parameter:**

| Parameter | Tipe | Wajib | Keterangan |
|-----------|------|-------|------------|
| `question` | string | Ya | Pertanyaan tentang tafsir |

**GET** `/api/v1/ai/validate`

Validasi apakah sumber mufassir terverifikasi.

---

### 8. Daftar Fitur

**GET** `/api/v1/features`

Tampilkan semua fitur yang tersedia di platform.

---

### 9. Health Check

**GET** `/health`

Periksa status server.

---

## Kode Status

| Kode | Keterangan |
|------|------------|
| 200 | Berhasil |
| 400 | Request tidak valid |
| 404 | Data tidak ditemukan |
| 500 | Kesalahan server |

## Catatan

- Semua sumber tafsir telah diverifikasi dan divalidasi
- API mendukung 10 mufassir terverifikasi
- Fitur Asisten AI masih dalam tahap beta
- Untuk pertanyaan atau laporan bug, silakan buka issue di GitHub
