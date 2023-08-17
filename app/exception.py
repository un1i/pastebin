import fastapi.exceptions as fastapi_exc


class HTTPException(fastapi_exc.HTTPException):
    def __init__(self, status_code: int, details: str):
        detail = {
            'status': 'error',
            'data': None,
            'details': details,
        }
        super().__init__(status_code=status_code, detail=detail)


class LengthError(Exception):
    pass


class LifeTimeError(Exception):
    pass


class NotFoundError(Exception):
    pass


class AuthorError(Exception):
    pass


