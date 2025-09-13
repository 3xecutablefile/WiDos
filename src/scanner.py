import subprocess
import csv
import os
import time
from collections import defaultdict

def scan_networks(interface, timeout=10):
    output_prefix = "scan_output"
    output_file = f"{output_prefix}-01.csv"
    print(f"[*] Scanning on {interface} for {timeout} seconds...")

    # Remove old scan files
    for f in os.listdir('.'):
        if f.startswith(output_prefix):
            os.remove(f)

    proc = subprocess.Popen([
        "airodump-ng",
        "--write-interval", "1",
        "--output-format", "csv",
        "-w", output_prefix,
        interface
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    time.sleep(timeout)
    proc.terminate()
    proc.wait()

    aps = []
    clients = defaultdict(int)
    try:
        with open(output_file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            in_client_section = False
            for row in reader:
                if not row:
                    in_client_section = True
                    continue
                
                if not in_client_section:
                    if len(row) >= 14 and row[0].strip() != 'BSSID':
                        try:
                            power = int(row[8].strip())
                            aps.append({
                                "BSSID": row[0].strip(),
                                "channel": row[3].strip(),
                                "ESSID": row[13].strip(),
                                "power": power,
                                "clients": 0  # Default to 0
                            })
                        except (ValueError, IndexError):
                            continue
                else:
                    if len(row) >= 6 and row[0].strip() != 'Station MAC':
                        ap_bssid = row[5].strip()
                        clients[ap_bssid] += 1

    except FileNotFoundError:
        print(f"[!] Scan output file not found: {output_file}")
        return []
    except Exception as e:
        print(f"[!] Failed to parse scan CSV: {e}")

    # Add client counts to APs
    for ap in aps:
        ap['clients'] = clients[ap['BSSID']]

    if not aps:
        print("[!] No networks found.")
    
    return aps