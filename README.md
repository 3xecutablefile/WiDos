# EZWiFi

**EZWiFi** is an interactive, modular wireless attack framework built for professional operators. It automates reconnaissance, scoring, handshake/PMKID capture, multi-tool cracking, and rogue AP deployment.

## ⚔️ Features

* 🔍 Interface detection + monitor mode activation
* 📡 AP + client scanning with scoring system
* 🧠 Full Assault Mode: Deauth → PMKID → WPS → Rogue AP
* 🔓 WPA2 + PMKID cracking with aircrack-ng, hashcat, john
* 🗂 Profile-based target saving/loading
* ⚙ Configurable cracking strategy (`config.yaml`)
* 📶 Adapter selection + monitor-mode capability check
* 🧼 Auto-cleanup and reset (scan\_clean.sh + iface\_reset.sh)
* 🧪 Optional WPS brute-force (via bully)
* 🧙 Rogue AP & Evil Twin attack modules

## 📦 Requirements

* Linux only (tested on Kali, Parrot, Ubuntu)
* Wi-Fi adapter with monitor mode + injection support
* Python 3.7+
* Tools: `aircrack-ng`, `hashcat`, `john`, `iw`, `hostapd`, `hcxpcapngtool`, `cap2hccapx`, `bully`

## 🚀 Usage

```bash
sudo python3 main.py
```

1. Choose interface
2. Scan + score targets
3. Select target
4. Choose attack method or enable Full Assault Mode
5. Sit back. Watch the system hunt.

## 🗃 Structure

```
EZWiFi/
├── main.py
├── config.yaml
├── interface_manager.py
├── scanner.py
├── client_score.py
├── deauth_controller.py
├── handshake_sniper.py
├── cracker.py
├── profile_manager.py
├── rogue_ap.py
├── evil_twin.py
├── wps_attack.py
├── fingerprint_match.py
├── logger.py
├── utils.py
├── utils/
│   ├── iface_reset.sh
│   └── scan_clean.sh
├── profiles/
│   └── target_list.json
├── logs/
└── README.md
```

## 🧠 Creator

**`3xecutablefile`** — Built with no limits.

## 🛑 Disclaimer

**For authorized security testing, CTFs, or lab use only.**
Misuse of this tool is your responsibility.