import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import sys

# Ensure we are in the correct directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def run_command(script_name):
    """
    Runs a batch script in a new console window.
    """
    try:
        if os.path.exists(script_name):
            # subprocess.Popen with shell=True and start ensures a new window on Windows
            subprocess.Popen(f'start cmd /k "{script_name}"', shell=True)
        else:
            messagebox.showerror("Error", f"File not found: {script_name}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run script: {e}")

def start_dashboard():
    run_command("run_dashboard.bat")

def start_watcher():
    run_command("watch_files.bat")

def start_scan():
    run_command("scan_files.bat")

def create_user():
    run_command("create_user.bat")

def open_admin():
    import webbrowser
    webbrowser.open("http://127.0.0.1:8000/admin")

def open_dashboard():
    import webbrowser
    webbrowser.open("http://127.0.0.1:8000/")

# Application Setup
root = tk.Tk()
root.title("FIM Sentinel Launcher")
root.geometry("400x550")
root.configure(bg="#0f172a")

# Styles
style = ttk.Style()
style.theme_use('clam')
style.configure("TButton", 
                font=('Segoe UI', 11), 
                padding=10, 
                background="#3b82f6", 
                foreground="white",
                borderwidth=0)
style.map("TButton", 
          background=[('active', '#2563eb')])

# Header
header_frame = tk.Frame(root, bg="#0f172a", pady=20)
header_frame.pack()
tk.Label(header_frame, text="🛡️ FIM Sentinel", font=("Segoe UI", 20, "bold"), bg="#0f172a", fg="#3b82f6").pack()
tk.Label(header_frame, text="Security Control Panel", font=("Segoe UI", 10), bg="#0f172a", fg="#94a3b8").pack()

# Buttons Frame
btn_frame = tk.Frame(root, bg="#0f172a", pady=10)
btn_frame.pack(fill='x', padx=40)

def create_btn(text, command, color=None):
    btn = ttk.Button(btn_frame, text=text, command=command, cursor="hand2")
    btn.pack(fill='x', pady=5)
    return btn

# Operations Section
tk.Label(btn_frame, text="OPERATIONS", font=("Segoe UI", 8, "bold"), bg="#0f172a", fg="#64748b", anchor="w").pack(fill='x', pady=(10, 5))

create_btn("🚀 Start Dashboard Server", start_dashboard)
create_btn("👀 Start Real-Time Watcher", start_watcher)
create_btn("🔍 Run Single Scan", start_scan)

# Access Section
tk.Label(btn_frame, text="ACCESS", font=("Segoe UI", 8, "bold"), bg="#0f172a", fg="#64748b", anchor="w").pack(fill='x', pady=(20, 5))

create_btn("🌐 Open Dashboard (Browser)", open_dashboard)
create_btn("⚙️ Open Admin Panel", open_admin)

# Setup Section
tk.Label(btn_frame, text="SETUP", font=("Segoe UI", 8, "bold"), bg="#0f172a", fg="#64748b", anchor="w").pack(fill='x', pady=(20, 5))

create_btn("👤 Create Admin User", create_user)

# Footer
tk.Label(root, text="v1.0.0 | Ready", font=("Segoe UI", 8), bg="#0f172a", fg="#475569").pack(side="bottom", pady=10)

root.mainloop()
