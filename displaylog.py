import pandas as pd
from tabulate import tabulate

LOG_FILE = "honeypot_log.csv"

def display_logs():
    try:
        df = pd.read_csv(LOG_FILE)

        if df.empty:
            print("[!] Log file is empty.")
            return

        # Show logs in a nice table
        print("\n=== Honeypot Logs ===\n")
        print(tabulate(df, headers="keys", tablefmt="pretty", showindex=False))

        # Summary
        print("\n=== Summary ===")
        print(f"Total attempts: {len(df)}")
        print("\nTop 5 attacker IPs:")
        print(df['IP'].value_counts().head().to_string())
        print("\nTop 5 targeted ports:")
        print(df['Port'].value_counts().head().to_string())

    except FileNotFoundError:
        print("[!] No log file found. Run honeypot.py first to generate logs.")
    except Exception as e:
        print(f"[!] Error reading logs: {e}")

if __name__ == "__main__":
    display_logs()
