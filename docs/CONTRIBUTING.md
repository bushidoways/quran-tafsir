# Panduan Kontribusi

Terima kasih atas minat Anda untuk berkontribusi pada proyek Quran Tafsir. Berikut panduan untuk membantu Anda memulai.

## Cara Berkontribusi

### 1. Laporkan Bug

Jika menemukan bug, silakan buat issue di GitHub dengan informasi berikut:
- Deskripsi singkat masalah
- Langkah-langkah untuk mereproduksi
- Perilaku yang diharapkan vs yang terjadi
- Screenshot (jika ada)

### 2. Ajukan Fitur Baru

Untuk mengajukan ide fitur baru:
- Buat issue dengan label "fitur baru"
- Jelaskan fitur yang diinginkan dan manfaatnya
- Berikan contoh penggunaan jika memungkinkan

### 3. Kontribusi Kode

#### Persiapan

1. Fork repository ini
2. Clone ke komputer Anda:

```bash
git clone https://github.com/USERNAME_ANDA/quran-tafsir.git
cd quran-tafsir
```

3. Buat branch baru:

```bash
git checkout -b fitur/nama-fitur-baru
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

#### Aturan Kode

- Gunakan bahasa Indonesia yang jelas dan mudah dipahami untuk komentar dan dokumentasi
- Ikuti style guide PEP 8 untuk kode Python
- Tambahkan unit test untuk setiap fitur baru
- Pastikan semua test lulus sebelum membuat Pull Request

#### Aturan Konten Tafsir

Konten tafsir harus memenuhi kriteria berikut:

Yang diterima:
- Tafsir dari mufassir yang diakui oleh ulama Ahlus Sunnah wal Jama'ah
- Penjelasan yang berdasarkan dalil Al-Qur'an dan Hadits shahih
- Pendapat yang didukung oleh ijma' ulama

Yang tidak diterima:
- Tafsir dari sumber yang menyimpang dari Ahlus Sunnah
- Pendapat tanpa landasan dalil yang jelas
- Konten yang kontroversial tanpa landasan ilmiah yang bisa diverifikasi

### 4. Pull Request

1. Pastikan kode Anda sudah bersih dan terformat rapi
2. Tulis deskripsi yang jelas tentang perubahan yang dilakukan
3. Referensikan issue terkait (jika ada)
4. Tunggu review dari maintainer

## Struktur Proyek

```
quran-tafsir/
├── backend/           # Backend API (FastAPI)
│   ├── app/          # Aplikasi utama
│   ├── api/          # Router dan endpoint
│   ├── data/         # Database lokal
│   ├── utils/        # Utilitas
│   └── tests/        # Unit test
├── frontend/         # Frontend (HTML/Next.js)
├── docs/             # Dokumentasi
├── data/             # Data dan sumber
└── tests/            # Test tambahan
```

## Kode Etik

- Hormati sesama kontributor
- Berikan feedback yang konstruktif
- Fokus pada kualitas konten dan keakuratan ilmiah
- Semua diskusi harus berdasarkan dalil dan rujukan yang jelas

## Pertanyaan?

Jika ada pertanyaan, silakan buat issue di GitHub atau hubungi maintainer.

Jazakumullahu khairan atas kontribusinya.
