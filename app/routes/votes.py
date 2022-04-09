# routes
from app.routes.routes_votes import routes_votes

# Authentication concerns
from app.utils.oauth2 import get_current_user

# fastapi concerns
from typing import Optional, List, Union
from fastapi import Response, APIRouter, Depends

# schemas concerns
import app.api.schemas_pd as schemas_pd

router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post(
    "/",
    response_model=Union[schemas_pd.VoteResponse, schemas_pd.InfoResponse],
)
def create_vote(
    response: Response,
    vote: schemas_pd.VoteRequest,
    user: schemas_pd.UserBase = Depends(get_current_user),
):
    return routes_votes.create_vote(response=response, vote=vote, user=user)
