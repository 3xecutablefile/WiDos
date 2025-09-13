def match_fingerprint(ap):
    known = {
        "TP-LINK": "China - SOHO router",
        "NETGEAR": "USA - Home/Business",
        "Huawei": "China - Carrier gear",
        "Cisco": "Enterprise AP",
        "Ubiquiti": "Pro WiFi"
    }

    essid = ap.get("ESSID", "").upper()
    for tag, desc in known.items():
        if tag in essid:
            print(f"[+] Matched fingerprint: {desc} ({tag})")
            return desc

    print("[-] No fingerprint match.")
    return "Unknown"