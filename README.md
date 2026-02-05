# 🛡️ FIM Sentinel: File Integrity Monitoring System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Django 5.0](https://img.shields.io/badge/django-5.0-green.svg)](https://www.djangoproject.com/)

**FIM Sentinel** is a professional-grade File Integrity Monitoring (FIM) system built with Python and Django. It acts as a security watchdog for your critical directories, detecting unauthorized changes, modifications, or deletions in real-time.

---

## ✨ Key Features

- **🚀 Real-Time Monitoring**: Detects file changes as they happen using the `watchdog` library.
- **🔍 Cryptographic Proof**: Uses SHA-256 hashing to verify file integrity—no change goes unnoticed.
- **🦠 Malware Detection**: Includes a signature-based engine to flag known threats and suspicious file types (e.g., executables in sensitive folders).
- **📊 Modern Dashboard**: A sleek, dark-mode web interface to manage monitored paths and view audit logs.
- **🛡️ Security Heuristics**: Automatically flags suspicious activities and unauthorized access patterns.
- **📝 Comprehensive Auditing**: Detailed logs of every file event (Created, Modified, Deleted).

---

## 🛠️ Tech Stack

- **Backend**: Python 3.10+, Django 5.0
- **Database**: SQLite (Baseline storage & Audit logs)
- **Hashing**: SHA-256 (Secure Hash Algorithm)
- **Monitoring**: Watchdog (OS Event API)
- **UI**: Django Templates + Vanilla CSS (Modern Dark Mode)

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/DeepakMurugaNan/File-Integrity-Management.git
cd File-Integrity-Management
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database
```bash
cd fim_project
python manage.py migrate
python manage.py createsuperuser  # Create your admin account
```

### 5. Launch the Application
You can use the built-in GUI launcher for convenience:
```bash
python FIM_Launcher.py
```
Or run the components manually:
- **Dashboard**: `python manage.py runserver`
- **Real-time Watcher**: `python manage.py watch_files`

---

## 📖 Usage Guide

1. **Add Monitored Path**: Log into the Admin Panel (`/admin`) and add a directory you wish to monitor.
2. **Start Monitoring**: Run the Watcher to begin tracking changes.
3. **Analyze Logs**: View the Audit Log section in the Dashboard to see real-time integrity alerts.

---

## 🧪 Testing

The project includes several verification scripts:
- `verify_hasher.py`: Tests the SHA-256 hashing logic.
- `verify_malware.py`: Tests the malware detection signatures.
- `verify_fim_logic.py`: Tests the core detection algorithm.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👤 Author

**Deepak Murugan**
- GitHub: [@DeepakMurugaNan](https://github.com/DeepakMurugaNan)
