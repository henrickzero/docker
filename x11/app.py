from fastapi import FastAPI
import pyautogui
from fastapi.responses import FileResponse

app = FastAPI()

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

@app.post("/click/")
def click():
    pyautogui.click()
    return {"status": "Clique executado"}

@app.post("/type/")
def type_text(text: str):
    pyautogui.write(text, interval=0.1)
    return {"status": "Texto digitado", "text": text}

@app.post("/press/")
def press_key(key: str):
    pyautogui.press(key)
    return {"status": "Tecla pressionada", "key": key}
