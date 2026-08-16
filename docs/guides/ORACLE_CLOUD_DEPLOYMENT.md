# 24/7 Oracle Cloud VPS Deployment Guide

[Documentation](../README.md) / [Guides](MONISH_CASE_STUDY.md) / [Oracle Cloud Deployment](ORACLE_CLOUD_DEPLOYMENT.md)

**Step-by-step instructions to deploy Nirixa OS 24/7 on an Oracle Cloud Always-Free Compute Instance (`instance-20260804-2336`) with continuous systemd service persistence.**

---

## 1. Prerequisites

* Oracle Cloud Always-Free Instance (Ubuntu 24.04 LTS / Debian).
* Private SSH Key (`ssh-key-2026-08-04.key`).
* Public IP Address of your Oracle VM.

---

## 2. Connect via SSH

```powershell
# Windows PowerShell
ssh -i .\ssh-key-2026-08-04.key ubuntu@<YOUR_ORACLE_PUBLIC_IP>
```

---

## 3. Remote Host Setup (Single Script)

Once logged into your Ubuntu instance, run:

```bash
# 1. Update packages
sudo apt update && sudo apt upgrade -y

# 2. Install Python 3.11 & Git
sudo apt install -y python3-pip python3-venv git

# 3. Clone Nirixa OS
git clone https://github.com/Monish-Nallagondalla/My-Os.git ~/nirixa-os
cd ~/nirixa-os

# 4. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 5. Configure environment variables
cp system/config/.env.example system/config/.env
nano system/config/.env
# Paste TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID, then press Ctrl+O, Enter, Ctrl+X
```

---

## 4. Set Up Systemd Daemon Service (24/7 Persistence)

Create a systemd unit file so the listener restarts automatically on reboots:

```bash
sudo tee /etc/systemd/system/nirixa.service > /dev/null <<EOF
[Unit]
Description=Nirixa OS 24/7 Background Daemon
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/nirixa-os
ExecStart=/home/ubuntu/nirixa-os/.venv/bin/python /home/ubuntu/nirixa-os/system/scripts/telegram_listener.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and start service
sudo systemctl daemon-reload
sudo systemctl enable nirixa.service
sudo systemctl start nirixa.service
```

---

## 5. Verify 24/7 Service Health

```bash
# Check service status
sudo systemctl status nirixa.service

# View live stream logs
journalctl -u nirixa.service -f
```

Your Nirixa OS Telegram Mobile Gateway is now live 24/7 with zero local laptop battery consumption.
