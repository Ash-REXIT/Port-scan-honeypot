import socket
import threading
import pandas as pd
from datetime import datetime
import pandas.errors
import requests  # ✅ for geolocation

# Ports (safe high-numbered for non-admin use)
PORTS = [2221, 2222, 2223, 8080, 8443, 3307]
LOG_FILE = "honeypot_log.csv"

# Thread lock for safe file access
log_lock = threading.Lock()

# Ensure log file exists and has headers
try:
    pd.read_csv(LOG_FILE)
except (FileNotFoundError, pandas.errors.EmptyDataError):
    df_init = pd.DataFrame(columns=["Timestamp", "IP", "Port", "Country", "Region", "City"])
    df_init.to_csv(LOG_FILE, index=False)

def get_geolocation(ip):
    """Query IP geolocation using ip-api.com"""
    try:
        if ip == "127.0.0.1":  # local testing
            return "Localhost", "-", "-"
        url = f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city"
        res = requests.get(url, timeout=5).json()
        if res.get("status") == "success":
            return res.get("country", "Unknown"), res.get("regionName", "Unknown"), res.get("city", "Unknown")
    except Exception:
        pass
    return "Unknown", "Unknown", "Unknown"

def handle_connection(client_socket, addr, port):
    ip = addr[0]
    print(f"[!] Connection attempt from {ip} on port {port}")

    # Optional: send banner
    try:
        client_socket.sendall(b"Welcome to the honeypot!\r\n")
    except:
        pass

    # Get geolocation
    country, region, city = get_geolocation(ip)

    # Create log row
    new_row = pd.DataFrame([{
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "IP": ip,
        "Port": port,
        "Country": country,
        "Region": region,
        "City": city
    }])

    # Save to CSV (thread-safe)
    with log_lock:
        try:
            df = pd.read_csv(LOG_FILE)
            df = pd.concat([df, new_row], ignore_index=True)
        except (FileNotFoundError, pandas.errors.EmptyDataError):
            df = new_row
        df.to_csv(LOG_FILE, index=False)

    client_socket.close()

def start_honeypot(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("", port))
    server.listen(5)
    print(f"[+] Listening on port {port}")
    while True:
        client_socket, addr = server.accept()
        threading.Thread(target=handle_connection, args=(client_socket, addr, port), daemon=True).start()

if __name__ == "__main__":
    for port in PORTS:
        threading.Thread(target=start_honeypot, args=(port,), daemon=True).start()

    try:
        while True:
            threading.Event().wait(1)
    except KeyboardInterrupt:
        print("\nShutting down.")
