import asyncio
import math
import os
import sys
import threading
import time
import tkinter as tk
from tkinter import scrolledtext, messagebox

# --- MEMBUNGKAM WARNING NODE.JS ---
os.environ["NODE_NO_WARNINGS"] = "1"

# ── Konstanta ──────────────────────────────────────────────────────────────
SITE_URL  = "https://stt-ronggolawe.ac.id/siakpt/login"

# ── Warna GUI ──────────────────────────────────────────────────────────────
BG      = "#0d1117"
SURFACE = "#161b22"
CARD    = "#21262d"
BORDER  = "#30363d"
ACCENT  = "#58a6ff"
SUCCESS = "#3fb950"
DANGER  = "#f85149"
WARNING = "#e3b341"
TEXT    = "#c9d1d9"
SUBTEXT = "#8b949e"
FMN     = ("Consolas", 10)
FML     = ("Consolas", 9)

# ═══════════════════════════════════════════════════════════════════════════
#  BOT FULL OTOMATIS (STEALTH V4)
# ═══════════════════════════════════════════════════════════════════════════

class SiakadBot:
    def __init__(self, log_fn, status_fn, stop_event: threading.Event, nim: str, pwd: str):
        self.log        = log_fn
        self.set_status = status_fn
        self.stop       = stop_event
        self.nim        = nim
        self.pwd        = pwd

    # ── Tunggu Cloudflare ──────────────────────────────────────────────────
    async def _wait_cloudflare(self, page):
        self.log("🛡️ Mengecek verifikasi keamanan Cloudflare...")
        for i in range(45): 
            if self.stop.is_set(): return False
            try:
                title = await page.title()
                if "Just a moment" in title or "Cloudflare" in title:
                    
                    # --- FITUR AUTO-CLICK CLOUDFLARE ---
                    if i % 2 == 0: 
                        try:
                            for frame in page.frames:
                                if "challenges.cloudflare.com" in frame.url or "turnstile" in frame.url:
                                    chk = frame.locator('input[type="checkbox"], .ctp-checkbox-label, label').first
                                    if await chk.is_visible(timeout=500):
                                        self.log("🤖 Mencoba centang otomatis Cloudflare...")
                                        box = await chk.bounding_box()
                                        if box:
                                            target_x = box["x"] + box["width"] / 2
                                            target_y = box["y"] + box["height"] / 2
                                            await page.mouse.move(target_x, target_y, steps=15)
                                            await asyncio.sleep(0.2)
                                            await page.mouse.click(target_x, target_y)
                                            await asyncio.sleep(1)
                        except:
                            pass 
                            
                    if i == 5:
                        self.log("⚠ PERHATIAN: Jika bot gagal centang otomatis, mohon BANTU KLIK MANUAL 1x!")

                    await asyncio.sleep(2)
                else:
                    self.log("✅ Cloudflare berhasil dilewati!")
                    return True
            except Exception as e:
                if "Execution context was destroyed" in str(e) or "Target closed" in str(e):
                    self.log("🔄 Halaman sedang dialihkan (Cloudflare lolos!)...")
                    await asyncio.sleep(3) 
                    return True
                else:
                    await asyncio.sleep(2)
                    
        self.log("⚠ Waktu tunggu Cloudflare habis, mencoba lanjut...")
        return True

    # ── Login Otomatis ─────────────────────────────────────────────────────
    async def _handle_login(self, page):
        self.log("🔐 Mengisi form login otomatis...")
        try:
            inputs = await page.query_selector_all('input')
            user_input = None
            for inp in inputs:
                t = await inp.get_attribute("type")
                if t in ["text", "number"] or not t:
                    user_input = inp
                    break
            
            pwd_input = await page.query_selector('input[type="password"]')
            
            if user_input and pwd_input:
                await user_input.fill(self.nim)
                await pwd_input.fill(self.pwd)
                await asyncio.sleep(0.5)
                
                login_btn = await page.query_selector('button:has-text("Login"), input[value="Login"]')
                if login_btn:
                    await login_btn.click()
                    self.log("⏳ Menunggu masuk ke Dashboard...")
                    await asyncio.sleep(3)
                    return True
            self.log("❌ Form login tidak ditemukan! (Mungkin sudah login)")
            return False
        except Exception as e:
            self.log(f"❌ Error saat login: {e}")
            return False

    # ── Navigasi ke E-learning -> Absensi ──────────────────────────────────
    async def _goto_absensi(self, page):
        self.log("📂 Navigasi otomatis ke sidebar menu...")
        try:
            await asyncio.sleep(2)
            
            if "absensi" in page.url.lower():
                self.log("✅ Sudah berada di halaman Absensi.")
                return True

            elearning = page.locator('text="E-learning"').first
            await elearning.wait_for(state="visible", timeout=10000)
            self.log("   ➤ Klik E-learning")
            await elearning.click()
            await asyncio.sleep(1.5) 
            
            absensi = page.locator('text="Absensi"').last
            await absensi.wait_for(state="visible", timeout=5000)
            self.log("   ➤ Klik Absensi")
            await absensi.click()
            await asyncio.sleep(3)
            self.log("✅ Berhasil masuk ke halaman Absensi.")
            return True
        except Exception as e:
            self.log(f"❌ Gagal navigasi sidebar: {e}")
            return False

    # ── Tunggu tabel selesai load ──────────────────────────────────────────
    async def _wait_table(self, page, timeout=30):
        deadline = time.time() + timeout
        while time.time() < deadline:
            proc_visible = await page.evaluate("""
                () => {
                    const el = document.querySelector('.dataTables_processing');
                    if (!el) return false;
                    const s = window.getComputedStyle(el);
                    return s.display !== 'none' && s.visibility !== 'hidden' && s.opacity !== '0';
                }
            """)
            if not proc_visible: break
            await asyncio.sleep(0.4)
        await asyncio.sleep(0.3)

    # ── Tunggu canvas muncul ───────────────────────────────────────────────
    async def _wait_canvas(self, page, timeout=8) -> bool:
        deadline = time.time() + timeout
        while time.time() < deadline:
            canvas = await page.query_selector("canvas")
            if canvas:
                box = await canvas.bounding_box()
                if box and box["width"] > 100: return True
            await asyncio.sleep(0.3)
        return False

    # ── Gambar Tanda Tangan Presisi (Sesuai Kordinatmu) ────────────────────
    async def _draw_signature(self, page) -> bool:
        canvas = await page.query_selector("canvas")
        if not canvas: return False
        box = await canvas.bounding_box()
        if not box or box["width"] < 50: return False

        w, h, ox, oy = box["width"], box["height"], box["x"], box["y"]
        def p(xr, yr): return (ox + w * xr, oy + h * yr)

        async def stroke(pts):
            if not pts: return
            await page.mouse.move(pts[0][0], pts[0][1])
            await page.mouse.down()
            for px, py in pts[1:]:
                await page.mouse.move(px, py, steps=8)
                await asyncio.sleep(0.005)
            await page.mouse.up()
            await asyncio.sleep(0.07)

        stroke1 = [
            p(0.342, 0.368), p(0.348, 0.348), p(0.356, 0.324), p(0.362, 0.300),
            p(0.368, 0.280), p(0.372, 0.260), p(0.376, 0.240), p(0.380, 0.220),
            p(0.384, 0.200), p(0.388, 0.180), p(0.392, 0.160), p(0.398, 0.180),
            p(0.402, 0.204), p(0.404, 0.228), p(0.406, 0.260), p(0.408, 0.288),
            p(0.408, 0.312), p(0.410, 0.332), p(0.410, 0.356), p(0.410, 0.380),
            p(0.412, 0.404), p(0.412, 0.428), p(0.414, 0.448), p(0.412, 0.468),
            p(0.410, 0.488), p(0.408, 0.508), p(0.406, 0.528), p(0.402, 0.548),
            p(0.394, 0.564), p(0.386, 0.584), p(0.374, 0.600), p(0.364, 0.612),
            p(0.354, 0.616), p(0.344, 0.612), p(0.334, 0.600), p(0.328, 0.580),
            p(0.326, 0.560), p(0.328, 0.536), p(0.332, 0.516), p(0.338, 0.496),
            p(0.344, 0.472), p(0.352, 0.452), p(0.358, 0.432), p(0.364, 0.412),
            p(0.372, 0.396), p(0.378, 0.376), p(0.384, 0.356), p(0.392, 0.336),
            p(0.398, 0.316), p(0.408, 0.288), p(0.414, 0.268), p(0.418, 0.248),
            p(0.424, 0.228), p(0.428, 0.208), p(0.434, 0.188), p(0.438, 0.168),
            p(0.442, 0.148), p(0.446, 0.128), p(0.454, 0.148), p(0.458, 0.168),
            p(0.462, 0.192), p(0.464, 0.212), p(0.466, 0.232), p(0.468, 0.252),
            p(0.470, 0.272), p(0.472, 0.300), p(0.472, 0.324), p(0.474, 0.344),
            p(0.474, 0.372), p(0.474, 0.396), p(0.474, 0.420), p(0.476, 0.440),
            p(0.476, 0.468), p(0.478, 0.488), p(0.480, 0.508), p(0.480, 0.532),
            p(0.480, 0.504), p(0.478, 0.484), p(0.476, 0.464), p(0.476, 0.436),
            p(0.472, 0.416), p(0.472, 0.392), p(0.470, 0.372), p(0.466, 0.352),
            p(0.466, 0.328), p(0.464, 0.304), p(0.462, 0.284), p(0.462, 0.260),
            p(0.462, 0.232), p(0.464, 0.208), p(0.466, 0.188), p(0.472, 0.168),
            p(0.482, 0.156), p(0.492, 0.140), p(0.504, 0.132), p(0.514, 0.128),
            p(0.526, 0.124), p(0.538, 0.128), p(0.548, 0.136), p(0.558, 0.148),
            p(0.566, 0.164), p(0.574, 0.180), p(0.576, 0.200), p(0.576, 0.224),
            p(0.572, 0.248), p(0.566, 0.268), p(0.560, 0.288), p(0.550, 0.308),
            p(0.542, 0.324), p(0.532, 0.340), p(0.522, 0.356), p(0.512, 0.364),
            p(0.502, 0.368), p(0.492, 0.376), p(0.482, 0.380), p(0.490, 0.396),
            p(0.498, 0.416), p(0.508, 0.432), p(0.516, 0.448), p(0.526, 0.460),
            p(0.534, 0.476), p(0.544, 0.496), p(0.554, 0.512), p(0.564, 0.524),
            p(0.572, 0.540), p(0.582, 0.552)
        ]

        await stroke(stroke1)
        await asyncio.sleep(0.1)
        self.log("✏  Tanda tangan digambar.")
        return True

    # ── Refresh Tabel Otomatis ─────────────────────────────────────────────
    async def _refresh_via_dropdown(self, page):
        self.log("🔄 Merefresh tabel...")
        try:
            js_script = """
                (targetText) => {
                    let success = false;
                    const selects = document.querySelectorAll('select');
                    for (let sel of selects) {
                        if (sel.innerText.includes('Semester Genap') && sel.innerText.includes('Semester Gasal')) {
                            let opt = Array.from(sel.options).find(o => o.text.includes(targetText));
                            if (opt) {
                                sel.value = opt.value;
                                sel.dispatchEvent(new Event('change', { bubbles: true }));
                                if (window.jQuery) window.jQuery(sel).trigger('change');
                                success = true;
                            }
                        }
                    }
                    return success;
                }
            """
            
            await page.evaluate(js_script, 'Semester Gasal')
            await asyncio.sleep(1.5)
            await self._wait_table(page, timeout=10)

            await page.evaluate(js_script, 'Semester Genap')
            await asyncio.sleep(1.5)
            await self._wait_table(page, timeout=10)
        except Exception as e:
            self.log("⚠ Gagal refresh dropdown, abaikan.")

    # ── Loop Tanda Tangan ──────────────────────────────────────────────────
    async def _run_loop(self, page):
        signed = skipped = rnd = 0

        while not self.stop.is_set():
            rnd += 1
            self.log(f"\n🔍  Scan putaran {rnd}...")
            await self._wait_table(page)

            buttons = await page.evaluate("""
                () => {
                    const items = [];
                    const tds = document.querySelectorAll('table tbody td');
                    for (const td of tds) {
                        const els = td.querySelectorAll('a, button, span, div');
                        for (const el of els) {
                            const bg = window.getComputedStyle(el).backgroundColor;
                            const cls = (el.className || '');
                            if (bg.includes('220, 53, 69') || bg.includes('255, 0, 0') || cls.includes('danger')) {
                                const rect = el.getBoundingClientRect();
                                if (el.innerText.trim() && rect.width > 0) {
                                    items.push({text: el.innerText.trim(), x: rect.left + rect.width/2 + window.scrollX, y: rect.top + rect.height/2 + window.scrollY});
                                }
                            }
                        }
                    }
                    return items;
                }
            """)

            if not buttons:
                self.log("ℹ  Tidak ada tombol merah tersisa.")
                break

            self.log(f"🔴  Ditemukan {len(buttons)} absensi tertunda.")
            for i, btn in enumerate(buttons, 1):
                if self.stop.is_set(): break
                label = f"Pertemuan {btn['text']}"
                self.log(f"▶  Klik {label}...")
                
                await page.evaluate(f"window.scrollTo(0, {max(0, btn['y'] - 300)})")
                await asyncio.sleep(0.3)
                await page.mouse.click(btn["x"], btn["y"])
                await asyncio.sleep(0.8)

                if not await self._wait_canvas(page):
                    skipped += 1
                    continue

                await page.evaluate("window.scrollTo(0, 0)")
                if await self._draw_signature(page):
                    simpan = await page.query_selector('button:has-text("Simpan"), input[value="Simpan"]')
                    if simpan:
                        self.log(f"💾  Menyimpan {label}...")
                        await simpan.click()
                        await asyncio.sleep(1.5)
                        await self._refresh_via_dropdown(page)
                        self.log(f"✅  {label} Berhasil!")
                        signed += 1
                    else: skipped += 1
                else: skipped += 1
                await asyncio.sleep(1)

        return signed, skipped

    # ── Main Eksekusi ──────────────────────────────────────────────────────
    async def run(self):
        from playwright.async_api import async_playwright
        self.set_status("running")

        async with async_playwright() as p:
            self.log("🌐 Membuka Browser Chrome dengan profil persisten...")
            
            user_data_dir = os.path.join(os.getcwd(), "chrome_bot_profile")
            
            try:
                # PERBAIKAN FATAL: Stealth Mode Bypass Cloudflare
                context = await p.chromium.launch_persistent_context(
                    user_data_dir=user_data_dir,
                    channel="chrome", 
                    headless=False,
                    no_viewport=True, 
                    ignore_default_args=["--enable-automation", "--no-sandbox"], 
                    args=[
                        "--disable-blink-features=AutomationControlled", 
                        "--start-maximized"
                    ]
                )
                
                page = context.pages[0] if len(context.pages) > 0 else await context.new_page()
                
                self.log(f"🔗 Menuju ke {SITE_URL}")
                await page.goto(SITE_URL, wait_until="domcontentloaded", timeout=60000)
                
                # 1. Tunggu Cloudflare
                await self._wait_cloudflare(page)
                
                # Pengecekan form login
                try:
                    await page.wait_for_selector('input[type="password"]', timeout=15000)
                    
                    # 2. Login
                    login_ok = await self._handle_login(page)
                    if not login_ok:
                        self.set_status("error")
                        return
                except:
                    self.log("✅ Tidak mendeteksi form login, menganggap sudah masuk...")

                # 3. Navigasi Sidebar E-Learning -> Absensi
                nav_ok = await self._goto_absensi(page)
                if not nav_ok:
                    self.set_status("error")
                    return

                # 4. Tanda Tangan
                signed, skipped = await self._run_loop(page)

                self.log("\n" + "═" * 50)
                self.log(f"  🎉  SELESAI FULL OTOMATIS!")
                self.log(f"  ✅  Berhasil ditandatangani : {signed}")
                self.log(f"  ⏭  Gagal / dilewati        : {skipped}")
                self.log("═" * 50)
                self.set_status("done")

            except Exception as e:
                self.log(f"\n💥 ERROR: {e}")
                self.set_status("error")
            finally:
                if 'context' in locals():
                    await asyncio.sleep(2)
                    await context.close()

