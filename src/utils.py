import subprocess
import shutil
import time
import os


def clear_screen():
    subprocess.call("clear" if shutil.which("clear") else "cls", shell=True)


def wait_for_key():
    try:
        input("[+] Press Enter to continue...")
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")
        time.sleep(1)
        exit(0)

def run_cmd(cmd, silent=True):
    if silent:
        return subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return subprocess.run(cmd)

def check_dependency(bin):
    if shutil.which(bin) is None:
        print(f"[!] Missing dependency: {bin}")
        return False
    return True

def ensure_dependencies(binaries):
    for bin in binaries:
        if not check_dependency(bin):
            print(f"[!] Please install: {bin}")
            return False
    return True

def get_timestamp():
    return time.strftime("%Y%m%d-%H%M%S")

def create_dir(path):
    os.makedirs(path, exist_ok=True)
