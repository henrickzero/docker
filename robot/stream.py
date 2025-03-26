# pip install flask opencv-python pyautogui numpy

from flask import Flask, Response
import cv2
import time
import pyautogui
import numpy as np

app = Flask(__name__)

def generate_frames():
    while True:
        # Captura a tela usando pyautogui
        screenshot = pyautogui.screenshot()

        # Converte para array NumPy
        frame = np.array(screenshot)

        # Converte de RGB (Pillow) para BGR (OpenCV)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Codifica a imagem em JPEG
        _, buffer = cv2.imencode('.jpg', frame)

        # Gera o frame para o stream
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

        time.sleep(0.1)  # Taxa de atualização (~10 FPS)

@app.route('/video')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
