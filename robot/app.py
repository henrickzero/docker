import subprocess

# Executa os comandos do X11 para corrigir a autenticação
subprocess.run("xauth generate :1 . trusted", shell=True)
subprocess.run("xauth add :1 . $(mcookie)", shell=True)

from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pyautogui
import uvicorn
from pymongo import MongoClient
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
import time

first = 0 

# Variável global para armazenar pares chave-valor
global_store = {}

class GenericRequest(BaseModel):
    id: Optional[int] = None
    type: Optional[str] = None
    url: Optional[str] = None
    x: Optional[int] = None
    y: Optional[int] = None
    duration: Optional[float] = None
    event: Optional[str] = None
    text: Optional[str] = None
    deltaY: Optional[int] = None
    key: Optional[str] = None
    time: Optional[datetime] = None

class MapRequest(BaseModel):
    key: Optional[str] = None
    value: Optional[str] = None


clientDb = MongoClient("mongodb://mongo:27017/")
db = clientDb["robo"]
 

print("Iniciando o script...")
app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "http://localhost:80",
    "http://127.0.0.1:80",
    "*"
]
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Replace with the Angular app's URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
print("Iniciando o FastAPI...")

@app.get("/")
def home():
    return {"message": "API de Automação Remota Ativa"}


# for (let i = 0; i < sessionStorage.length; i++) {
#   const key = sessionStorage.key(i);
#   const value = sessionStorage.getItem(key);

#   fetch('http://127.0.0.1:8000/set_value', {
#     method: 'POST',
#     headers: {
#       'Content-Type': 'application/json'
#     },
#     body: JSON.stringify({ key, value })
#   })
#   .then(res => res.json())
#   .then(data => console.log(`Enviado ${key}:`, data))
#   .catch(err => console.error(`Erro ao enviar ${key}:`, err));
# }

# Endpoint para armazenar chave e valor na variável global
@app.post("/set_value/")
def set_value(map: MapRequest):
    global_store[map.key] = map.value
    return {"status": "Valor armazenado", "key": map.key, "value": map.value}

# Endpoint para recuperar valor da variável global por chave
@app.get("/get_value/{key}")
def get_value(key: str):
    value = global_store.get(key, None)
    return {"key": key, "value": value}


@app.post("/generic")
def generic(generics: List[GenericRequest]):
    newTime = 0
    for item in generics:
        millis = int(item.time.microsecond / 1000)
        if newTime==0:
            newTime = item.time
        else:
            delta = item.time - newTime
            millis = int(delta.total_seconds() * 1000)
            newTime = item.time     
            print(item.id)  
            print(millis)
            time.sleep(millis / 1000)


        if item.type == 'open':
            open(item)
        elif item.type == 'move_mouse_and_click':
            move_mouse_and_click(item.x, item.y, item.duration, item.event)
        elif item.type == 'move_mouse':
            move_mouse(item.x, item.y, item.duration)
        elif item.type == 'text':
            type_text(item.text)
        elif item.type == 'scroll':
            scroll(item.deltaY)
        elif item.type == 'press':
            press_key(item.key)
        elif item.type == 'hotkey':
            hotkey(item.text)
    return {"status": "generic"}


@app.post("/open")
def open(request: GenericRequest):
    return openUrl(request.url)

def openUrl(url: str): 
    # if(first == 1):
    #     pyautogui.hotkey('ctrl', 'w')

    subprocess.Popen(["sudo", 
    "google-chrome-stable", 
    "--user-data-dir=/tmp/chrome-profile",
    "--no-sandbox",
    "--disable-features=AutoUpdate", 
    "--disable-dev-shm-usage",
    # "--disable-gpu",
    "--disable-extensions", 
    "--no-default-browser-check", 
    "--no-first-run", 
    "--disable-translate", 
    "--force-device-scale-factor=0.8", 
    "--start-fullscreen",
     "--test-type",
     "--disable-infobars",
     "--disable-save-password-bubble",
     "--password-store=basic",
    url])
    # first = 1
    pyautogui.hotkey('f11')
    return {"status": "open"}


@app.get("/screenshot")
def screenshot():
    file_path = "screenshot.png"
    pyautogui.screenshot().save(file_path)
    return FileResponse(file_path, media_type="image/png")

@app.post("/move_mouse_and_click/")
def move_mouse_and_click(x: int, y: int, duration: float = 1.0, event: str = 'left'):
    print("move_mouse")
    pyautogui.moveTo(x, y, duration=duration)
    pyautogui.click(button=event)
    return {"status": "Mouse movido", "x": x, "y": y, "duration": duration}

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

@app.post("/text/")
def type_text(text: str):
    pyautogui.write(text, interval=0.1)
    return {"status": "Texto digitado", "text": text}

@app.post("/hotkey/")
def hotkey(key: str):
    pyautogui.hotkey(key)
    return {"status": "HotKey", "key": key}

@app.post("/scroll/")
def scroll(deltaY: int):
    if (deltaY < 0):
        pyautogui.press('up')
    else:
        pyautogui.press('down')
    
    return {"status": "Scroll", "deltaY": deltaY}

@app.post("/open")
def open(request: GenericRequest):
    return openUrl(request.url)


# @app.get("/getx")
# def getz(key: key):
#     pyautogui.hotkey('ctrl', 'shift', 'l')
#     return {"status": "get"}

@app.get("/getvalue")
def getValue():
    pyautogui.hotkey('ctrl', 'shift', 'j')
    return {"status": "get"}


@app.post("/press/")
def press_key(key: str):
    if key == 'ArrowLeft':
        pyautogui.press('left')
    elif key == 'ArrowRight':
        pyautogui.press('right')
    elif key == 'ArrowUp':
        pyautogui.press('up')
    elif key == 'ArrowDown':
        pyautogui.press('down')
    elif key == '':
        pyautogui.press('space')
    else:
        pyautogui.press(key)    
    return {"status": "Tecla pressionada", "key": key}

# subprocess.Popen(["firefox","--kiosk", "https://www.investidor.b3.com.br/login?utm_source=B3_MVP&utm_medium=HM_PF&utm_campaign=menu"])


subprocess.Popen(["sudo", 
"google-chrome-stable", 
"--user-data-dir=/tmp/chrome-profile",
"--no-sandbox",
"--disable-features=AutoUpdate", 
# "--disable-gpu",
"--disable-extensions", 
"--no-default-browser-check", 
"--no-first-run", 
"--disable-translate", 
"--force-device-scale-factor=0.8", 
# "--kiosk", 
"--start-fullscreen",
"--test-type",
"--disable-infobars",
"--disable-dev-shm-usage",
"--disable-save-password-bubble",
"--password-store=basic",
"https://www.google.com"])

pyautogui.hotkey('f11')




subprocess.Popen(["python","/home/ubuntu/stream.py"])

if __name__ == "__main__":
    print("Rodando o servidor FastAPI...")
    uvicorn.run(app, host="0.0.0.0", port=8000)