from datetime import datetime
from fastapi import APIRouter, Body, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from utils import return_response

router = APIRouter(prefix=f"/frontend", tags=["frontend"])
templates = Jinja2Templates(directory="frontend_fastapi/templates")

@router.get("", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})
