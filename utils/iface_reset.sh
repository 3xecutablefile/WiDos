#!/bin/bash
IFACE=$1
if [ -z "$IFACE" ]; then
    echo "Usage: $0 <interface>"
    exit 1
fi
sudo ip link set "$IFACE" down
sudo iw "$IFACE" set type managed
sudo ip link set "$IFACE" up
echo "[+] Interface $IFACE reset to managed mode."