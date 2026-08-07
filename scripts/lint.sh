#!/bin/bash
set -euo pipefail

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }

show_help() {
    echo "Uso: ./scripts/lint.sh [-h]"
    echo ""
    echo "Roda lint nos scripts Bash (shellcheck) e no codigo Python (Fase 3)."
}

while getopts ":h" opt; do
    case $opt in
        h) show_help; exit 0 ;;
        \?) log_error "Opcao invalida: -$OPTARG"; show_help; exit 1 ;;
    esac
done

if command -v shellcheck &> /dev/null; then
    log_info "Rodando shellcheck nos scripts..."
    shellcheck scripts/*.sh
    log_info "Shellcheck ok."
else
    log_warn "shellcheck nao instalado, pulando lint dos scripts Bash."
fi

log_info "Lint do Python... (placeholder ate a Fase 3)"
echo "TODO: substituir por 'flake8' ou 'ruff' quando app/ existir"
