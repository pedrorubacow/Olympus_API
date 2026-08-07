#!/bin/bash
set -euo pipefail

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }

show_help() {
    echo "Uso: ./scripts/run.sh [-h]"
    echo ""
    echo "Sobe a Olympus API localmente."
}

while getopts ":h" opt; do
    case $opt in
        h) show_help; exit 0 ;;
        \?) log_error "Opcao invalida: -$OPTARG"; show_help; exit 1 ;;
    esac
done

if [ ! -d "venv" ]; then
    log_error "venv nao encontrado. Rode ./scripts/setup.sh primeiro."
    exit 1
fi

log_info "Ativando ambiente virtual..."
# shellcheck disable=SC1091
source venv/bin/activate

export FLASK_APP=app.py
export FLASK_RUN_HOST=0.0.0.0
log_info "Iniciando a aplicacao em http://0.0.0.0:5000 ..."
flask run
