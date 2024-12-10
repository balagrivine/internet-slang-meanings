from fastapi import FastAPI, Request, APIRouter, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from .database import db_conn

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).parent / 'templates')

@router.get("/status")
async def health_check():
    return {"status": "healthy"}

@router.get("/", response_class=HTMLResponse)
async def get_view(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/decode", response_class=HTMLResponse)
async def decode_slang(request: Request, slang: str = Form(...)):
    slang = slang.upper() # Convert to uppercase to match database records
    
    slang_meaning = db_conn.get_slang_meaning(slang)

    meaning = slang_meaning[0] if slang_meaning else "Meaning not found"

    return templates.TemplateResponse("index.html", {"request": request, "slang": slang, "meaning": meaning})
