from fastapi import Request
from fastapi.exceptions import HTTPException, RequestValidationError
from pages.router import templates


async def not_found_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        '404.html',
        {'request': request, 'info': exc.detail},
        status_code=exc.status_code,
    )


async def unprocessable_content_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        '422.html',
        {'request': request, 'info': exc.detail},
        status_code=exc.status_code
    )


async def validate_exception_handler(request: Request, exc: RequestValidationError):
    info = {'details': exc.errors()[0]['msg']}
    return templates.TemplateResponse(
        '422.html',
        {'request': request, 'info': info},
        status_code=422,
    )


async def internal_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        '500.html',
        {'request': request},
        status_code=exc.status_code,
    )
