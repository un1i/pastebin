from fastapi import APIRouter, Request, Depends
from app.paste.router import get_paste
from fastapi.templating import Jinja2Templates
from app.auth.auth import fastapi_users
from database.models import User

router = APIRouter(
    prefix='/pages',
    tags=['Pages']
)


current_user = fastapi_users.current_user(optional=True)

templates = Jinja2Templates(directory='templates')


@router.get('/base')
def get_base_page(request: Request):
    return templates.TemplateResponse('base.html', {'request': request})


@router.get('/main')
def get_main_page(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse('main.html', {'request': request, 'user': user})


@router.get('/')
def get_paste(request: Request, paste=Depends(get_paste), user: User = Depends(current_user)):
    return templates.TemplateResponse('paste.html', {'request': request, 'paste': paste['data'], 'user': user})


@router.get('/registration')
def get_registration_page(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse('registration.html', {'request': request, 'user': user})


@router.get('/login')
def get_login_page(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse('login.html', {'request': request, 'user': user})
