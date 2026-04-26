# ⚡ SIAKAD KPT — Auto Absensi Bot V4 (Full Auto Stealth)

Bot otomasi absensi cerdas yang dirancang khusus untuk mahasiswa **STT Ronggolawe Cepu**. Versi ini dilengkapi dengan *Stealth Mode* untuk menembus Cloudflare, sistem navigasi otomatis, dan fitur untuk menggunakan tanda tangan asli kamu sendiri.

---

## 📁 Struktur File
Berikut adalah kegunaan dari masing-masing *file* dalam proyek ini:
* [cite_start]`INSTALL.bat`: Script otomatis untuk menginstal Python library yang dibutuhkan[cite: 1, 2].
* `absen.py`: Aplikasi kanvas untuk menggambar dan merekam koordinat tanda tangan aslimu.
* `hasil.py`: Aplikasi untuk menguji coba (preview) animasi tanda tangan sebelum dimasukkan ke bot.
* `absensi_bot.py`: Script bot utama yang menjalankan proses otomasi secara penuh.
* [cite_start]`JALANKAN.bat`: Script otomatis untuk menjalankan bot utama dengan satu kali klik[cite: 4].

---

## 🚀 Langkah 1: Instalasi
Jika ini adalah pertama kalinya kamu menggunakan bot ini di komputermu, ikuti langkah berikut:
1. [cite_start]Pastikan **Python** sudah terinstal di komputermu (centang "Add to PATH" saat instalasi Python)[cite: 2].
2. Klik 2x pada file `INSTALL.bat`. [cite_start]Script ini akan otomatis menginstal library `playwright` dan mengunduh *browser* Chromium[cite: 2].
3. [cite_start]Tunggu hingga muncul tulisan "Semua siap!" di terminal[cite: 3].

---

## ✍️ Langkah 2: Membuat & Memasang Tanda Tangan
Kamu harus merekam tanda tanganmu sendiri agar bot bisa menirunya.
1. Jalankan *file* `absen.py` menggunakan Python.
2. Gambar tanda tanganmu di kotak putih yang disediakan.
3. Klik tombol **"⚙️ Buat Kode"** lalu *copy* seluruh teks koordinat yang muncul (dimulai dari tulisan `stroke1 = [ ... ]`).
4. **(Opsional)** Jika kamu ragu dengan hasilnya, buka file `hasil.py`, timpa kordinat `stroke1` di dalamnya dengan kodemu, lalu jalankan untuk melihat *preview* animasinya.
5. Buka *file* `absensi_bot.py` menggunakan Notepad atau *code editor*.
6. Gunakan fitur pencarian (Ctrl+F) dan cari tulisan `stroke1 =`.
7. **Paste (timpa)** koordinat bawaan dengan koordinat tanda tangan aslimu yang sudah di-*copy* tadi. Simpan *file* (Ctrl+S).

---

## ▶️ Langkah 3: Menjalankan Bot
1. [cite_start]Klik 2x pada *file* `JALANKAN.bat`[cite: 4].
2. Masukkan **NIM** dan **Password** SIAKAD kamu pada aplikasi bot.
3. Klik tombol **"▶ Mulai Otomatis"**.
4. **Perhatikan Cloudflare:** Bot akan membuka Chrome asli dan mencoba melewati Cloudflare. Jika bot gagal melakukan centang otomatis "Verify you are human", silakan bantu klik manual 1x pada layar.
5. **Set-and-Forget:** Setelah berhasil login, bot akan otomatis masuk ke menu **E-learning > Absensi**, mencari semua absensi yang berwarna merah, menandatanganinya dengan tanda tangan aslimu, dan me-*refresh* tabel otomatis.

---

## ⚠️ Catatan Keamanan & Penggunaan
* **Persistent Profile:** Bot ini menggunakan profil Chrome asli. Setelah login pertama berhasil, *cookies* akan tersimpan. Saat menjalankan bot di lain waktu, Cloudflare biasanya tidak akan menanyakan verifikasi ulang.
* **Keamanan Data:** Informasi NIM dan Password hanya digunakan secara lokal saat bot berjalan dan tidak dikirim ke pihak ketiga mana pun.
* **Bot Terdeteksi?:** Bot ini sudah menggunakan argumen `--disable-blink-features=AutomationControlled` dan mengabaikan argumen `--enable-automation` bawaan Playwright agar Cloudflare tidak mengenali aktivitas ini sebagai robot.

---

## 👨‍💻 Developer
* **Nama:** Mohamad Bagus Jiran Riskohar
* **Prodi:** Informatika - STT Ronggolawe
* **Versi:** 4.0.0 (Stealth Edition)
