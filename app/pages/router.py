from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from app.paste.router import get_paste
from app.profile.router import get_profile
from fastapi.templating import Jinja2Templates
from app.auth.auth import fastapi_users
from database.models import User

router = APIRouter(
    prefix='/pages',
    tags=['Pages']
)

current_user = fastapi_users.current_user(optional=True)

templates = Jinja2Templates(directory='app/templates')


def get_redirect_to_profile(user_id: int):
    url = '/pages/profile/' + str(user_id)
    return RedirectResponse(url)


@router.get('/base')
def get_base_page(request: Request):
    return templates.TemplateResponse(
        'base.html',
        {'request': request}
    )


@router.get('/main')
def get_main_page(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse(
        'main.html',
        {'request': request, 'user': user}
    )


@router.get('/paste/{id_paste}')
def get_paste(request: Request, paste=Depends(get_paste), user: User = Depends(current_user)):
    return templates.TemplateResponse(
        'paste.html',
        {'request': request, 'paste': paste['data'], 'user': user}
    )


@router.get('/registration')
def get_registration_page(request: Request, user: User = Depends(current_user)):
    if user is not None:
        return get_redirect_to_profile(user.id)

    return templates.TemplateResponse(
        'registration.html',
        {'request': request, 'user': user}
    )


@router.get('/login')
def get_login_page(request: Request, user: User = Depends(current_user)):
    if user is not None:
        return get_redirect_to_profile(user.id)

    return templates.TemplateResponse(
        'login.html',
        {'request': request, 'user': user}
    )


@router.get('/profile/{user_id}')
def get_profile_page(user_id: int, request: Request, profile=Depends(get_profile), user: User = Depends(current_user)):
    if user is not None and user_id == user.id:
        template = 'personal_profile.html'
    else:
        template = 'profile.html'

    return templates.TemplateResponse(
        template,
        {'request': request, 'profile': profile['data'], 'user': user}
    )
