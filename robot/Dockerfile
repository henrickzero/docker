# Usa a imagem base com interface gráfica
FROM dorowu/ubuntu-desktop-lxde-vnc


# Adiciona a chave GPG do Google corretamente (Novo método)
RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg

# Adiciona o repositório do Chrome com a chave GPG correta
RUN echo "deb [signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb stable main" \
    | tee /etc/apt/sources.list.d/google-chrome.list


# Atualiza pacotes básicos e instala dependências essenciais
RUN apt-get update && apt-get install -y \
    curl wget gnupg python3 python3-pip python3-venv python3-dev python3-tk \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Atualiza os pacotes novamente
RUN apt-get update

RUN apt install gnome-screenshot -y

#RUN sudo apt install tesseract-ocr -y

RUN pip install fastapi
RUN pip install pyautogui
RUN pip install uvicorn
RUN pip install pillow
RUN pip install --upgrade pillow
RUN pip install pymongo
#RUN pip install opencv-python
#RUN pip install opencv-python-headless
#RUN pip install pytesseract

# Atualiza pacotes básicos e instala Python
EXPOSE 8000

# Copia o script da API para o container
COPY app.py /home/ubuntu/app.py
COPY entrypoint.sh /home/ubuntu/entrypoint.sh

RUN mkdir -p /etc/opt/chrome/policies/managed
COPY disable_translate.json /etc/opt/chrome/policies/managed/disable_translate.json

ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


# RUN chmod +x /home/ubuntu/entrypoint.sh


# Comando para iniciar o ambiente gráfico e a API
#CMD ["/bin/bash", "-c", "python /app.py]
