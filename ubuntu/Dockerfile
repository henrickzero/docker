FROM ubuntu:24.04

# Evita prompts interativos durante a instalação
ENV DEBIAN_FRONTEND=noninteractive

# Atualiza e instala pacotes necessários
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y ubuntu-desktop \
                       tigervnc-standalone-server \
                       tigervnc-common \
                       dbus-x11 \
                       gnome-flashback \
                       metacity \
                       gnome-terminal \
                       nautilus && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Cria um usuário padrão (user) com senha 'password' (altere para algo seguro)
RUN useradd -m -s /bin/bash user && \
    echo "user:password" | chpasswd && \
    usermod -aG sudo user

# Configura o VNC para o usuário
USER user
RUN mkdir -p /home/user/.vnc && \
    echo "password" | vncpasswd -f > /home/user/.vnc/passwd && \
    chmod 600 /home/user/.vnc/passwd

# Arquivo xstartup para iniciar o GNOME Flashback
RUN echo '#!/bin/sh\n\
xrdb $HOME/.Xresources\n\
xsetroot -solid grey\n\
export XKL_XMODMAP_DISABLE=1\n\
export XDG_CURRENT_DESKTOP="GNOME-Flashback:GNOME"\n\
export XDG_MENU_PREFIX="gnome-flashback-"\n\
gnome-session --session=gnome-flashback-metacity --disable-acceleration-check &' > /home/user/.vnc/xstartup && \
    chmod +x /home/user/.vnc/xstartup

# Volta para root
USER root

# Expõe a porta VNC padrão (5901 para display :1)
EXPOSE 5901

# Inicia o VNC server como o usuário 'user'
CMD ["su", "-", "user", "-c", "vncserver :1 -depth 24 -geometry 1280x800"]