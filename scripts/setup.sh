#!/bin/bash
set -euo pipefail

# Cores para o log
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }

show_help() {
    echo "Uso: ./scripts/setup.sh [-h]"
    echo ""
    echo "Prepara o ambiente da Olympus API: cria venv e instala dependencias."
    echo ""
    echo "Opcoes:"
    echo "  -h    Mostra esta ajuda e sai"
}

while getopts ":h" opt; do
    case $opt in
        h)
            show_help
            exit 0
            ;;
        \?)
            log_error "Opcao invalida: -$OPTARG"
            show_help
            exit 1
            ;;
    esac
done

log_info "Verificando Python 3..."
if ! command -v python3 &> /dev/null; then
    log_error "python3 nao encontrado. Instale antes de continuar."
    exit 1
fi

log_info "Criando ambiente virtual..."
python3 -m venv venv

log_info "Ativando ambiente virtual..."
# shellcheck disable=SC1091
source venv/bin/activate

log_info "Instalando dependencias..."
pip install -r requirements.txt

log_info "Setup concluido com sucesso!"
