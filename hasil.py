import tkinter as tk
import time

class SignatureTester(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tester Koordinat Tanda Tangan")
        self.configure(bg="#0d1117")
        self.resizable(False, False)
        
        # Ukuran canvas disamakan dengan script perekam (500x250)
        self.canvas_w = 500
        self.canvas_h = 250
        
        tk.Label(self, text="👀 Preview Tanda Tangan:", 
                 bg="#0d1117", fg="#c9d1d9", font=("Consolas", 11)).pack(pady=10)
        
        self.canvas = tk.Canvas(self, width=self.canvas_w, height=self.canvas_h, 
                                bg="white", bd=0, highlightthickness=1)
        self.canvas.pack(padx=20)
        
        tk.Button(self, text="▶️ Simulasikan Gambar", command=self.simulate_draw, 
                  bg="#58a6ff", fg="white", font=("Consolas", 10, "bold"), relief="flat", padx=10).pack(pady=15)

    def p(self, x, y):
        # Mengubah rasio (0.00 - 1.00) kembali menjadi piksel asli di dalam canvas
        return (x * self.canvas_w, y * self.canvas_h)

    def simulate_draw(self):
        self.canvas.delete("all")
        
        # --- DATA KOORDINAT DARI HASIL REKAMANMU ---
        stroke1 = [
            self.p(0.342, 0.368), self.p(0.348, 0.348), self.p(0.356, 0.324), self.p(0.362, 0.300),
            self.p(0.368, 0.280), self.p(0.372, 0.260), self.p(0.376, 0.240), self.p(0.380, 0.220),
            self.p(0.384, 0.200), self.p(0.388, 0.180), self.p(0.392, 0.160), self.p(0.398, 0.180),
            self.p(0.402, 0.204), self.p(0.404, 0.228), self.p(0.406, 0.260), self.p(0.408, 0.288),
            self.p(0.408, 0.312), self.p(0.410, 0.332), self.p(0.410, 0.356), self.p(0.410, 0.380),
            self.p(0.412, 0.404), self.p(0.412, 0.428), self.p(0.414, 0.448), self.p(0.412, 0.468),
            self.p(0.410, 0.488), self.p(0.408, 0.508), self.p(0.406, 0.528), self.p(0.402, 0.548),
            self.p(0.394, 0.564), self.p(0.386, 0.584), self.p(0.374, 0.600), self.p(0.364, 0.612),
            self.p(0.354, 0.616), self.p(0.344, 0.612), self.p(0.334, 0.600), self.p(0.328, 0.580),
            self.p(0.326, 0.560), self.p(0.328, 0.536), self.p(0.332, 0.516), self.p(0.338, 0.496),
            self.p(0.344, 0.472), self.p(0.352, 0.452), self.p(0.358, 0.432), self.p(0.364, 0.412),
            self.p(0.372, 0.396), self.p(0.378, 0.376), self.p(0.384, 0.356), self.p(0.392, 0.336),
            self.p(0.398, 0.316), self.p(0.408, 0.288), self.p(0.414, 0.268), self.p(0.418, 0.248),
            self.p(0.424, 0.228), self.p(0.428, 0.208), self.p(0.434, 0.188), self.p(0.438, 0.168),
            self.p(0.442, 0.148), self.p(0.446, 0.128), self.p(0.454, 0.148), self.p(0.458, 0.168),
            self.p(0.462, 0.192), self.p(0.464, 0.212), self.p(0.466, 0.232), self.p(0.468, 0.252),
            self.p(0.470, 0.272), self.p(0.472, 0.300), self.p(0.472, 0.324), self.p(0.474, 0.344),
            self.p(0.474, 0.372), self.p(0.474, 0.396), self.p(0.474, 0.420), self.p(0.476, 0.440),
            self.p(0.476, 0.468), self.p(0.478, 0.488), self.p(0.480, 0.508), self.p(0.480, 0.532),
            self.p(0.480, 0.504), self.p(0.478, 0.484), self.p(0.476, 0.464), self.p(0.476, 0.436),
            self.p(0.472, 0.416), self.p(0.472, 0.392), self.p(0.470, 0.372), self.p(0.466, 0.352),
            self.p(0.466, 0.328), self.p(0.464, 0.304), self.p(0.462, 0.284), self.p(0.462, 0.260),
            self.p(0.462, 0.232), self.p(0.464, 0.208), self.p(0.466, 0.188), self.p(0.472, 0.168),
            self.p(0.482, 0.156), self.p(0.492, 0.140), self.p(0.504, 0.132), self.p(0.514, 0.128),
            self.p(0.526, 0.124), self.p(0.538, 0.128), self.p(0.548, 0.136), self.p(0.558, 0.148),
            self.p(0.566, 0.164), self.p(0.574, 0.180), self.p(0.576, 0.200), self.p(0.576, 0.224),
            self.p(0.572, 0.248), self.p(0.566, 0.268), self.p(0.560, 0.288), self.p(0.550, 0.308),
            self.p(0.542, 0.324), self.p(0.532, 0.340), self.p(0.522, 0.356), self.p(0.512, 0.364),
            self.p(0.502, 0.368), self.p(0.492, 0.376), self.p(0.482, 0.380), self.p(0.490, 0.396),
            self.p(0.498, 0.416), self.p(0.508, 0.432), self.p(0.516, 0.448), self.p(0.526, 0.460),
            self.p(0.534, 0.476), self.p(0.544, 0.496), self.p(0.554, 0.512), self.p(0.564, 0.524),
            self.p(0.572, 0.540), self.p(0.582, 0.552)
        ]

        # Logika untuk menjalankan animasi menggambar garis
        for i in range(len(stroke1) - 1):
            x1, y1 = stroke1[i]
            x2, y2 = stroke1[i+1]
            self.canvas.create_line(x1, y1, x2, y2, width=3, fill="black", capstyle=tk.ROUND, smooth=True)
            self.update() # Memperbarui tampilan UI
            time.sleep(0.005)  # Kecepatan menggambar (semakin kecil angkanya, semakin cepat)

if __name__ == "__main__":
    app = SignatureTester()
    app.mainloop()