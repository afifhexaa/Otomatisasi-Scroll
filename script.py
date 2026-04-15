import pyautogui
import time
import random
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import datetime

# Flag global
running = False

# Fungsi logging dua kolom
def log_split(widget, left="", right=""):
    timestamp = time.strftime("%H:%M:%S")
    space = " " * 5
    if left:
        widget.insert(tk.END, f"{timestamp} ▶ {left}{space}\n")
    if right:
        widget.insert(tk.END, f"{timestamp} ▶ {space*10}{right}\n")
    widget.see(tk.END)

# Simulasi perilaku manusia
def smart_behavior(widget, min_delay, max_delay, right_timer):
    global running
    count = 1
    while running:
        log_split(widget, right=f"🌀 Aksi ke-{count}")

        mode = random.choices(
            ['normal', 'idle', 'focused', 'distracted'], weights=[50, 20, 20, 10], k=1
        )[0]

        if mode == 'normal':
            if random.random() < 0.7:
                dx, dy = random.randint(-20, 20), random.randint(-10, 10)
                pyautogui.moveRel(dx, dy, duration=0.3)
                log_split(widget, right=f"🖱️ Mouse moved ({dx},{dy})")
            if random.random() < 0.5:
                scroll_amt = random.choice([-100, -50, 50, 100])
                pyautogui.scroll(scroll_amt)
                log_split(widget, right=f"📜 Scrolled {scroll_amt}")
        elif mode == 'focused':
            pyautogui.scroll(50)
            log_split(widget, right="🧠 Fokus: Scroll pelan")
        elif mode == 'distracted':
            log_split(widget, right="💭 Distracted: diam")
        elif mode == 'idle':
            log_split(widget, right="😴 Idle: tidak bergerak")

        delay = random.randint(min_delay, max_delay)
        for i in range(delay, 0, -1):
            if not running:
                return
            right_timer.set(f"⏳ Aksi berikutnya dalam: {i}s")
            time.sleep(1)
        count += 1

# Deteksi tombol continue editing
def detect_continue_editing(widget, image_path, left_timer):
    global running
    cek_delay = 30
    while running:
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
            if location:
                log_split(widget, left=f"✅ Tombol ditemukan di {location}. Klik!")
                pyautogui.moveTo(location)
                pyautogui.click()
                time.sleep(2)
            else:
                log_split(widget, left="🔍 Tidak ada tombol ditemukan.")
        except Exception as e:
            log_split(widget, left=f"⚠️ Tombol tidak terdeteksi {str(e)}")

        for i in range(cek_delay, 0, -1):
            if not running:
                return
            left_timer.set(f"⌛ Cek tombol berikutnya: {i}s")
            time.sleep(1)

# Kontrol GUI
def start_simulation(log, slider, img_path_var, left_timer, right_timer):
    global running
    if running:
        return
    running = True
    min_delay = int(slider.get())
    max_delay = min_delay + 40
    path = img_path_var.get()

    if not path:
        messagebox.showwarning("Gambar kosong", "Harap pilih gambar tombol popup.")
        return

    threading.Thread(target=smart_behavior, args=(log, min_delay, max_delay, right_timer), daemon=True).start()
    threading.Thread(target=detect_continue_editing, args=(log, path, left_timer), daemon=True).start()

def stop_simulation():
    global running
    running = False

def pilih_gambar(img_path_var, preview_label):
    path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
    if path:
        img_path_var.set(path)
        img = Image.open(path)
        img.thumbnail((150, 150))
        img_tk = ImageTk.PhotoImage(img)
        preview_label.config(image=img_tk)
        preview_label.image = img_tk

# Update waktu real-time
def update_clock(clock_label, date_label):
    now = time.strftime("%H:%M:%S")
    today = datetime.datetime.now().strftime("%A, %d %B %Y")
    clock_label.config(text=now)
    date_label.config(text=today)
    clock_label.after(1000, update_clock, clock_label, date_label)

# Main GUI
def main_gui():
    window = tk.Tk()
    window.title("🛡️ Kaggle Scroll Guardian")
    window.geometry("800x650")
    window.configure(bg="black")

    # Header Clock
    header_frame = tk.Frame(window, bg="black")
    header_frame.pack(pady=5)
    date_label = tk.Label(header_frame, font=("Courier", 12), fg="lime", bg="black")
    date_label.pack()
    clock_label = tk.Label(header_frame, font=("Courier", 16), fg="lime", bg="black")
    clock_label.pack()
    update_clock(clock_label, date_label)

    # Countdown Timers
    timer_frame = tk.Frame(window, bg="black")
    timer_frame.pack(pady=5)
    left_timer = tk.StringVar()
    right_timer = tk.StringVar()
    tk.Label(timer_frame, textvariable=left_timer, font=("Courier", 12), fg="lime", bg="black").pack(side=tk.LEFT, padx=40)
    tk.Label(timer_frame, textvariable=right_timer, font=("Courier", 12), fg="lime", bg="black").pack(side=tk.RIGHT, padx=40)

    # Pengaturan Frame
    control_frame = tk.LabelFrame(window, text="⚙️ Pengaturan", fg="lime", bg="black", font=("Courier", 10), labelanchor='n')
    control_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(control_frame, text="Delay minimal antar aksi (detik):", fg="lime", bg="black").pack(pady=2)
    slider = tk.Scale(control_frame, from_=30, to=90, orient=tk.HORIZONTAL, fg="lime", bg="black", troughcolor="green", highlightbackground="black")
    slider.set(50)
    slider.pack(pady=2)

    # Gambar Frame
    gambar_frame = tk.LabelFrame(window, text="🖼️ Gambar Tombol 'Continue Editing'", fg="lime", bg="black", font=("Courier", 10), labelanchor='n')
    gambar_frame.pack(fill="x", padx=10, pady=5)

    img_path_var = tk.StringVar()
    tk.Entry(gambar_frame, textvariable=img_path_var, width=60, bg="#111", fg="lime", insertbackground="lime").pack(pady=5)
    preview_label = tk.Label(gambar_frame, bg="black")
    preview_label.pack()
    tk.Button(gambar_frame, text="📁 Pilih Gambar", command=lambda: pilih_gambar(img_path_var, preview_label), bg="lime", fg="black").pack(pady=5)

    # Log Terminal
    log_frame = tk.LabelFrame(window, text="📜 Aktivitas Log", fg="lime", bg="black", font=("Courier", 10), labelanchor='n')
    log_frame.pack(fill="both", expand=True, padx=10, pady=5)
    log = tk.Text(log_frame, height=15, bg="black", fg="lime", font=("Courier", 10))
    log.pack(fill=tk.BOTH, expand=True, padx=5)

    # Tombol Kontrol
    btn_frame = tk.Frame(window, bg="black")
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="▶ Mulai", command=lambda: start_simulation(log, slider, img_path_var, left_timer, right_timer), bg="lime", fg="black", width=12).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="🛑 Stop", command=stop_simulation, bg="lime", fg="black", width=12).pack(side=tk.RIGHT, padx=10)

    window.mainloop()

if __name__ == "__main__":
    main_gui()
