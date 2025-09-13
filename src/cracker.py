import subprocess
import os
from src.config_manager import load_config

HASH_MODES = {
    "WPA2": "2500",  # WPA/WPA2
    "PMKID": "16800" # WPA-PMKID-PBKDF2
}

def crack_hash(hash_file, hash_type):
    config = load_config()
    if not config:
        print("[!] Cracking failed: Could not load config.")
        return

    wordlist = config.get("cracking", {}).get("wordlist")
    if not wordlist or not os.path.exists(wordlist):
        print(f"[!] Wordlist not found: {wordlist}")
        return

    priority = config.get("cracking", {}).get("priority", [])
    
    print(f"[*] Starting crack for {hash_type} hash: {hash_file}")
    print(f"[*] Cracking priority: {', '.join(priority)}")

    for method in priority:
        print(f"[*] Trying method: {method}")
        if method == "hashcat":
            if _crack_with_hashcat(hash_file, hash_type, wordlist):
                return True
        elif method == "john":
            if _crack_with_john(hash_file, hash_type, wordlist):
                return True
        elif method == "aircrack":
            if hash_type == "WPA2": # aircrack only supports .cap files
                if _crack_with_aircrack(hash_file, wordlist):
                    return True
            else:
                print("[-] aircrack-ng does not support PMKID hashes. Skipping.")
    
    print("[-] Exhausted all cracking methods. Password not found.")
    return False

def _crack_with_hashcat(hash_file, hash_type, wordlist):
    hash_mode = HASH_MODES.get(hash_type)
    if not hash_mode:
        print(f"[-] hashcat does not support hash type: {hash_type}")
        return False

    # Convert .cap to .hccapx for hashcat if needed
    if hash_type == "WPA2" and hash_file.endswith(".cap"):
        hccapx_file = hash_file.replace(".cap", ".hccapx")
        print("[*] Converting .cap to .hccapx for hashcat...")
        try:
            subprocess.run(["cap2hccapx", hash_file, hccapx_file], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            hash_file = hccapx_file
        except (FileNotFoundError, subprocess.CalledProcessError):
            print("[-] Failed to convert .cap to .hccapx. Skipping hashcat.")
            return False

    print("[*] Cracking with hashcat...")
    result = subprocess.run([
        "hashcat", "-m", hash_mode, hash_file, wordlist,
        "--force", "--potfile-path", "cracked.pot", "--status"
    ], capture_output=True, text=True)

    if "Status...........: Cracked" in result.stdout or "Status...........: Exhausted" in result.stdout:
         # Check potfile for cracked password
        potfile_content = subprocess.check_output(["hashcat", "--show", "-m", hash_mode, hash_file], text=True)
        if potfile_content.strip():
            print("[+] Key Found with hashcat!")
            print(potfile_content)
            return True
    
    print("[-] Key not found with hashcat.")
    return False

def _crack_with_john(hash_file, hash_type, wordlist):
    if hash_type == "WPA2" and hash_file.endswith(".cap"):
        john_hash_file = hash_file.replace(".cap", ".johnhash")
        print("[*] Converting .cap to John the Ripper format...")
        try:
            # Using hcxpcapngtool as it's more robust
            subprocess.run(["hcxpcapngtool", "-o", john_hash_file, hash_file], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            hash_file = john_hash_file
        except (FileNotFoundError, subprocess.CalledProcessError):
            print("[-] Failed to convert .cap to John format. Skipping John the Ripper.")
            return False
    elif hash_type == "PMKID":
        # John can read the .16800 format directly if it's in the right format.
        # The format should be: essid:$pmkid
        # hcxpcapngtool should produce this format.
        pass


    print("[*] Cracking with John the Ripper...")
    try:
        subprocess.run(["john", hash_file, f"--wordlist={wordlist}"], check=True)
        
        # Check if cracked
        result = subprocess.run(["john", "--show", hash_file], capture_output=True, text=True)
        if result.stdout and "0 passwords cracked" not in result.stdout:
            print("[+] Key Found with John the Ripper!")
            print(result.stdout)
            return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("[-] John the Ripper failed or not installed.")
        return False

    print("[-] Key not found with John the Ripper.")
    return False

def _crack_with_aircrack(cap_file, wordlist):
    print("[*] Cracking with aircrack-ng...")
    try:
        result = subprocess.run([
            "aircrack-ng", cap_file,
            "-w", wordlist
        ], capture_output=True, text=True, check=True)

        if "KEY FOUND!" in result.stdout:
            print("[+] Key Found with aircrack-ng!")
            print(result.stdout.split("KEY FOUND!")[-1])
            return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("[-] aircrack-ng failed or not installed.")
        return False

    print("[-] Key not found with aircrack-ng.")
    return False