# ═══════════════════════════════════════════════════════════════════════════
#  GUI (VERSI V4 UPDATED)
# ═══════════════════════════════════════════════════════════════════════════

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SIAKAD KPT — Full Auto Absensi v4 (Stealth Mode)")
        self.configure(bg=BG)
        self.resizable(False, False)
        self._stop_event = threading.Event()
        self._thread = None
        self._build_ui()
        self._center()

    def _build_ui(self):
        hdr = tk.Frame(self, bg=SURFACE, padx=20, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text="⚡", bg=SURFACE, fg=WARNING, font=("Consolas", 20)).pack(side="left")
        tk.Label(hdr, text=" SIAKAD KPT", bg=SURFACE, fg=ACCENT, font=("Consolas", 18, "bold")).pack(side="left")
        tk.Label(hdr, text="  Full Auto v4", bg=SURFACE, fg=SUBTEXT, font=("Consolas", 12)).pack(side="left")
        self._dot = tk.Label(hdr, text="●", bg=SURFACE, fg=SUBTEXT, font=("Consolas", 15))
        self._dot.pack(side="right")
        self._slbl = tk.Label(hdr, text="Siap", bg=SURFACE, fg=SUBTEXT, font=FMN)
        self._slbl.pack(side="right", padx=(0, 6))

        # --- FRAME LOGIN ---
        login_frame = tk.Frame(self, bg=CARD, padx=20, pady=15)
        login_frame.pack(fill="x", padx=14, pady=12)
        
        tk.Label(login_frame, text="AKUN SIAKAD", bg=CARD, fg=ACCENT, font=("Consolas", 9, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        tk.Label(login_frame, text="NIM      :", bg=CARD, fg=TEXT, font=FMN).grid(row=1, column=0, sticky="w")
        self.nim_entry = tk.Entry(login_frame, font=FMN, bg=SURFACE, fg=TEXT, insertbackground=TEXT, width=30)
        self.nim_entry.grid(row=1, column=1, padx=10, pady=5)
        self.nim_entry.insert(0, "24550011") 

        tk.Label(login_frame, text="Password :", bg=CARD, fg=TEXT, font=FMN).grid(row=2, column=0, sticky="w")
        self.pwd_entry = tk.Entry(login_frame, font=FMN, bg=SURFACE, fg=TEXT, insertbackground=TEXT, show="*", width=30)
        self.pwd_entry.grid(row=2, column=1, padx=10, pady=5)

        # --- TOMBOL AKSI ---
        btns = tk.Frame(self, bg=BG, padx=14, pady=5)
        btns.pack(fill="x")

        self._btn_run = tk.Button(
            btns, text="▶  Mulai Otomatis", command=self._start_bot,
            bg=SUCCESS, fg=BG, activebackground="#2ea043", relief="flat",
            font=("Consolas", 11, "bold"), padx=18, pady=9, cursor="hand2"
        )
        self._btn_run.pack(side="left")

        self._btn_stop = tk.Button(
            btns, text="■  Stop", command=self._do_stop,
            bg=DANGER, fg=BG, activebackground="#da3633", relief="flat",
            font=("Consolas", 11, "bold"), padx=18, pady=9, cursor="hand2", state="disabled"
        )
        self._btn_stop.pack(side="left", padx=10)

        tk.Button(btns, text="🗑", command=self._clear, bg=SURFACE, fg=SUBTEXT, relief="flat", font=("Consolas", 12), padx=10, pady=9, cursor="hand2").pack(side="right")

        # --- LOG ---
        lf = tk.Frame(self, bg=BG, padx=0, pady=0)
        lf.pack(fill="both", expand=True)
        tk.Label(lf, text=" ● LOG PROSES ", bg=SURFACE, fg=SUBTEXT, font=("Consolas", 8, "bold"), anchor="w").pack(fill="x")

        self._log = scrolledtext.ScrolledText(lf, width=74, height=15, bg=SURFACE, fg=TEXT, insertbackground=ACCENT, relief="flat", font=FML, state="disabled", padx=12, pady=8)
        self._log.pack(fill="both", expand=True)

        for tag, col in [("ok", SUCCESS), ("err", DANGER), ("warn", WARNING), ("info", ACCENT), ("dim", SUBTEXT)]:
            self._log.tag_config(tag, foreground=col)

    def _center(self):
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        w, h = self.winfo_width(), self.winfo_height()
        self.geometry(f"+{(sw-w)//2}+{(sh-h)//2}")

    def _write_log(self, msg: str):
        m = msg.lower()
        tag = "ok" if any(k in m for k in ["✅","berhasil","selesai","🎉"]) else \
              "err" if any(k in m for k in ["❌","💥","error","gagal"]) else \
              "warn" if any(k in m for k in ["⚠","habis"]) else \
              "info" if any(k in m for k in ["🔍","🌐","🔗","💾","🔴","ℹ","✏","📄","📋","🟢","🔄","⏳","🔐","📂","▶","🤖"]) else \
              "dim" if "═" in msg else None

        ts = time.strftime("%H:%M:%S")
        self._log.config(state="normal")
        self._log.insert("end", f"[{ts}] {msg}\n", tag or "")
        self._log.see("end")
        self._log.config(state="disabled")

    def _set_status(self, s: str):
        MAP = {"running": (WARNING, "Berjalan..."), "done": (SUCCESS, "Selesai ✓"), "error": (DANGER, "Error ✗"), "idle": (SUBTEXT, "Siap")}
        c, t = MAP.get(s, (SUBTEXT, s))
        def _up():
            self._dot.config(fg=c)
            self._slbl.config(fg=c, text=t)
            if s in ("done", "error", "idle"):
                self._btn_run.config(state="normal")
                self._btn_stop.config(state="disabled")
        self.after(0, _up)

    def _clear(self):
        self._log.config(state="normal")
        self._log.delete("1.0", "end")
        self._log.config(state="disabled")

    def _start_bot(self):
        nim = self.nim_entry.get().strip()
        pwd = self.pwd_entry.get().strip()

        if not nim or not pwd:
            messagebox.showwarning("Peringatan", "Mohon isi NIM dan Password terlebih dahulu!")
            return

        self._stop_event.clear()
        self._btn_run.config(state="disabled")
        self._btn_stop.config(state="normal")
        self._set_status("running")
        
        self._write_log("\n" + "═" * 50)
        self._write_log(f"  ⚡ Memulai Otomasi — {time.strftime('%H:%M:%S')}")
        self._write_log("═" * 50)

        bot = SiakadBot(
            log_fn=lambda m: self.after(0, self._write_log, m),
            status_fn=self._set_status,
            stop_event=self._stop_event,
            nim=nim,
            pwd=pwd
        )

        def _worker():
            asyncio.run(bot.run())
            if not self._stop_event.is_set():
                self.after(0, self._set_status, "idle")

        self._thread = threading.Thread(target=_worker, daemon=True)
        self._thread.start()

    def _do_stop(self):
        self._stop_event.set()
        self._write_log("🛑 Dihentikan oleh pengguna.")
        self._btn_stop.config(state="disabled")
        self._set_status("idle")

if __name__ == "__main__":
    app = App()
    app.mainloop()
