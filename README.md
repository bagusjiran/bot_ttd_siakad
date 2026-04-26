# ⚡ SIAKAD KPT — Auto Absensi Bot V3 (Full Auto Stealth)

Bot otomasi absensi cerdas yang dirancang khusus untuk mahasiswa **STT Ronggolawe Cepu**. Versi **V4** ini merupakan evolusi tertinggi yang menggabungkan fitur *Stealth Mode* untuk melewati proteksi Cloudflare dan sistem *Persistent Profile* agar bot mengenali perangkat Anda seperti browser asli.

---

## ✨ Fitur Unggulan V4
* **🛡️ Anti-Cloudflare (Stealth Mode):** Menggunakan teknik `ignore_default_args` untuk menghapus jejak otomatisasi ("Chrome is being controlled...") yang sering memicu blokir Cloudflare.
* **👤 Persistent Profile (Bukan Incognito):** Bot menyimpan session dan cookies di folder `chrome_bot_profile`. Jika Anda sudah login sekali, bot akan mengingatnya (Sama seperti browser utama).
* **🔐 Full Auto Login:** Masukkan NIM dan Password langsung di GUI, bot yang akan melakukan proses pengisian.
* **📂 Smart Navigation:** Otomatis membuka sidebar **E-learning** lalu menuju menu **Absensi** tanpa intervensi pengguna.
* **✏️ High-Precision Signature:** Menggunakan koordinat asli (inisial "JR") yang sudah diuji 95% identik dengan tanda tangan manual.
* **🔄 Anti-Bug Refresh:** Sistem otomatis memancing refresh tabel dengan mengubah filter semester (Gasal -> Genap) untuk memastikan tombol merah muncul setelah tanda tangan disimpan.

---

## 🛠️ Persyaratan Sistem
1.  **Python 3.10+**
2.  **Google Chrome** versi terbaru terinstal di Windows.
3.  **Library Python:**
    * `playwright` (Engine browser)
    * `tkinter` (Bawaan Python untuk GUI)

---

## 🚀 Instalasi

1.  **Clone atau download repo ini.**
2.  **Install dependencies:**
    Buka CMD di folder script, lalu jalankan:
    ```bash
    pip install playwright
    playwright install chrome
    ```
3.  **Jalankan aplikasi:**
    ```bash
    python absensi_bot.py
    ```

---

## 📖 Alur Penggunaan

Bot bekerja dengan alur **"Set-and-Forget"** (Setel dan Tinggalkan):

1.  **Input Kredensial:** Masukkan NIM dan Password SIAKAD Anda pada kolom yang tersedia di GUI.
2.  **Klik "Mulai Otomatis":** Bot akan membuka jendela Chrome asli.
3.  **Verifikasi Cloudflare:** * Jika muncul halaman "Verify you are human", bot akan mencoba mengklik otomatis. 
    * Jika gagal (karena proteksi tinggi), Anda cukup membantu mengklik kotak verifikasi tersebut **satu kali**.
4.  **Login & Navigasi:** Setelah lolos Cloudflare, bot akan mengisi form login, masuk ke Dashboard, lalu secara otomatis mencari menu **E-learning > Absensi** di sidebar.
5.  **Proses Tanda Tangan:**
    * Bot memindai semua tombol merah (pertemuan yang belum absen).
    * Mengklik tombol, menggambar tanda tangan presisi, dan menyimpan.
    * Melakukan trik "Refresh Semester" untuk memvalidasi status absensi terbaru.
6.  **Selesai:** Bot akan memberikan laporan jumlah pertemuan yang berhasil ditandatangani di bagian Log.

---

## ⚠️ Catatan Keamanan
* **Data Profile:** Folder `chrome_bot_profile` berisi session login Anda. Jangan bagikan folder ini kepada orang lain.
* **Mode Manual:** Jika website SIAKAD sedang maintenance atau lambat, Anda bisa menekan tombol **Stop** untuk mengambil alih kontrol browser secara manual.

---

## 👨‍💻 Developer
* **Nama:** Mohamad Bagus Jiran Riskohar
* **Prodi:** Informatika - STT Ronggolawe
* **Versi:** 4.0.0 (Stealth Edition)
