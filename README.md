# EZWiFi

**EZWiFi** is a modular wireless attack framework designed to automate reconnaissance, client scoring, handshake capture, deauthentication, and WPA2 cracking. Built by hackers, for hackers.

## 🔧 Features

* Interface detection and monitor mode activation
* AP scanning with airodump-ng
* Client scoring and interactive targeting
* Handshake-aware deauth loop
* Cracking with aircrack-ng / hashcat / John
* Persistent logging
* Fingerprinting and rogue AP deployment
* Optional WPS brute with bully

## 📦 Requirements

* Linux with wireless chipset supporting monitor mode
* Python 3.7+
* Dependencies:

  * `aircrack-ng`
  * `iw`, `ip`, `hostapd`
  * `hashcat`, `john`, `bully`
  * `hcxpcapngtool`, `cap2hccapx`

## 🚀 Usage

```bash
# Clone the repo
git clone https://github.com/3xecutablefile/WiDos
cd WiDos

# Make the tool executable
chmod +x main.py

# Set up an alias for easier access (Linux shells like bash or zsh)
# For bash:
echo "alias ezwifi='sudo $(pwd)/main.py'" >> ~/.bashrc
source ~/.bashrc

# For zsh:
echo "alias ezwifi='sudo $(pwd)/main.py'" >> ~/.zshrc
source ~/.zshrc

# Run the tool
ezwifi
```

1. Choose a wireless interface
2. Scan for nearby networks
3. Select a target AP
4. Automatic handshake capture begins
5. Cracking starts with selected method

## 🗃 Structure

```
EZWiFi/
├── main.py
├── interface_manager.py
├── scanner.py
├── client_score.py
├── deauth_controller.py
├── cracker.py
├── logger.py
├── utils.py
├── evil_twin.py
├── wps_attack.py
├── fingerprint_match.py
├── handshake_sniper.py
├── rogue_ap.py
├── profiles/
│   └── target_list.json
└── logs/
```

## 📜 License

MIT

## 🧠 Author

`3xecutablefile` — built with zero mercy.
