from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from dotenv import load_dotenv
import os


load_dotenv()

app = FastAPI()

# CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace with specific origin in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Code(BaseModel):
    user_code: str

@app.post("/fix-code")
def fix_code(code: Code):
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="GEMINI_API_KEY not set")

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-pro")

        prompt = f"Detect bugs in this code\n{code.user_code}\n and suggest some fixes \n without using markdown \nOnly provide the corrected version."

        response = model.generate_content(prompt)
        fixed_code = response.text.strip()

        return {
            "original": code.user_code,
            "suggested_fix": fixed_code
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
