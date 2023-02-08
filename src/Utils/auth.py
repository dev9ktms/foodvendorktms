from fastapi import HTTPException
from google.auth.transport import requests
from starlette.requests import Request


def isLoggedIn(request:Request):
    if ('user' in request.session) == False:
        raise HTTPException(status_code=400, detail="Request Unauthorized")