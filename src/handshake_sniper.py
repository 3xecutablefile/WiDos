def analyze_handshake(file):
    print(f"[*] Analyzing handshake: {file}")
    try:
        with open(file, 'rb') as f:
            data = f.read()
            if b'WPA' in data or b'EAPOL' in data:
                print("[+] Likely contains WPA/EAPOL handshake.")
                return True
    except Exception as e:
        print(f"[!] Error reading {file}: {e}")
    return False