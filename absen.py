import tkinter as tk
import math

class SignatureRecorder(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Perekam Tanda Tangan SIAKAD")
        self.configure(bg="#0d1117")
        self.resizable(False, False)
        
        # Proporsi canvas mirip dengan rasio canvas di web SIAKAD
        self.canvas_w = 500
        self.canvas_h = 250
        
        tk.Label(self, text="✍️ Gambar tanda tanganmu di kotak putih bawah ini:", 
                 bg="#0d1117", fg="#c9d1d9", font=("Consolas", 11)).pack(pady=10)
        
        self.canvas = tk.Canvas(self, width=self.canvas_w, height=self.canvas_h, 
                                bg="white", cursor="crosshair", bd=0, highlightthickness=1)
        self.canvas.pack(padx=20)
        
        # Binding event mouse
        self.canvas.bind("<Button-1>", self.start_stroke)
        self.canvas.bind("<B1-Motion>", self.draw_stroke)
        self.canvas.bind("<ButtonRelease-1>", self.end_stroke)
        
        self.strokes = []
        self.current_stroke = []
        self.last_x = 0
        self.last_y = 0
        
        # Tombol aksi
        btn_frame = tk.Frame(self, bg="#0d1117")
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="🗑️ Hapus Ulang", command=self.clear, 
                  bg="#f85149", fg="white", font=("Consolas", 10, "bold"), relief="flat", padx=10).pack(side="left", padx=10)
        tk.Button(btn_frame, text="⚙️ Buat Kode", command=self.generate, 
                  bg="#3fb950", fg="white", font=("Consolas", 10, "bold"), relief="flat", padx=10).pack(side="left", padx=10)
        
        # Area teks untuk menampung kode
        self.text_area = tk.Text(self, height=12, width=70, bg="#161b22", fg="#58a6ff", 
                                 font=("Consolas", 9), insertbackground="white", relief="flat", padx=10, pady=10)
        self.text_area.pack(padx=20, pady=(0, 20))
        
    def start_stroke(self, event):
        self.current_stroke = []
        self.add_point(event.x, event.y)
        self.last_x, self.last_y = event.x, event.y

    def draw_stroke(self, event):
        # Hindari error jika mouse keluar canvas
        x = max(0, min(event.x, self.canvas_w))
        y = max(0, min(event.y, self.canvas_h))
        
        # Ambil jarak antar titik. Jika > 5 pixel, baru simpan (agar kode tidak terlalu panjang/berat)
        dist = math.hypot(x - self.last_x, y - self.last_y)
        if dist > 5: 
            self.canvas.create_line(self.last_x, self.last_y, x, y, width=3, fill="black", capstyle=tk.ROUND, smooth=True)
            self.add_point(x, y)
            self.last_x, self.last_y = x, y

    def end_stroke(self, event):
        if self.current_stroke:
            self.strokes.append(self.current_stroke)
            self.current_stroke = []
            
    def add_point(self, x, y):
        # Ubah kordinat pixel menjadi rasio 0.00 hingga 1.00
        rx = round(x / self.canvas_w, 3)
        ry = round(y / self.canvas_h, 3)
        self.current_stroke.append((rx, ry))
        
    def clear(self):
        self.canvas.delete("all")
        self.strokes = []
        self.text_area.delete("1.0", tk.END)
        
    def generate(self):
        self.text_area.delete("1.0", tk.END)
        if not self.strokes:
            self.text_area.insert(tk.END, "Canvas masih kosong! Gambar dulu ya.")
            return
            
        code = ""
        for i, strk in enumerate(self.strokes, 1):
            code += f"        stroke{i} = [\n"
            for rx, ry in strk:
                code += f"            p({rx:.3f}, {ry:.3f}),\n"
            code += "        ]\n"
            
        code += "\n"
        for i in range(1, len(self.strokes) + 1):
            code += f"        await stroke(stroke{i})\n"
            code += f"        await asyncio.sleep(0.1)\n"
            
        self.text_area.insert(tk.END, code)

if __name__ == "__main__":
    app = SignatureRecorder()
    app.mainloop()