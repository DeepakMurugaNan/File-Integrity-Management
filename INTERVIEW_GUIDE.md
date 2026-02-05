# Interview Guide: File Integrity Monitoring (FIM) System

## 1. The "Elevator Pitch" (What is it?)
> "I built a File Integrity Monitoring system in Python using Django. It acts as a security watchdog that continuously scans critical directories, calculates cryptographic hashes of files, and detects unauthorized changes—whether that's a hacker modifying a config file, malware adding an executable, or an accidental deletion."

## 2. Technical Architecture (How does it work?)

### The Core Loop
"The system runs on a **detect-and-compare** model:"
1.  **Baseline Phase**: I scan the directory and calculate a SHA-256 hash for every file. This `FileRecord` is stored in a SQLite database as the "source of truth".
2.  **Monitoring Phase**: When the scanner runs again, it recalculates hashes.
3.  **Comparison Logic**:
    *   **New File**: Found on disk but not in DB.
    *   **Modified**: Found in both, but hashes differ.
    *   **Deleted**: Found in DB but not on disk.

### The Stack
*   **Backend**: Django (Framework), Python (Logic).
*   **Database**: SQLite (for storing baselines and audit logs).
*   **Security**: SHA-256 Hashing for integrity proof.
*   **Frontend**: Django Templates + CSS variables for a modern Dark Mode UI.

## 3. Key Features demonstrated
*   **Integrity Verification**: "I used SHA-256 because it's distinct; even a single bit change in a file completely changes the hash."
*   **Malware Detection**: "I implemented a signature matching engine. It checks file hashes against a database of 'Known Bad' signatures (like a simplified Antivirus)."
*   **Heuristics**: "It also flags suspicious behaviors, like executable files (`.exe`, `.bat`) appearing in non-executable directories."

## 4. Challenges & Solutions (Talking Points)
*   **Challenge**: "How do we handle large files efficiently?"
    *   **Solution**: "I used chunked reading (reading 64KB at a time) in the hashing function so we don't load the whole file into RAM."
*   **Challenge**: "How do we know if a file was renamed vs deleted?"
    *   **Current State**: "Right now it sees it as a Delete + New. A future improvement would be to compare hashes of 'New' files against 'Deleted' ones to detect moves."

## 5. Future Improvements (Shows you think ahead)
*   "I would move the scanning to a background worker (like Celery) so it doesn't block the main thread."
*   "I would add real-time OS event listeners (like `Watchdog` library) instead of polling."
