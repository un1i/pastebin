from fastapi import APIRouter, Request, Depends
from app.paste.router import get_paste
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='/pages',
    tags=['Pages']
)

templates = Jinja2Templates(directory='templates')


@router.get('/base')
def get_base_page(request: Request):
    return templates.TemplateResponse('base.html', {'request': request})


@router.get('/main')
def get_main_page(request: Request):
    return templates.TemplateResponse('main.html', {'request': request})


@router.get('/')
def get_paste(request: Request, paste=Depends(get_paste)):
    return templates.TemplateResponse('paste.html', {'request': request, 'paste': paste['data']})
