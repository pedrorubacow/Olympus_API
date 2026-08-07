#!/bin/bash
set -euo pipefail

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }

show_help() {
    echo "Uso: ./scripts/test.sh [-h]"
    echo ""
    echo "Roda a suite de testes da Olympus API."
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

log_info "Rodando testes... (placeholder ate a Fase 3/12)"
echo "TODO: substituir por 'pytest' quando os testes existirem"
