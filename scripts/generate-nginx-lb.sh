#!/bin/bash
set -euo pipefail

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }

UPSTREAM_CONF="/etc/nginx/conf.d/olympus-upstream.conf"

show_help() {
    echo "Uso: ./scripts/generate-nginx-lb.sh -p \"5001 5002 5003\""
    echo ""
    echo "Gera o bloco upstream do Nginx com as portas informadas,"
    echo "testa a config e so recarrega o Nginx se a config for valida."
}

PORTS=""

while getopts ":p:h" opt; do
    case $opt in
        p) PORTS="$OPTARG" ;;
        h) show_help; exit 0 ;;
        \?) log_error "Opcao invalida: -$OPTARG"; show_help; exit 1 ;;
        :) log_error "A opcao -$OPTARG precisa de um argumento."; exit 1 ;;
    esac
done

if [ -z "$PORTS" ]; then
    log_error "Nenhuma porta informada. Use -p \"5001 5002 5003\"."
    show_help
    exit 1
fi

log_info "Gerando upstream para as portas: $PORTS"

{
    echo "upstream olympus_backend {"
    for port in $PORTS; do
        echo "    server 127.0.0.1:${port};"
    done
    echo "}"
} | sudo tee "$UPSTREAM_CONF" > /dev/null

log_info "Testando configuracao do Nginx..."
if sudo nginx -t; then
    log_info "Config valida. Recarregando Nginx..."
    sudo systemctl reload nginx
    log_info "Nginx recarregado com backends: $PORTS"
else
    log_error "Config invalida! Nginx NAO foi recarregado. Corrija o problema."
    exit 1
fi
