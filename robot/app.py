import subprocess

# Executa os comandos do X11 para corrigir a autenticação
subprocess.run("xauth generate :1 . trusted", shell=True)
subprocess.run("xauth add :1 . $(mcookie)", shell=True)

from fastapi import FastAPI
import pyautogui
from fastapi.responses import FileResponse
import uvicorn
from pymongo import MongoClient

clientDb = MongoClient("mongodb://mongo:27017/")
db = clientDb["robo"]

print("Iniciando o script...")
app = FastAPI()
print("Iniciando o FastAPI...")

@app.get("/")
def home():
    return {"message": "API de Automação Remota Ativa"}

@app.get("/screenshot")
def screenshot():
    file_path = "screenshot.png"
    pyautogui.screenshot().save(file_path)
    return FileResponse(file_path, media_type="image/png")

@app.post("/move_mouse/")
def move_mouse(x: int, y: int, duration: float = 1.0):
    pyautogui.moveTo(x, y, duration=duration)
    return {"status": "Mouse movido", "x": x, "y": y, "duration": duration}

@app.get("/mouse_position")
def get_mouse_position():
    x, y = pyautogui.position()
    return {"x": x, "y": y}

@app.post("/click/")
def click():
    pyautogui.click()
    colecao = db["usuarios"]
    documento = {
        "nome": "Henrique",
        "email": "henrique@email.com",
        "idade": 30
    }
    return {"status": "Clique executado"}

@app.post("/type/")
def type_text(text: str):
    pyautogui.write(text, interval=0.1)
    return {"status": "Texto digitado", "text": text}

@app.post("/press/")
def press_key(key: str):
    pyautogui.press(key)
    return {"status": "Tecla pressionada", "key": key}

# subprocess.Popen(["firefox","--kiosk", "https://www.investidor.b3.com.br/login?utm_source=B3_MVP&utm_medium=HM_PF&utm_campaign=menu"])
subprocess.Popen(["sudo", 
"google-chrome-stable", 
"--no-sandbox",
"--disable-features=AutoUpdate", 
"--disable-dev-shm-usage",
# "--disable-gpu",
"--disable-extensions", 
"--no-default-browser-check", 
"--no-first-run", 
"--disable-translate", 
"--force-device-scale-factor=0.8", 
"--kiosk", 
"https://www.investidor.b3.com.br/login?utm_source=B3_MVP&utm_medium=HM_PF&utm_campaign=menu"])
if __name__ == "__main__":
    print("Rodando o servidor FastAPI...")
    uvicorn.run(app, host="0.0.0.0", port=8000)