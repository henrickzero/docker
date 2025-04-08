#pip install fastapi uvicorn pytchat

from fastapi import FastAPI
from pydantic import BaseModel
import pytchat
import uvicorn

app = FastAPI()

class LiveChatRequest(BaseModel):
    id_da_live: str

@app.post("/live-chat/")
def get_live_chat(req: LiveChatRequest):
    try:
        # Use LiveChatAsync para evitar o erro com signal()
        chat = pytchat.LiveChatAsync(video_id=req.id_da_live)

        # Coleta a primeira mensagem
        data = chat.get()
        if data.items:
            msg = data.items[0]
            return {"author": msg.author.name, "message": msg.message}

        return {"message": "Nenhuma mensagem no momento"}

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("Rodando o servidor FastAPI...")
    uvicorn.run(app, host="0.0.0.0", port=8001)