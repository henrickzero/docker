# Usa a imagem oficial do Node-RED (base Alpine)
FROM nodered/node-red:latest

# Alterna para root para instalar pacotes
USER root

# Instala dependências necessárias usando apk (Alpine)
RUN apk add --no-cache \
    python3 \
    make \
    g++ \
    git

# Define o diretório de trabalho do Node-RED
WORKDIR /data

# Instala o pacote do WhatsApp bot
RUN npm install node-red-contrib-whatsappbot --unsafe-perm --no-update-notifier --no-fund --only=production

# Retorna para o usuário padrão do Node-RED
USER node-red

# Expõe a porta do Node-RED
EXPOSE 1880

# Inicia o Node-RED
CMD ["npm", "start", "--", "--userDir", "/data"]