import tkinter as tk
from tkinter import messagebox
from enum import Enum, auto
import datetime

class DeviceState(Enum):
    IDLE = auto()
    MIXING = auto()
    HEATING = auto()
    SEPARATION = auto()
    CLEANING = auto()
    FINISH = auto()
    FAIL_SAFE = auto()

class DeviceController:
    def __init__(self):
        self.state = DeviceState.IDLE
        self.temperature = 25
        self.target_temp = 90
        self.rpm = 500
        self.duration = 5
        
        self.time_counter = 0
        self.current_step_duration = 0
        self.separation_time = 3
        self.cleaning_time = 2
        self.error_msg = ""

    def log_event(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] State: {self.state.name} | {message}\n"
        with open("process_log.txt", "a", encoding="utf-8") as f:
            f.write(log_entry)

    def enter_fail_safe(self, reason):
        self.error_msg = reason
        self.state = DeviceState.FAIL_SAFE
        self.log_event(f"HATA OLUŞTU: {reason}")
        self.temperature = 25
        self.rpm = 0

    def reset_system(self):
        self.state = DeviceState.IDLE
        self.error_msg = ""
        self.temperature = 25
        self.log_event("Sistem kullanıcı tarafından sıfırlandı.")

    def check_errors(self):
        if self.state == DeviceState.FAIL_SAFE: return
        
        if self.temperature > 115:
            self.enter_fail_safe("Kritik Sıcaklık Limiti Aşıldı (>115°C)")
        elif self.rpm > 1800:
            self.enter_fail_safe("Yüksek RPM Kararsızlığı (>1800)")
        elif self.state not in [DeviceState.IDLE, DeviceState.FINISH] and self.rpm < 50:
            self.enter_fail_safe("Motor Tork Kaybı / Sıkışma")

    def start(self):
        # GÜVENLİK KİLİDİ: Hata varken başlatma
        if self.state == DeviceState.FAIL_SAFE:
            messagebox.showerror("GÜVENLİK ENGELİ", f"Sistemde çözülmemiş hata var: {self.error_msg}\nLütfen 'SIFIRLA' butonuna basın.")
            return

        if self.state in [DeviceState.IDLE, DeviceState.FINISH]:
            self.state = DeviceState.MIXING
            self.time_counter = 0
            self.current_step_duration = self.duration
            self.log_event("Süreç Otomatik Olarak Başlatıldı")

    def stop(self):
        self.enter_fail_safe("Kullanıcı Acil Durdurma")

    def update(self):
        self.check_errors()
        if self.state in [DeviceState.FAIL_SAFE, DeviceState.IDLE]:
            return

        if self.state == DeviceState.MIXING:
            self.time_counter += 1
            if self.time_counter >= self.current_step_duration:
                self.state = DeviceState.HEATING
                self.time_counter = 0

        elif self.state == DeviceState.HEATING:
            if self.temperature < self.target_temp:
                self.temperature += 3
            else:
                self.state = DeviceState.SEPARATION
                self.time_counter = 0
                self.current_step_duration = self.separation_time

        elif self.state == DeviceState.SEPARATION:
            self.time_counter += 1
            if self.time_counter >= self.current_step_duration:
                self.state = DeviceState.CLEANING
                self.time_counter = 0
                self.current_step_duration = self.cleaning_time

        elif self.state == DeviceState.CLEANING:
            self.time_counter += 1
            if self.time_counter >= self.current_step_duration:
                self.state = DeviceState.FINISH

        elif self.state == DeviceState.FINISH:
            res = self.calculate_particle()
            messagebox.showinfo("İşlem Tamamlandı", res)
            self.state = DeviceState.IDLE

    def calculate_particle(self):
        base_size = 120
        temp_effect = abs(self.target_temp - 70) * 0.4
        rpm_effect = self.rpm / 150
        particle_size = (base_size + temp_effect) / (1 + rpm_effect)
        msg = f"Sentez Sonucu: {round(particle_size, 2)} nm"
        self.log_event(msg)
        return msg

device = DeviceController()

def update_ui():
    status_label.config(text=f"Durum: {device.state.name}")
    temp_display.config(text=f"Anlık Sıcaklık: {device.temperature}°C")
    
    if device.state in [DeviceState.MIXING, DeviceState.SEPARATION, DeviceState.CLEANING]:
        remaining = device.current_step_duration - device.time_counter
        timer_label.config(text=f"Kalan Süre: {remaining} sn", fg="#0056b3")
    elif device.state == DeviceState.HEATING:
        timer_label.config(text="Isınıyor...", fg="#d9534f")
    else:
        timer_label.config(text="")

    if device.state == DeviceState.FAIL_SAFE:
        status_label.config(fg="red")
        error_display.config(text=f"DURDURULDU: {device.error_msg}")
    elif device.state == DeviceState.IDLE:
        status_label.config(fg="black")
        error_display.config(text="")
    else:
        status_label.config(fg="green")

def loop():
    device.update()
    update_ui()
    root.after(1000, loop)

def set_temp(v): device.target_temp = int(v)
def set_rpm(v): device.rpm = int(v)
def set_time(v): device.duration = int(v)

# --- UI TASARIMI ---
root = tk.Tk()
root.title("NanoPro Control System v2.1")
root.geometry("450x600")

status_label = tk.Label(root, text="Durum: IDLE", font=("Arial", 16, "bold"))
status_label.pack(pady=15)

timer_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
timer_label.pack()

temp_display = tk.Label(root, text="Sıcaklık: 25°C", font=("Arial", 10))
temp_display.pack(pady=5)

error_display = tk.Label(root, text="", fg="red", font=("Arial", 10, "italic"))
error_display.pack()

param_frame = tk.LabelFrame(root, text=" Sistem Parametreleri ", padx=10, pady=10)
param_frame.pack(padx=20, pady=10, fill="x")

tk.Label(param_frame, text="Hedef Sıcaklık (°C):").pack()
tk.Scale(param_frame, from_=25, to=150, orient="horizontal", command=set_temp).pack(fill="x")

tk.Label(param_frame, text="Karıştırma Hızı (RPM):").pack()
tk.Scale(param_frame, from_=0, to=2000, orient="horizontal", command=set_rpm).pack(fill="x")

tk.Label(param_frame, text="Başlangıç Karıştırma Süresi (sn):").pack()
tk.Scale(param_frame, from_=1, to=30, orient="horizontal", command=set_time).pack(fill="x")

btn_frame = tk.Frame(root)
btn_frame.pack(pady=15)

tk.Button(btn_frame, text="BAŞLAT", command=device.start, bg="#d4edda", width=15, height=2).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="ACİL DURDUR", command=device.stop, bg="#f8d7da", width=15, height=2).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="SİSTEMİ SIFIRLA", command=device.reset_system, bg="#e2e3e5", width=32).grid(row=1, column=0, columnspan=2, pady=10)

loop()
root.mainloop()
