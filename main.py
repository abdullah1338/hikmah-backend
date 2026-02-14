import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from fastapi.middleware.cors import CORSMiddleware

# 1. FastAPI initialize karna
app = FastAPI()

# CORS allow karna taake mobile app connect ho sake
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Model ko "Halka" tareeqay se load karna
# Hum sirf CPU version load karenge taake RAM kam kharch ho
print("Halka AI Model load ho raha hai...")
try:
    # 'all-MiniLM-L6-v2' sabse chota aur tez model hai
    model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
    print("Model Successfully Loaded!")
except Exception as e:
    print(f"Model Load Error: {e}")
    model = None

class ChatRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"status": "Hikmah AI is Online", "model_loaded": model is not None}

@app.post("/chat")
async def chat(request: ChatRequest):
    if model is None:
        return {"response": "System thori dair mein tayyar ho jaye ga. Dubara koshish karein."}
    
    user_input = request.text
    # Filhal simple response, data integration hum end mein karenge
    return {
        "response": f"Hikmah AI (Cloud): Aapne pucha '{user_input}'. Main live hoon aur aapka sawal mujh tak pahunch gaya hai.",
        "source": "Cloud Server"
    }

# 3. Port setting (Koyeb/Render ke liye zaroori)
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
