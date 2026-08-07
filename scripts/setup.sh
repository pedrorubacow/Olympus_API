#!/bin/bash
set -euo pipefail

echo "Verificando Python 3..."
if ! command -v python3 &> /dev/null; then
    echo "Erro: python3 nao encontrado. Instale antes de continuar." >&2
    exit 1
fi

echo "Criando ambiente virtual..."
python3 -m venv venv

echo "Ativando ambiente virtual..."
source venv/bin/activate

echo "Instalando dependencias..."
pip install -r requirements.txt

echo "Setup concluido com sucesso!"
