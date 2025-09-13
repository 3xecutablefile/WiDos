import subprocess
import re
import sys
import time

def detect_interfaces():
    interfaces = []
    try:
        output = subprocess.check_output(["iw", "dev"], text=True)
        phy_interfaces = re.findall(r"phy#(\d+)", output)
        
        for phy in phy_interfaces:
            phy_output = subprocess.check_output(["iw", f"phy{phy}", "info"], text=True)
            if "monitor" in phy_output:
                iface_match = re.search(r"Interface\s+(\w+)", output)
                if iface_match:
                    iface_name = iface_match.group(1)
                    interfaces.append({"name": iface_name, "monitor": True})

    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[!] Failed to run 'iw'. Is wireless-tools installed?")
        sys.exit(1)
        
    # Fallback for interfaces that are already in monitor mode
    try:
        output = subprocess.check_output(["iw", "dev"], text=True)
        mon_interfaces = re.findall(r"Interface\s+(mon\d+)", output)
        for iface in mon_interfaces:
            if not any(d['name'] == iface for d in interfaces):
                 interfaces.append({"name": iface, "monitor": True})
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass # Ignore if iw dev fails here

    return interfaces

def enable_monitor_mode(interface):
    print(f"[*] Enabling monitor mode on {interface}...")
    try:
        subprocess.run(["ip", "link", "set", interface, "down"], check=True)
        subprocess.run(["iw", interface, "set", "monitor", "control"], check=True)
        subprocess.run(["ip", "link", "set", interface, "up"], check=True)
        time.sleep(1) # Give it a second to settle
        return interface
    except subprocess.CalledProcessError:
        print(f"[!] Failed to enable monitor mode on {interface}.")
        return None

def reset_interface(interface):
    print(f"[*] Resetting {interface} to managed mode...")
    try:
        subprocess.run(["ip", "link", "set", interface, "down"], check=True)
        subprocess.run(["iw", interface, "set", "type", "managed"], check=True)
        subprocess.run(["ip", "link", "set", interface, "up"], check=True)
    except subprocess.CalledProcessError:
        print(f"[!] Failed to reset {interface}.")

def switch_adapter(old_iface, new_iface):
    if old_iface:
        reset_interface(old_iface)
    return enable_monitor_mode(new_iface)
