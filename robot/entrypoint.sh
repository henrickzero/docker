#!/bin/bash
set -e  # Faz o script falhar se qualquer comando falhar

# Configurar X11 corretamente
echo "Configurando X11..."
xauth generate :0 . trusted
xauth add :0 . $(mcookie)

# Exibir variáveis de ambiente (debug)
echo "DISPLAY é: $DISPLAY"
echo "RESOLUTION é: $RESOLUTION"

# Rodar a aplicação
echo "Iniciando o FastAPI..."
exec python3 /app.py
