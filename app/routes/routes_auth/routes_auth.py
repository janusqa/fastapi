# Encryption & Hashing concerns
from app.utils.utils import hash as password_hash, verify as password_verify
from app.utils.oauth2 import create_access_token

# db concerns
from app.db.db import dbconnect, ResultIter

# fastapi concerns
from typing import Optional, List, Union
from fastapi import Response, status, HTTPException

# db concerns
from psycopg import Error

# schemas concerns
import app.api.schemas_pd as schemas_pd


def login(auth: schemas_pd.AuthRequest, response: Response):
    user_found = None
    access_token = None
    try:
        with dbconnect() as curr:
            sql = """
                SELECT 
                    user_id, 
                    email, 
                    password 
                FROM users 
                WHERE email = %s
            """
            query_parameters = (auth.email,)
            curr.execute(sql, query_parameters)
            user_found = next(ResultIter(curr, 1), None)
        if user_found is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Invalid credentials for {auth.email}",
            )
        else:
            if password_verify(auth.password, user_found["password"]):
                access_token = create_access_token(
                    data={"user_id": user_found["user_id"]}
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Invalid credentials for {auth.email}",
                )
    except HTTPException as error:
        response.status_code = error.status_code
        return {"detail": error.detail}
    except (Exception, Error) as error:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": str(error)}
    return {"access_token": access_token, "token_type": "bearer"}
