from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

router = APIRouter()

router.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

@router.get("/organization", response_class=HTMLResponse, include_in_schema=False)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="add_org.html"
    )

@router.get("/organization/edit", response_class=HTMLResponse, include_in_schema=False)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="edit_org.html"
    )

@router.get("/project", response_class=HTMLResponse, include_in_schema=False)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="add_pro.html"
    )

@router.get("/project/edit", response_class=HTMLResponse, include_in_schema=False)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="edit_pro.html"
    )