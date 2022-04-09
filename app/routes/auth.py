# routes
from app.routes.routes_auth import routes_auth

# fastapi concerns
from typing import List, Union
from fastapi import Response, APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

# schemas concerns
import app.api.schemas_pd as schemas_pd

# general
import json

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/login",
    response_model=Union[schemas_pd.AuthResponse, schemas_pd.InfoResponse],
)
def login(response: Response, auth: OAuth2PasswordRequestForm = Depends()):
    request = {"email": auth.username, "password": auth.password}
    return routes_auth.login(
        schemas_pd.AuthRequest(**request),
        response,
    )
