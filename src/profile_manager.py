import json
import os


def load_profiles():
    path = "profiles/target_list.json"
    if not os.path.exists(path):
        print("[!] No saved profiles found.")
        return []


    with open(path) as f:
        return json.load(f)


def save_profile(ap):
    path = "profiles/target_list.json"
    os.makedirs("profiles", exist_ok=True)
    profiles = load_profiles()
    profiles.append(ap)


    with open(path, "w") as f:
        json.dump(profiles, f, indent=2)


    print(f"[+] Saved target: {ap['ESSID']} ({ap['BSSID']})")