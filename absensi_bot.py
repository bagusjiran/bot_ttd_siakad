import asyncio
import math
import os
import subprocess
import sys
import threading
import time
import tkinter as tk
from tkinter import scrolledtext, messagebox

# --- MEMBUNGKAM WARNING NODE.JS ---
os.environ["NODE_NO_WARNINGS"] = "1"

# ── Konstanta ──────────────────────────────────────────────────────────────
CDP_PORT  = 9222
SITE_URL  = "https://stt-ronggolawe.ac.id/siakpt/home"

# Lokasi Chrome yang umum di Windows
CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",  # Edge fallback
]

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
#  CARI CHROME
# ═══════════════════════════════════════════════════════════════════════════

def find_chrome() -> str | None:
    for p in CHROME_PATHS:
        if os.path.exists(p):
            return p
    return None


# ═══════════════════════════════════════════════════════════════════════════
#  BOT — nyambung ke Chrome yang sudah dibuka user
# ═══════════════════════════════════════════════════════════════════════════

class SiakadBot:
    def __init__(self, log_fn, status_fn, stop_event: threading.Event):
        self.log        = log_fn
        self.set_status = status_fn
        self.stop       = stop_event

    # ── Tunggu tabel selesai load ──────────────────────────────────────────
    async def _wait_table(self, page, timeout=30):
        deadline = time.time() + timeout
        while time.time() < deadline:
            proc_visible = await page.evaluate("""
                () => {
                    const el = document.querySelector('.dataTables_processing');
                    if (!el) return false;
                    const s = window.getComputedStyle(el);
                    return s.display !== 'none' && s.visibility !== 'hidden'
                        && s.opacity !== '0';
                }
            """)
            if not proc_visible:
                break
            await asyncio.sleep(0.4)
        await asyncio.sleep(0.3)

    # ── Tunggu canvas muncul ───────────────────────────────────────────────
    async def _wait_canvas(self, page, timeout=8) -> bool:
        deadline = time.time() + timeout
        while time.time() < deadline:
            canvas = await page.query_selector("canvas")
            if canvas:
                box = await canvas.bounding_box()
                if box and box["width"] > 100:
                    return True
            await asyncio.sleep(0.3)
        return False

    # ── Gambar tanda tangan sesuai koordinat aslimu ────────────────────────
    async def _draw_signature(self, page) -> bool:
        canvas = await page.query_selector("canvas")
        if not canvas:
            self.log("⚠  Canvas tidak ditemukan!")
            return False

        box = await canvas.bounding_box()
        if not box or box["width"] < 50:
            self.log("⚠  Canvas tidak valid.")
            return False

        w, h  = box["width"], box["height"]
        ox    = box["x"]
        oy    = box["y"]

        # Fungsi penempatan rasio relatif terhadap ukuran canvas
        def p(xr, yr):
            return (ox + w * xr, oy + h * yr)

        async def stroke(pts):
            if not pts: return
            await page.mouse.move(pts[0][0], pts[0][1])
            await page.mouse.down()
            for px, py in pts[1:]:
                # Menggambar garis dengan mulus
                await page.mouse.move(px, py, steps=8)
                await asyncio.sleep(0.005)
            await page.mouse.up()
            await asyncio.sleep(0.07)

        # Koordinat asli dari hasil rekamanmu
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

        self.log("✏  Tanda tangan aslimu selesai digambar.")
        return True

    # ── Trik Pindah Semester (Bypass Kesalahan Web SIAKAD) ────────────────
    async def _refresh_via_dropdown(self, page):
        self.log("🔄 Merefresh tabel (Trik Pindah Semester Gasal -> Genap)...")
        try:
            # Script JS ini sangat sakti untuk membypass klik UI Select2 yang sering meleset
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
            
            # 1. Pindah ke Semester Gasal
            ok = await page.evaluate(js_script, 'Semester Gasal')
            if not ok:
                await page.locator('.select2-selection, select, span, div').filter(has_text="Semester Genap").last.click()
                await asyncio.sleep(0.5)
                await page.locator('li, option').filter(has_text="Semester Gasal").last.click()

            await asyncio.sleep(1.5)
            await self._wait_table(page, timeout=10)

            # 2. Kembalikan lagi ke Semester Genap
            ok = await page.evaluate(js_script, 'Semester Genap')
            if not ok:
                await page.locator('.select2-selection, select, span, div').filter(has_text="Semester Gasal").last.click()
                await asyncio.sleep(0.5)
                await page.locator('li, option').filter(has_text="Semester Genap").last.click()

            await asyncio.sleep(1.5)
            await self._wait_table(page, timeout=10)
            self.log("✅ Refresh tabel berhasil.")

        except Exception as e:
            self.log(f"⚠ Trik refresh gagal, mencoba reload halaman... {str(e)[:30]}")
            await page.reload()
            await self._wait_table(page, timeout=10)

    # ── Ambil semua tombol merah dari tabel ───────────────────────────────
    async def _get_red_buttons(self, page) -> list:
        return await page.evaluate("""
            () => {
                const RED_COLORS = new Set([
                    'rgb(220, 53, 69)', 'rgb(217, 83, 79)', 'rgb(220, 38, 38)',
                    'rgb(239, 68, 68)', 'rgb(248, 113, 113)', 'rgb(185, 28, 28)',
                    'rgb(255, 0, 0)', 'rgb(200, 35, 51)'
                ]);

                const items = [];
                const tds = document.querySelectorAll(
                    'table tbody td, .dataTables_wrapper td'
                );

                for (const td of tds) {
                    const els = td.querySelectorAll('a, button, span, div');
                    for (const el of els) {
                        const st  = window.getComputedStyle(el);
                        const bg  = st.backgroundColor;
                        const cls = (el.className || '').toString();
                        const isRed = RED_COLORS.has(bg) ||
                                      cls.includes('btn-danger') ||
                                      cls.includes('danger');
                        if (!isRed) continue;

                        const text = el.innerText.trim();
                        const rect = el.getBoundingClientRect();
                        if (!text || rect.width === 0) continue;

                        items.push({
                            text,
                            bg,
                            x: rect.left + rect.width  / 2 + window.scrollX,
                            y: rect.top  + rect.height / 2 + window.scrollY,
                        });
                    }
                }
                return items;
            }
        """)

    # ── Proses satu pertemuan ─────────────────────────────────────────────
    async def _sign_one(self, page, btn: dict, idx: int) -> bool:
        label = f"Pertemuan {btn['text']}"
        self.log(f"🔴  [{idx}] Klik {label}...")

        await page.evaluate(f"window.scrollTo(0, {max(0, btn['y'] - 300)})")
        await asyncio.sleep(0.3)

        pos = await page.evaluate(f"""
            () => {{
                const els = document.querySelectorAll('table tbody td a, table tbody td button, table tbody td span');
                for (const el of els) {{
                    const st = window.getComputedStyle(el);
                    const RED_COLORS = new Set(['rgb(220, 53, 69)','rgb(217, 83, 79)','rgb(220, 38, 38)','rgb(239, 68, 68)','rgb(248, 113, 113)','rgb(185, 28, 28)','rgb(255, 0, 0)','rgb(200, 35, 51)']);
                    const cls = (el.className||'').toString();
                    if ((RED_COLORS.has(st.backgroundColor)||cls.includes('btn-danger')) && el.innerText.trim() === '{btn['text']}') {{
                        el.scrollIntoView({{block:'center'}});
                        const r = el.getBoundingClientRect();
                        return {{ x: r.left + r.width/2, y: r.top + r.height/2 }};
                    }}
                }}
                return null;
            }}
        """)

        if pos:
            await page.mouse.click(pos["x"], pos["y"])
        else:
            self.log(f"⚠  Tombol {label} tidak ditemukan lagi.")
            return False

        await asyncio.sleep(0.8)

        ok = await self._wait_canvas(page)
        if not ok:
            self.log(f"⚠  Canvas tidak muncul untuk {label}, skip.")
            return False

        await page.evaluate("window.scrollTo(0, 0)")
        await asyncio.sleep(0.3)

        drawn = await self._draw_signature(page)
        if not drawn: return False

        await asyncio.sleep(0.5)

        simpan = await page.query_selector(
            'button:text-matches("simpan", "i"), '
            'input[value="Simpan"], '
            'button[type="submit"]'
        )
        if not simpan:
            self.log(f"⚠  Tombol Simpan tidak ada!")
            return False

        self.log(f"💾  Simpan {label}...")
        await simpan.click()
        await asyncio.sleep(1.5)

        # TRIK REFRESH SEMESTER
        await self._refresh_via_dropdown(page)

        self.log(f"✅  {label} berhasil!")
        return True

    # ── Loop utama ────────────────────────────────────────────────────────
    async def _run_loop(self, page) -> tuple[int, int]:
        signed = skipped = rnd = 0

        while not self.stop.is_set():
            rnd += 1
            self.log(f"\n🔍  Scan putaran {rnd}...")
            await self._wait_table(page)

            buttons = await self._get_red_buttons(page)
            if not buttons:
                self.log("ℹ  Tidak ada tombol merah tersisa.")
                break

            self.log(f"🔴  Ditemukan {len(buttons)} tombol merah:")
            for i, b in enumerate(buttons, 1):
                self.log(f"    [{i}] Pertemuan {b['text']}")

            for i, btn in enumerate(buttons, 1):
                if self.stop.is_set():
                    break
                ok = await self._sign_one(page, btn, i)
                (signed if ok else skipped).__class__  # dummy
                if ok:
                    signed += 1
                else:
                    skipped += 1
                
                await asyncio.sleep(1)

        return signed, skipped

    # ── Entry point ───────────────────────────────────────────────────────
    async def run(self):
        from playwright.async_api import async_playwright

        self.set_status("running")
        self.log("🔗  Mencoba nyambung ke Chrome...")

        async with async_playwright() as p:
            try:
                browser = await p.chromium.connect_over_cdp(
                    f"http://127.0.0.1:{CDP_PORT}"
                )
            except Exception as e:
                self.log(f"❌  Gagal nyambung: {e}")
                self.set_status("error")
                return

            self.log("✅  Berhasil nyambung ke Chrome!")

            contexts = browser.contexts
            if not contexts: return
            pages = contexts[0].pages
            if not pages: return

            page = None
            for pg in pages:
                if "siakpt" in pg.url or "ronggolawe" in pg.url:
                    page = pg
                    break
            if not page: page = pages[0]

            self.log(f"📄  Tab aktif: {page.url}")

            try:
                signed, skipped = await self._run_loop(page)
                self.log("\n" + "═" * 50)
                self.log(f"  🎉  SELESAI!")
                self.log(f"  ✅  Berhasil : {signed} pertemuan")
                self.log(f"  ⏭  Dilewati : {skipped} pertemuan")
                self.log("═" * 50)
                self.set_status("done")

            except Exception as e:
                self.log(f"\n💥  ERROR: {e}")
                self.set_status("error")


