import tkinter as tk
from enum import Enum, auto

# =====================================================
# STATE DEFINITIONS
# =====================================================
class DeviceState(Enum):
    IDLE = auto()
    START = auto()
    MIXING = auto()
    HEATING = auto()
    SEPARATION = auto()
    CLEANING = auto()
    FINISH = auto()
    ERROR = auto()
    FAIL_SAFE = auto()

# =====================================================
# STATE MACHINE / DEVICE CONTROLLER
# =====================================================
class DeviceController:
    def __init__(self):
        self.state = DeviceState.IDLE
        self.temperature = 25
        self.rpm = 500
        self.duration = 60

    # -----------------------------
    # FAIL SAFE
    # -----------------------------
    def enter_fail_safe(self):
        self.temperature = 0
        self.rpm = 0
        self.state = DeviceState.FAIL_SAFE

    # -----------------------------
    # USER ACTIONS
    # -----------------------------
    def start(self):
        if self.state == DeviceState.IDLE:
            self.state = DeviceState.START

    def stop(self):
        self.enter_fail_safe()

    def trigger_error(self):
        self.state = DeviceState.ERROR
        self.enter_fail_safe()

    # -----------------------------
    # STATE TRANSITION LOGIC
    # -----------------------------
    def next_state(self):
        if self.state == DeviceState.START:
            self.state = DeviceState.MIXING
        elif self.state == DeviceState.MIXING:
            self.state = DeviceState.HEATING
        elif self.state == DeviceState.HEATING:
            # Örnek hata simülasyonu
            if self.temperature > 250:
                self.trigger_error()
            else:
                self.state = DeviceState.SEPARATION
        elif self.state == DeviceState.SEPARATION:
            self.state = DeviceState.CLEANING
        elif self.state == DeviceState.CLEANING:
            self.state = DeviceState.FINISH
        elif self.state == DeviceState.FINISH:
            self.state = DeviceState.IDLE
        elif self.state == DeviceState.FAIL_SAFE:
            self.state = DeviceState.IDLE

# =====================================================
# UI LAYER
# =====================================================
device = DeviceController()

def update_status():
    state_text = device.state.name
    status_label.config(text=f"Durum: {state_text}")

def start_device():
    device.start()
    update_status()

def stop_device():
    device.stop()
    update_status()

def next_step():
    device.next_state()
    update_status()

def set_temp(v):
    device.temperature = int(v)

def set_rpm(v):
    device.rpm = int(v)

def set_time(v):
    device.duration = int(v)

# -----------------------------
# TKINTER UI
# -----------------------------
root = tk.Tk()
root.title("Nanopartikül Üretim Kontrolü")
root.geometry("480x400")
root.resizable(False, False)

status_label = tk.Label(
    root, text="Durum: IDLE",
    font=("Arial", 16, "bold"),
    bg="gray", fg="white", pady=10
)
status_label.pack(fill="x")

settings = tk.LabelFrame(root, text="Parametreler", padx=10, pady=10)
settings.pack(padx=10, pady=10, fill="x")

tk.Label(settings, text="Sıcaklık (°C)").grid(row=0, column=0, sticky="w")
tk.Scale(settings, from_=0, to=300, orient=tk.HORIZONTAL, command=set_temp).grid(row=0, column=1)

tk.Label(settings, text="Karıştırma Hızı (RPM)").grid(row=1, column=0, sticky="w")
tk.Scale(settings, from_=0, to=2000, orient=tk.HORIZONTAL, command=set_rpm).grid(row=1, column=1)

tk.Label(settings, text="Süre (sn)").grid(row=2, column=0, sticky="w")
tk.Scale(settings, from_=0, to=600, orient=tk.HORIZONTAL, command=set_time).grid(row=2, column=1)

buttons = tk.Frame(root)
buttons.pack(pady=10)

tk.Button(buttons, text="BAŞLAT", width=12, command=start_device).grid(row=0, column=0, padx=5)
tk.Button(buttons, text="SONRAKİ ADIM", width=12, command=next_step).grid(row=0, column=1, padx=5)

tk.Button(root, text="DURDUR", width=28, command=stop_device).pack(pady=5)

root.mainloop()
