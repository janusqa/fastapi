# routes
from app.routes.routes_posts import routes_posts

# Authentication concerns
from app.utils.oauth2 import get_current_user

# fastapi concerns
from typing import Optional, List, Union
from fastapi import Response, APIRouter, Depends

# schemas concerns
import app.api.schemas_pd as schemas_pd

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get(
    "/latest",
    response_model=Union[schemas_pd.PostResponse, schemas_pd.InfoResponse],
)
def get_latest_post(
    response: Response,
    user: schemas_pd.UserBase = Depends(get_current_user),
):
    return routes_posts.get_latest_post(user, response)


@router.get(
    "/{id}",
    response_model=Union[schemas_pd.PostResponse, schemas_pd.InfoResponse],
)
def get_post(
    id: int,
    response: Response,
    user: schemas_pd.UserBase = Depends(get_current_user),
):
    return routes_posts.get_post(id, user, response)


@router.put(
    "/{id}",
    response_model=Union[schemas_pd.PostResponse, schemas_pd.InfoResponse],
)
def update_post(
    id: int,
    post: schemas_pd.Post,
    response: Response,
    user: schemas_pd.UserBase = Depends(get_current_user),
):
    return routes_posts.update_post(id, post, user, response)


@router.delete(
    "/{id}",
    response_model=Union[schemas_pd.PostResponse, schemas_pd.InfoResponse],
)
def delete_post(
    id: int,
    response: Response,
    user: schemas_pd.UserBase = Depends(get_current_user),
):
    return routes_posts.delete_post(id, user, response)


@router.post(
    "/",
    response_model=Union[schemas_pd.PostResponse, schemas_pd.InfoResponse],
)
def create_post(
    post: schemas_pd.Post,
    response: Response,
    user: schemas_pd.UserBase = Depends(get_current_user),
):
    return routes_posts.create_post(post, user, response)


@router.get(
    "/",
    response_model=Union[List[schemas_pd.PostResponse], schemas_pd.InfoResponse],
)
def get_posts(
    response: Response,
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
    user: schemas_pd.UserBase = Depends(get_current_user),
):
    return routes_posts.get_posts(
        response=response, limit=limit, skip=skip, search=search, user=user
    )
