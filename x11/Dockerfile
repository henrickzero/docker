# Usa a imagem base x11vnc/desktop
FROM x11vnc/desktop

# Define a senha do VNC
ENV X11VNC_PASSWORD=1234


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

RUN apt update && apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt update
RUN apt install -y python3.8 python3.8-venv python3.8-dev python3.8-distutils

RUN update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 2
RUN update-alternatives --config python

# Atualiza os pacotes novamente
#RUN apt-get update

RUN pip3 install fastapi
RUN pip3 install pyautogui


# Expõe as portas do VNC e noVNC
EXPOSE 5900 6080

# Comando para iniciar o servidor X11 e VNC automaticamente
#CMD ["bash", "-c", "/startup.sh && tail -f /dev/null"]
