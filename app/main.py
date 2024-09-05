from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from .ai_client import generate_response
from .schemas import ResponseModel
from pathlib import Path

app = FastAPI()

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="a_secret_key_for_session")

# Serve static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def get_homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate/")
async def get_response(request: Request):
    form_data = await request.form()
    prompt = form_data.get("prompt")
    session = request.session

    if "conversation" not in session:
        session["conversation"] = []

    session["conversation"].append({"user": prompt})

    # Construct the conversation history
    conversation_history = ""
    for msg in session["conversation"]:
        if "user" in msg:
            conversation_history += f"User: {msg['user']}\n"
        if "ai" in msg:
            conversation_history += f"AI: {msg['ai']}\n"

    try:
        ai_response = generate_response(conversation_history)
        session["conversation"].append({"ai": ai_response})
        return {
            "response_text": ai_response,
            "conversation": session["conversation"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
