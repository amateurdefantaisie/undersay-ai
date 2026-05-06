import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)
# Correction ici : Utilisation de 'gemini-pro' qui est la version stable
model = genai.GenerativeModel('gemini-pro')

try:
    with open("knowledge.txt", "r", encoding="utf-8") as f:
        context = f.read()
except FileNotFoundError:
    context = "L'agence Amateur De Fantaisie est une agence numérique de pointe."

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Msg(BaseModel):
    text: str

@app.get("/")
async def get_index():
    return FileResponse('index.html')

@app.post("/chat")
async def chat_endpoint(msg: Msg):
    system_prompt = f"Tu es Undersay, l'IA d'Amateur De Fantaisie. Contexte : {context}"
    try:
        # On envoie le tout au modèle
        response = model.generate_content(system_prompt + "\nUtilisateur: " + msg.text)
        return {"reply": response.text}
    except Exception as e:
        # Si ça échoue encore, on essaie une méthode plus directe
        return {"reply": "Désolé, j'ai un petit souci de connexion à mon cerveau. Réessaie dans un instant !"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)