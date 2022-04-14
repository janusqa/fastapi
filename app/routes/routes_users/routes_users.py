# Encryption & Hashing concerns
from app.utils.utils import hash as password_hash

# db concerns
from app.db.db import dbconnect, ResultIter
from app.db.db import DBError

# fastapi concerns
from typing import Optional, List, Union
from fastapi import Response, status, HTTPException

# schemas concerns
import app.api.schemas_pd as schemas_pd


def get_user(user_id: int, response: Response):
    user_found = None
    try:
        with dbconnect() as curr:
            sql = """
            SELECT * 
            FROM users 
            WHERE user_id = %s
            """
            query_parameters = (user_id,)
            curr.execute(sql, query_parameters)
            user_found = next(ResultIter(curr, 1), None)
        if user_found is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Resource with id {user_id} does not exist",
            )
    except HTTPException as error:
        response.status_code = error.status_code
        return {"detail": error.detail}
    except (Exception, DBError) as error:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": str(error)}
    return user_found


def create_user(user: schemas_pd.User, response: Response):
    try:
        user.password = password_hash(user.password)
        with dbconnect() as curr:
            sql = """
                INSERT 
                INTO users (email, password) 
                VALUES (%s, %s) 
                RETURNING *
            """
            query_parameters = (user.email, user.password)
            curr.execute(sql, query_parameters)
            new_user = next(ResultIter(curr, 1), None)
        if new_user:
            response.status_code = status.HTTP_201_CREATED
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unable to add to resource",
            )
    except HTTPException as error:
        response.status_code = error.status_code
        return {"detail": error.detail}
    except (Exception, DBError) as error:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": str(error)}
    return new_user
