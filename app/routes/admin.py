# routes
from app.routes.routes_admin import bootstrap_tables

# fastapi concerns
from typing import Optional, List, Union
from fastapi import Response, APIRouter, Depends

# schemas concerns
import app.api.schemas_pd as schemas_pd
from app.utils.oauth2 import get_current_user

router = APIRouter(tags=["Admin"])


@router.post("/tables", response_model=schemas_pd.InfoResponse)
def create_tables(response: Response):
    return bootstrap_tables.create_tables(response)
