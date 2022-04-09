from lib2to3.pgen2 import token
from jose import JWTError, jwt
from datetime import datetime, timedelta

# schemas concerns
import app.api.schemas_pd as schemas_pd

# fastapi concerns
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

# db concerns
from app.db.db import dbconnect, ResultIter
from psycopg import errors

# config concerns
import app.config as appconfig

settings: appconfig.Settings = appconfig.get_settings()

# Secret Key
# Algorithm
# Expiration time

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = settings.oauth2_secret_key
ALGORITHM = settings.oauth2_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.oauth2_expire_min

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(data: dict):
    token_data = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data.update({"exp": expire})
    jwt_token = jwt.encode(claims=token_data, key=SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token


def verify_access_token(jwt_token: str, auth_exception):
    try:
        jwt_token_decoded = jwt.decode(
            token=jwt_token, key=SECRET_KEY, algorithms=[ALGORITHM]
        )
        user_id: int = jwt_token_decoded.get("user_id")
        exp: int = jwt_token_decoded.get("exp")
        if user_id is None or exp is None:
            raise auth_exception
    except JWTError as error:
        raise auth_exception
    else:
        token_data = schemas_pd.TokenData(**{"user_id": user_id, "exp": exp})
    return token_data


def get_current_user(jwt_token: str = Depends(oauth2_scheme)):
    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(jwt_token=jwt_token, auth_exception=auth_exception)

    with dbconnect() as curr:
        try:
            sql = """
                SELECT 
                    user_id, 
                    email, 
                    user_created_at 
                FROM users 
                WHERE user_id = %s            
            """
            query_parameters = (token_data.user_id,)
            curr.execute(sql, query_parameters)
            found_user = next(ResultIter(curr, 1), None)
        except Exception as error:
            found_user = None
            print(error)
            curr.connection.rollback()

    return schemas_pd.UserResponse(**found_user)
