import subprocess


def run_wps_attack(interface):
    print("[*] Starting WPS attack with bully...")
    try:
        subprocess.run(["bully", interface], check=True)
    except FileNotFoundError:
        print("[!] bully not found. Install with: apt install bully")
    except subprocess.CalledProcessError:
        print("[!] WPS attack failed or was terminated.")