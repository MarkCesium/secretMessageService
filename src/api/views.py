from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from src.api import dao
from src.core.db import db_helper
from src.exceptions.files import FileCreateException, FileReadException
from src.utils.flashes import get_flashed_messages, flash


router = APIRouter()
templates: Jinja2Templates = Jinja2Templates(directory="templates")
templates.env.globals["get_flashed_messages"] = get_flashed_messages


@router.post("/create", response_class=RedirectResponse)
async def create_message(
    request: Request,
    secret_key: str = Form(...),
    message: str = Form(...),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        message_hash = await dao.message_create(message, secret_key, session)
    except FileCreateException:
        flash(request, "Failed to create message", "danger")
        return RedirectResponse("/", 302)

    return templates.TemplateResponse(
        "message_info.html", context={"request": request, "message_hash": message_hash}
    )


@router.post("/get")
async def get_message(
    request: Request,
    secret_key: str = Form(...),
    message_hash: str = Form(...),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        message_text = await dao.message_get(message_hash, secret_key, session)
    except FileReadException:
        flash(request, "Failed to read message", "danger")
        return RedirectResponse("/", 302)

    if message_text is None:
        flash(request, "Message not found", "danger")
        return RedirectResponse("/", 302)

    return templates.TemplateResponse(
        "message.html",
        context={"request": request, "message": message_text},
    )


@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    context = {
        "request": request,
        "title": "CesSecrets",
    }
    return templates.TemplateResponse("index.html", context)
