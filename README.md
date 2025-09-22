# Python Honeypot

A simple honeypot that listens on multiple ports, logs connection attempts, and enriches them with IP geolocation. Built for learning cybersecurity and networking fundamentals.

## ✨ Features
- Listens on configurable TCP ports  
- Logs: timestamp, IP, port, country, region, city  
- CSV-based logging (thread-safe)  
- Viewer script for organized summaries  

## 🚀 Quick Start
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
pip install -r requirements.txt
python honeypot.py
```
Test with:
```bash
telnet 127.0.0.1 2222
```
in a new terminal..
if accessing from a different device, replace the 127.0.0.1 with the Ip of the targeted system
To view logs:
```bash
python displaylog.py
```

📂 Files
honeypot.py → main honeypot
view_logs.py → display logs in table & summary
requirements.txt → dependencies
honeypot_log.csv → generated log file

