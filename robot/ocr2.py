import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from PIL import Image

# Carregue imagem
img = cv2.imread('screenshot.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detecte contornos (separa elementos)
edges = cv2.Canny(gray, 50, 150)
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Liste elementos
for i, cnt in enumerate(contours):
    x, y, w, h = cv2.boundingRect(cnt)
    roi = img[y:y+h, x:x+w]
    text = pytesseract.image_to_string(Image.fromarray(roi))
    if text.strip():  # Só se houver texto
        print(f"Elemento {i+1}: Posição [{x}, {y}, {w}, {h}], Texto: {text.strip()}")