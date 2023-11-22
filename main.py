from fastapi import FastAPI, Request, Form, Path
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from hasher import get_message_hash
from schemas import Message

app: FastAPI = FastAPI()
messages: list[Message] = []
templates: Jinja2Templates = Jinja2Templates(directory='templates')


@app.post('/create', response_class=RedirectResponse)
async def create_message(
        request: Request,
        secret_key: str = Form(...),
        message: str = Form(...)
):
    message_hash: str = get_message_hash(message, secret_key)
    message: Message = Message(message=message, message_hash=message_hash, message_salt=secret_key)
    messages.append(message)

    return templates.TemplateResponse('message_info.html', context={'request': request, 'message_hash': message_hash})


@app.post('/get')
async def get_message(
        request: Request,
        secret_key: str = Form(...),
        message_hash: str = Form(...)
):
    for message in messages:
        if message.message_hash == message_hash and message.message_salt == secret_key:
            response_message = message.message
            messages.remove(message)
            return templates.TemplateResponse('message.html', context={
                'request': request,
                'message': response_message
            })

    return RedirectResponse('/', 302)


@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    context = {'request': request, 'title': 'Secret Message', 'message': 'Secret Message service'}
    return templates.TemplateResponse('index.html', context)
