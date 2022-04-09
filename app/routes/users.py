# routes
from app.routes.routes_users import routes_users

# fastapi concerns
from typing import Optional, List, Union
from fastapi import Response, APIRouter

# schemas concerns
import app.api.schemas_pd as schemas_pd

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/{id}",
    response_model=Union[schemas_pd.UserResponse, schemas_pd.InfoResponse],
)
def get_user(id: int, response: Response):
    return routes_users.get_user(id, response)


@router.post(
    "/",
    response_model=Union[schemas_pd.UserResponse, schemas_pd.InfoResponse],
)
def create_user(user: schemas_pd.UserCreateRequest, response: Response):
    return routes_users.create_user(user, response)
