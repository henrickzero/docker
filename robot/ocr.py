import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from pytesseract import Output
import json

# Carrega a imagem (substitua "imagem.jpg" pelo caminho da sua imagem)
img = cv2.imread("response.png")

# 1. Converter para escala de cinza e binarizar para detectar formas
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Aplicar threshold binário inverso para obter elementos em branco sob fundo preto
_, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

# 2. Encontrar contornos externos na imagem limiarizada
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

elements = []  # lista de elementos interativos detectados

for cnt in contours:
    area = cv2.contourArea(cnt)
    if area < 100:  # ignora contornos muito pequenos (ruído)
        continue
    # Aproxima o contorno para identificar cantos
    peri = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
    # Verifica se o contorno aproximado tem 4 vértices -> possivelmente um retângulo (botão)
    if len(approx) == 4:
        x, y, w, h = cv2.boundingRect(cnt)
        # Ignora contornos que abrangem quase toda a imagem (por exemplo, fundo inteiro)
        if w >= img.shape[1] * 0.9 and h >= img.shape[0] * 0.9:
            continue
        # Adiciona como possível botão (nome será identificado pelo texto interno, se houver)
        elements.append({"tipo": "botão", "nome": "", "posição": (int(x), int(y)), "tamanho": (int(w), int(h))})

# 3. OCR: extrai texto e posições usando Tesseract
data = pytesseract.image_to_data(img, output_type=Output.DICT)  # resultado em formato de dicionário
n = len(data["text"])
for i in range(n):
    text = data["text"][i].strip()
    conf = data["conf"][i] if isinstance(data["conf"][i], int) else -1

    if conf < 0 or text == "":  # ignora entradas sem texto ou de baixa confiança
        continue
    tx, ty, tw, th = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
    # 4. Verifica se este texto está dentro de algum botão identificado
    inside_button = False
    for elem in elements:
        if elem["tipo"] == "botão":
            bx, by = elem["posição"]
            bw, bh = elem["tamanho"]
            # Checa se as coordenadas do texto ficam completamente dentro do contorno do botão
            if tx >= bx and ty >= by and (tx + tw) <= (bx + bw) and (ty + th) <= (by + bh):
                # Associa este texto como nome do botão
                elem["nome"] = (elem["nome"] + " " + text).strip() if elem["nome"] else text
                inside_button = True
                break
    # Se o texto não estiver dentro de nenhum botão, consideramos como link de texto
    if not inside_button:
        elements.append({
            "tipo": "link",
            "nome": text,
            "posição": (int(tx), int(ty)),
            "tamanho": (int(tw), int(th))
        })

# 5. Saída: imprime a lista de elementos em formato JSON
output_json = json.dumps(elements, ensure_ascii=False, indent=2)
print(output_json)
