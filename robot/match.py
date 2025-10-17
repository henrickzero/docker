import cv2
import numpy as np

# Carregar as imagens
imagem_maior = cv2.imread('imagem_maior.jpg')
subimagem = cv2.imread('subimagem.jpg')

# Verificar se as imagens foram carregadas corretamente
if imagem_maior is None or subimagem is None:
    print("Erro ao carregar uma ou ambas as imagens.")
    exit()

# Converter as imagens para escala de cinza (opcional, mas pode melhorar a correspondência)
imagem_maior_cinza = cv2.cvtColor(imagem_maior, cv2.COLOR_BGR2GRAY)
subimagem_cinza = cv2.cvtColor(subimagem, cv2.COLOR_BGR2GRAY)

# Aplicar o método de correspondência de padrões
metodo = cv2.TM_CCOEFF_NORMED  # Método de correspondência (normalizado para melhor precisão)
resultado = cv2.matchTemplate(imagem_maior_cinza, subimagem_cinza, metodo)

# Obter o valor máximo de correspondência
_, max_val, _, max_loc = cv2.minMaxLoc(resultado)

# Definir um limiar para considerar uma correspondência válida
limiar = 0.8  # Ajuste conforme necessário (0 a 1, onde 1 é correspondência perfeita)

if max_val >= limiar:
    print("Subimagem encontrada!")
    # Obter as dimensões da subimagem
    h, w = subimagem_cinza.shape
    # Desenhar um retângulo na região correspondente (opcional)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(imagem_maior, top_left, bottom_right, (0, 255, 0), 2)

    # Mostrar a imagem com a região destacada
    cv2.imshow('Resultado', imagem_maior)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Subimagem não encontrada.")