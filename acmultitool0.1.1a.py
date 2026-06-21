import tkinter as tk
from tkinter import ttk, scrolledtext
import socket
import subprocess
import threading
import platform
import sys
import ctypes
import os
import urllib.request
import json

# Auto Dependencies
def install_dependencies():
    required = ["pyperclip"]
    for pkg in required:
        try:
            __import__(pkg.replace("-", "_"))
        except ImportError:
            print(f"Installing {pkg}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
            except:
                print(f"Failed to install {pkg}")

install_dependencies()

# Auto Admin
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if platform.system() == "Windows" and not is_admin():
        try:
            script = os.path.abspath(sys.argv[0])
            params = ' '.join([f'"{arg}"' for arg in sys.argv[1:]])
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
            sys.exit(0)
        except:
            pass

run_as_admin()

class CatsMultitool:
    def __init__(self, root):
        self.root = root
        self.root.title("AC HOLDINGS MULTITOOL v0.2.5 🐱 [ADMIN]")
        self.root.geometry("1100x720")
        self.root.configure(bg="#0A0A0A")

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TNotebook", background="#0A0A0A")
        self.style.configure("TNotebook.Tab", background="#1A1A1A", foreground="#00FFAA", padding=[12, 6], font=("Courier", 10, "bold"))
        self.style.map("TNotebook.Tab", background=[("selected", "#003322")])
        self.style.configure("TButton", background="#002211", foreground="#00FFAA", borderwidth=3, font=("Courier", 11, "bold"))

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=8, pady=8)

        tabs = [
            ("WiFi Scanner", self.build_wifi_tab),
            ("Port Scanner", self.build_port_tab),
            ("IP Grabber", self.build_ipgrabber_tab),
        ]
        
        for tab_name, build_func in tabs:
            frame = tk.Frame(self.notebook, bg="#0A0A0A")
            self.notebook.add(frame, text=tab_name)
            build_func(frame)

        self.status = tk.Label(root, text="AC HOLDINGS MULTITOOL v0.2.5 | PROTOCOL ZERO | NYAH~ Master AC", 
                             bg="#000000", fg="#00FFAA", font=("Courier", 9), anchor="w")
        self.status.pack(side="bottom", fill="x", padx=5, pady=3)

    def _safe_insert(self, widget, text):
        def insert():
            widget.insert(tk.END, text)
            widget.see(tk.END)
        self.root.after(0, insert)

    # WiFi Scanner (fixed)
    def build_wifi_tab(self, frame):
        tk.Label(frame, text="=== WIFI SCANNER ===", bg="#0A0A0A", fg="#00FFAA", font=("Courier", 14, "bold")).pack(pady=10)
        tk.Button(frame, text="LAUNCH WIFI SCAN", bg="#002211", fg="#00FFAA", font=("Courier", 12, "bold"),
                  command=self.scan_wifi, height=2, width=30).pack(pady=10)
        self.wifi_output = scrolledtext.ScrolledText(frame, height=20, bg="#000000", fg="#00FFAA", font=("Courier", 10))
        self.wifi_output.pack(padx=10, pady=10, fill="both", expand=True)

    def scan_wifi(self):
        self._safe_insert(self.wifi_output, "SCANNING NETWORKS (ADMIN MODE)...\n")
        def run():
            try:
                system = platform.system()
                if system == "Darwin":
                    result = subprocess.check_output(["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-s"], timeout=15).decode(errors='ignore')
                elif system == "Windows":
                    try:
                        result = subprocess.check_output("netsh wlan show networks", shell=True, timeout=15).decode(errors='ignore')
                    except subprocess.CalledProcessError:
                        result = "No WiFi networks found or WiFi is disabled.\nTips: Turn on WiFi first.\n"
                else:
                    cmds = ["nmcli dev wifi list 2>/dev/null", "iwlist scan 2>/dev/null"]
                    result = ""
                    for cmd in cmds:
                        try:
                            out = subprocess.check_output(cmd, shell=True, timeout=10).decode(errors='ignore')
                            if out.strip():
                                result += out + "\n---\n"
                        except:
                            pass
                    if not result.strip():
                        result = "Try sudo or install nmcli/iwlist.\n"
                self._safe_insert(self.wifi_output, result + "\nSCAN COMPLETE ~ NYAH! Master AC\n")
            except Exception as e:
                self._safe_insert(self.wifi_output, f"ERROR: {str(e)}\n")
        threading.Thread(target=run, daemon=True).start()

    # Port Scanner
    def build_port_tab(self, frame):
        tk.Label(frame, text="=== PORT SCANNER ===", bg="#0A0A0A", fg="#00FFAA", font=("Courier", 14, "bold")).pack(pady=10)
        tk.Label(frame, text="Target:", bg="#0A0A0A", fg="#00FFAA").pack(anchor="w", padx=10)
        self.port_target = tk.Entry(frame, width=40, bg="#1A1A1A", fg="#00FFAA", insertbackground="#00FFAA")
        self.port_target.pack(padx=10, fill="x")
        self.port_target.insert(0, "127.0.0.1")
        tk.Button(frame, text="LAUNCH PORT SCAN", bg="#002211", fg="#00FFAA", font=("Courier", 12, "bold"),
                  command=self.scan_ports, height=2, width=30).pack(pady=10)
        self.port_output = scrolledtext.ScrolledText(frame, height=20, bg="#000000", fg="#00FFAA", font=("Courier", 10))
        self.port_output.pack(padx=10, pady=10, fill="both", expand=True)

    def scan_ports(self):
        target = self.port_target.get().strip()
        self._safe_insert(self.port_output, f"SCANNING {target}...\n")
        def scan():
            for port in range(1, 1001):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.3)
                    if s.connect_ex((target, port)) == 0:
                        self._safe_insert(self.port_output, f"[OPEN] Port {port}\n")
                    s.close()
                except:
                    pass
            self._safe_insert(self.port_output, "PORT SCAN COMPLETE ~ NYAH! Master AC\n")
        threading.Thread(target=scan, daemon=True).start()

    # IP Grabber
    def build_ipgrabber_tab(self, frame):
        tk.Label(frame, text="=== IP GRABBER ===", bg="#0A0A0A", fg="#00FFAA", font=("Courier", 14, "bold")).pack(pady=10)
        
        tk.Button(frame, text="GET PUBLIC IP", bg="#002211", fg="#00FFAA", font=("Courier", 12, "bold"),
                  command=self.get_public_ip, height=2, width=30).pack(pady=10)
        
        tk.Button(frame, text="GET LOCAL IP", bg="#002211", fg="#00FFAA", font=("Courier", 12, "bold"),
                  command=self.get_local_ip, height=2, width=30).pack(pady=5)
        
        self.ip_output = scrolledtext.ScrolledText(frame, height=18, bg="#000000", fg="#00FFAA", font=("Courier", 10))
        self.ip_output.pack(padx=10, pady=10, fill="both", expand=True)

    def get_public_ip(self):
        self._safe_insert(self.ip_output, "Fetching Public IP...\n")
        def run():
            try:
                with urllib.request.urlopen("https://api.ipify.org?format=json", timeout=8) as resp:
                    data = json.loads(resp.read().decode())
                    ip = data["ip"]
                    self._safe_insert(self.ip_output, f"✅ PUBLIC IP: {ip}\n")
            except:
                self._safe_insert(self.ip_output, "Failed. Check internet connection.\n")
        threading.Thread(target=run, daemon=True).start()

    def get_local_ip(self):
        self._safe_insert(self.ip_output, "Fetching Local IP...\n")
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            self._safe_insert(self.ip_output, f"✅ LOCAL IP: {local_ip}\n")
        except Exception as e:
            self._safe_insert(self.ip_output, f"Failed: {e}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = CatsMultitool(root)
    root.mainloop()