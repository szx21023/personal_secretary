from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix=f"/frontend", tags=["frontend"])
templates = Jinja2Templates(directory="frontend_fastapi/templates")

@router.get("", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@router.get("/list", response_class=HTMLResponse)
async def list_form(request: Request):
    return templates.TemplateResponse("list.html", {"request": request})