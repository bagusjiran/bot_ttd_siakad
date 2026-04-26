# SIAKAD KPT — Auto Absensi Bot v2

> Ditulis ulang berdasarkan analisis video rekaman langsung.

---

## Perbaikan dari versi sebelumnya

| Masalah v1 | Solusi v2 |
|---|---|
| Pakai `page.goto()` ke URL berbeda | Klik sidebar link (SPA-aware) |
| Navigasi halaman = balik ke home | Semua di halaman yang sama, no navigate |
| Signature generic/acak | Signature "JR" sesuai aslinya |
| Deteksi tombol merah kurang tepat | Deteksi via computed CSS color dari dalam tabel |

---

## Instalasi

### Windows
1. Pastikan **Python 3.10+** sudah terinstall
2. Klik 2x **`INSTALL.bat`**
3. Klik 2x **`JALANKAN.bat`**

### Linux / Mac
```bash
pip3 install playwright
playwright install chromium
python3 absensi_bot.py
```

---

## Cara Penggunaan

1. Jalankan bot
2. Isi **NIM** (default: 24550011) dan **Password**
3. Klik **▶ Mulai Bot**
4. Browser Chrome akan terbuka — **jangan tutup!**
5. Pantau progress di log panel

---

## Alur Kerja Bot (sesuai video)

```
Buka browser
    ↓
Login (jika belum)
    ↓
Klik "Absensi" di sidebar
    ↓
Tunggu tabel selesai loading
    ↓
Scan semua tombol MERAH di tabel
    ↓
Untuk setiap tombol merah:
  Klik → Canvas muncul di atas tabel
  Gambar tanda tangan "JR"
  Klik Simpan
  Tunggu tabel reload
    ↓
Ulangi scan sampai tidak ada merah
    ↓
Selesai!
```

---

## Catatan

- **URL tidak berubah** — website pakai SPA dengan AJAX, selalu di `home#`
- Tanda tangan mengikuti style "JR" (inisial Jiran Riskohar) dari video
- Bot scan ulang setelah setiap selesai, untuk antisipasi tombol baru yang terbuka