# ═══════════════════════════════════════════════════════════════════════════
#  GUI
# ═══════════════════════════════════════════════════════════════════════════

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SIAKAD KPT — Auto Absensi v3")
        self.configure(bg=BG)
        self.resizable(False, False)

        self._stop_event   = threading.Event()
        self._chrome_proc  = None
        self._thread       = None

        self._build_ui()
        self._center()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_ui(self):
        hdr = tk.Frame(self, bg=SURFACE, padx=20, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text="⚡", bg=SURFACE, fg=WARNING, font=("Consolas", 20)).pack(side="left")
        tk.Label(hdr, text=" SIAKAD KPT", bg=SURFACE, fg=ACCENT, font=("Consolas", 18, "bold")).pack(side="left")
        tk.Label(hdr, text="  Auto Absensi v3", bg=SURFACE, fg=SUBTEXT, font=("Consolas", 12)).pack(side="left")
        self._dot  = tk.Label(hdr, text="●", bg=SURFACE, fg=SUBTEXT, font=("Consolas", 15))
        self._dot.pack(side="right")
        self._slbl = tk.Label(hdr, text="Siap", bg=SURFACE, fg=SUBTEXT, font=FMN)
        self._slbl.pack(side="right", padx=(0, 6))
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

        steps = tk.Frame(self, bg=CARD, padx=20, pady=14)
        steps.pack(fill="x", padx=14, pady=12)
        tk.Label(steps, text="CARA PAKAI", bg=CARD, fg=ACCENT, font=("Consolas", 9, "bold")).pack(anchor="w")

        panduan = [
            ("1", "Klik  ▶ Buka Browser  — Chrome terbuka"),
            ("2", "Login SIAKAD seperti biasa (manual)"),
            ("3", "Navigasi ke halaman  Absensi"),
            ("4", "Klik  ▶ Mulai Bot  — bot otomatis ganti semester & ttd"),
        ]
        for num, txt in panduan:
            row = tk.Frame(steps, bg=CARD)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=f" {num} ", bg=ACCENT, fg=BG, font=("Consolas", 9, "bold"), padx=4, pady=1).pack(side="left")
            tk.Label(row, text=f"  {txt}", bg=CARD, fg=TEXT, font=FMN).pack(side="left")

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

        btns = tk.Frame(self, bg=BG, padx=14, pady=10)
        btns.pack(fill="x")

        self._btn_open = tk.Button(
            btns, text="🌐  Buka Browser", command=self._open_browser,
            bg=CARD, fg=ACCENT, activebackground=BORDER, relief="flat",
            font=("Consolas", 11, "bold"), padx=18, pady=9, cursor="hand2", bd=1, highlightbackground=BORDER,
        )
        self._btn_open.pack(side="left")

        self._btn_run = tk.Button(
            btns, text="▶  Mulai Bot", command=self._start_bot,
            bg=SUCCESS, fg=BG, activebackground="#2ea043", relief="flat",
            font=("Consolas", 11, "bold"), padx=18, pady=9, cursor="hand2",
        )
        self._btn_run.pack(side="left", padx=10)

        self._btn_stop = tk.Button(
            btns, text="■  Stop", command=self._do_stop,
            bg=DANGER, fg=BG, activebackground="#da3633", relief="flat",
            font=("Consolas", 11, "bold"), padx=18, pady=9, cursor="hand2", state="disabled",
        )
        self._btn_stop.pack(side="left")

        tk.Button(
            btns, text="🗑", command=self._clear,
            bg=SURFACE, fg=SUBTEXT, relief="flat", font=("Consolas", 12), padx=10, pady=9, cursor="hand2",
        ).pack(side="right")

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

        lf = tk.Frame(self, bg=BG, padx=0, pady=0)
        lf.pack(fill="both", expand=True)
        tk.Label(lf, text=" ● LOG ", bg=SURFACE, fg=SUBTEXT, font=("Consolas", 8, "bold"), anchor="w").pack(fill="x")

        self._log = scrolledtext.ScrolledText(
            lf, width=74, height=20, bg=SURFACE, fg=TEXT, insertbackground=ACCENT,
            relief="flat", font=FML, state="disabled", padx=12, pady=8,
        )
        self._log.pack(fill="both", expand=True)

        for tag, col in [("ok", SUCCESS), ("err", DANGER), ("warn", WARNING), ("info", ACCENT), ("dim", SUBTEXT)]:
            self._log.tag_config(tag, foreground=col)

    def _center(self):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        w  = self.winfo_width()
        h  = self.winfo_height()
        self.geometry(f"+{(sw-w)//2}+{(sh-h)//2}")

    def _write_log(self, msg: str):
        m = msg.lower()
        if any(k in m for k in ["✅","berhasil","selesai","🎉"]): tag = "ok"
        elif any(k in m for k in ["❌","💥","error","gagal"]): tag = "err"
        elif any(k in m for k in ["⚠","skip","tidak ditemukan","timeout"]): tag = "warn"
        elif any(k in m for k in ["🔍","🌐","🔗","💾","🔴","ℹ","✏","📄","📋","🟢","🔄","⏳"]): tag = "info"
        elif "═" in msg: tag = "dim"
        else: tag = None

        ts   = time.strftime("%H:%M:%S")
        line = f"[{ts}] {msg}\n"
        self._log.config(state="normal")
        self._log.insert("end", line, tag or "")
        self._log.see("end")
        self._log.config(state="disabled")

    def _set_status(self, s: str):
        MAP = {
            "running": (WARNING, "Berjalan..."),
            "done":    (SUCCESS, "Selesai ✓"),
            "error":   (DANGER,  "Error ✗"),
            "idle":    (SUBTEXT, "Siap"),
        }
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

    def _open_browser(self):
        chrome = find_chrome()
        if not chrome:
            messagebox.showerror("Chrome Tidak Ditemukan", "Download Chrome dari: https://google.com/chrome")
            return

        self._write_log(f"🌐  Membuka Chrome (Port: {CDP_PORT})")
        try:
            if self._chrome_proc and self._chrome_proc.poll() is None:
                self._chrome_proc.terminate()
                time.sleep(1)

            profile_dir = os.path.join(os.getcwd(), "chrome_bot_profile")
            self._chrome_proc = subprocess.Popen([
                chrome,
                f"--remote-debugging-port={CDP_PORT}",
                f"--user-data-dir={profile_dir}",
                "--no-first-run",
                "--no-default-browser-check",
                SITE_URL,
            ])
            self._write_log("✅  Browser terbuka! Silakan login SIAKAD.")
        except Exception as e:
            self._write_log(f"❌  Gagal buka browser: {e}")

    def _start_bot(self):
        self._stop_event.clear()
        self._btn_run.config(state="disabled")
        self._btn_stop.config(state="normal")
        self._set_status("running")
        self._write_log("\n" + "═" * 50)
        self._write_log(f"  ⚡ Bot dimulai — {time.strftime('%H:%M:%S')}")
        self._write_log("═" * 50)

        bot = SiakadBot(
            log_fn     = lambda m: self.after(0, self._write_log, m),
            status_fn  = self._set_status,
            stop_event = self._stop_event,
        )

        def _worker():
            asyncio.run(bot.run())
            if not self._stop_event.is_set():
                self.after(0, self._set_status, "idle")

        self._thread = threading.Thread(target=_worker, daemon=True)
        self._thread.start()

    def _do_stop(self):
        self._stop_event.set()
        self._write_log("🛑  Dihentikan.")
        self._btn_stop.config(state="disabled")
        self._set_status("idle")

    def _on_close(self):
        if self._chrome_proc and self._chrome_proc.poll() is None:
            if messagebox.askyesno("Tutup", "Tutup Chrome juga?"):
                self._chrome_proc.terminate()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()