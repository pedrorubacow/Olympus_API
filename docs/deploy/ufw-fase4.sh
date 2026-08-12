#!/bin/bash
# Regras de firewall (ufw) da Fase 4 - Networking & Security
# Reproduz o estado que a EC2 do Olympus API deve ter: nega tudo por padrao,
# libera so o SSH (porta customizada 2222) e o Nginx (80/443).
set -euo pipefail

sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 2222/tcp   # SSH, porta trocada da 22 padrao (ver sshd-hardening.conf)
sudo ufw allow 80/tcp     # Nginx - redireciona pra 443
sudo ufw allow 443/tcp    # Nginx - HTTPS (Flask fica isolada em 127.0.0.1:5000)
sudo ufw --force enable

sudo ufw status verbose
