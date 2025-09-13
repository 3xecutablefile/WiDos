import json
import os
from datetime import datetime


def save_log(data, ap):
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    essid = ap.get("ESSID", "unknown").replace(" ", "_")
    name = f"logs/{essid}_{ts}.json"


    os.makedirs("logs", exist_ok=True)
    with open(name, "w") as f:
        json.dump(data, f, indent=4)


    print(f"[+] Log saved: {name}")