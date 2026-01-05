# P&ID Equipment Extractor (AI-Powered)

Proyek ini adalah alat otomatisasi berbasis Python yang menggunakan teknologi **Computer Vision (OCR)** untuk mengekstrak daftar *Equipment* (Tag dan Deskripsi) serta judul dokumen dari file P&ID (Piping and Instrumentation Diagram) dalam format PDF.

Sistem ini dioptimalkan untuk berjalan pada perangkat dengan sumber daya terbatas, seperti **MacBook M1 RAM 8GB**, dengan menggunakan strategi *Progressive Processing* dan *Region of Interest (ROI) Analysis*.

## ✨ Fitur Utama
- **High-Accuracy OCR**: Menggunakan PaddleOCR (PP-OCRv5) untuk pembacaan teks teknis yang tajam.
- **ROI Optimization**: Fokus hanya pada area tabel equipment dan title block untuk menghemat CPU/RAM.
- **Memory Safety**: Pembersihan cache RAM otomatis (Garbage Collection) per halaman.
- **Progressive Save**: Menyimpan hasil langsung ke Excel per halaman. Jika program terhenti, proses dapat dilanjutkan tanpa mengulang dari awal.
- **Auto-Split Support**: Memproses file PDF yang telah dipisah per halaman untuk stabilitas maksimal.

## 🛠️ Prasyarat (Prerequisites)
Pastikan Anda sudah menginstal:
- [Python 3.10+](https://www.python.org/downloads/)
- [uv](https://github.com/astral-sh/uv) (Python package manager yang sangat cepat)
- [Poppler](https://poppler.freedesktop.org/) (Untuk konversi PDF ke gambar)
  - Di Mac: `brew install poppler`

## 🚀 Instalasi

1. **Clone repositori:**
   ```bash
   git clone [https://github.com/username/pid-extractor.git](https://github.com/username/pid-extractor.git)
   cd pid-extractor
