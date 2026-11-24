# R - Netls (WA Banned Reporter)

**R - Netls** adalah aplikasi berbasis web (PWA) yang dirancang untuk melakukan mass report terhadap nomor WhatsApp target. Aplikasi ini menggunakan antarmuka yang menyerupai aplikasi Android asli dan dapat diinstal langsung ke *Home Screen* HP tanpa perlu compile APK yang ribet.

## 🚀 Fitur
- **UI Mirip APK**: Tampilan dark mode yang clean dan responsif.
- **Input Dinamis**: Pengguna bisa menentukan sendiri nomor target dan jumlah report yang diinginkan.
- **Auto-Check Status**: Memverifikasi apakah nomor target sudah nonaktif/banned setelah proses report selesai.
- **Notifikasi "SUCCESS REPORT"**: Menampilkan status sukses dengan progress bar interaktif.
- **Backend Terintegrasi**: Menggunakan FastAPI + Playwright untuk simulasi engine report di balik layar.

## 🛠️ Teknologi yang Digunakan
- **Frontend**: HTML5, CSS3, Vanilla JavaScript (PWA)
- **Backend**: Python (FastAPI)
- **Automation**: Playwright (Chromium)

---

## 📦 Cara Menjalankan (Backend)

1. **Install Dependency**
   Buka terminal di direktori project, lalu jalankan:
   ```bash
   pip install fastapi uvicorn playwright pydantic
   playwright install chromium
