import subprocess

def deploy_rogue_ap(interface, essid="Free_WiFi", channel="6"):
    print(f"[*] Deploying rogue AP: {essid} on ch {channel}")

    config = f"""
interface={interface}
driver=nl80211
ssid={essid}
channel={channel}
"""

    with open("rogue_ap.conf", "w") as f:
        f.write(config)

    try:
        subprocess.run(["hostapd", "rogue_ap.conf"], check=True)
    except FileNotFoundError:
        print("[!] hostapd not found.")
    except subprocess.CalledProcessError:
        print("[!] hostapd failed to start rogue AP.")