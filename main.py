import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
import torch
from fastapi.middleware.cors import CORSMiddleware

# 1. FastAPI App initialize karna
app = FastAPI(title="Hikmah AI Cloud Backend")

# 2. CORS Setting: Ye boht zaroori hai taake mobile app cloud se connect ho sake
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Sab origins ko ijazat dena
    allow_credentials=True,
    allow_methods=["*"], # GET, POST sab allow karna
    allow_headers=["*"],
)

# 3. AI Model load karna (Semantic Search ke liye)
# Jab ye pehli baar chalega, model download hone mein thora waqt lagega
print("AI Model loading...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model Ready!")

class ChatRequest(BaseModel):
    text: str

# Health Check: Check karne ke liye ke server on hai ya nahi
@app.get("/")
def health_check():
    return {"status": "Hikmah AI is Online and Running on Cloud"}

# Chat Endpoint: Yahan se mobile app baat karegi
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        user_input = request.text
        
        if not user_input:
            raise HTTPException(status_code=400, detail="Empty message")

        # Filhal dummy response, jab dataset aayega toh hum semantic search use karenge
        # Lekin backend ka dhancha (structure) professional ho gaya hai
        response_text = f"Hikmah AI: JazakAllah! Main aapke sawal '{user_input}' ka jawab jald hi dataset se nikalunga."
        
        return {
            "response": response_text,
            "status": "success",
            "source": "Cloud Intelligence"
        }
    except Exception as e:
        print(f"Error: {e}")
        return {"response": "System mein error hai, dobara koshish karein.", "status": "error"}

# 4. Running Logic: Ye part Render/Cloud ke liye boht zaroori hai
if __name__ == "__main__":
    import uvicorn
    # Cloud platforms 'PORT' environment variable provide karte hain
    port = int(os.environ.get("PORT", 8000))
    # host 0.0.0.0 ka matlab hai ke ye poore internet par listen karega
    uvicorn.run(app, host="0.0.0.0", port=port)