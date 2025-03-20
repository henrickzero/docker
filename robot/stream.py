#pip install flask opencv-python

from flask import Flask, Response
import cv2
import time

app = Flask(__name__)

IMAGE_PATH = "screenshot.png"  # Caminho para a imagem que será atualizada constantemente

def generate_frames():
    while True:
        frame = cv2.imread(IMAGE_PATH)  # Lê a imagem do arquivo
        if frame is None:
            continue  # Evita erros caso a imagem não esteja disponível

        _, buffer = cv2.imencode('.jpg', frame)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

        time.sleep(0.1)  # Atualiza a imagem a cada 100ms (~10FPS)

@app.route('/video')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)