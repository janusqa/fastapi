# db concerns
from app.db.db import dbconnect, ResultIter
from psycopg import Error

# fastapi concerns
from fastapi import Response, status, HTTPException

# schemas concerns
import app.db.schemas_db as schemas_db


def create_tables(response: Response):
    try:
        with dbconnect() as curr:
            curr.execute(schemas_db.table_users)
            curr.execute(schemas_db.table_posts)
            curr.execute(schemas_db.table_votes)
    except (Exception, Error) as error:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": str(error)}
    response.status_code = status.HTTP_201_CREATED
    return {"detail": "Tables succesfully created."}
