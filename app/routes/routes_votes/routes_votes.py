# db concerns
from app.db.db import dbconnect, ResultIter
from app.db.db import DBError, DBErrors

# fastapi concerns
from fastapi import Response, status, HTTPException

# schemas concerns
import app.api.schemas_pd as schemas_pd


def create_vote(
    response: Response, vote: schemas_pd.VoteRequest, user: schemas_pd.User
):
    try:
        with dbconnect() as curr:
            query_paramters = (user.user_id, vote.post_id)
            if vote.direction == 1:
                sql = """
                INSERT 
                INTO votes (user_id, post_id) 
                VALUES (%s, %s) 
                RETURNING *
                """
            else:
                sql = """
                DELETE 
                FROM votes 
                WHERE user_id = %s AND post_id = %s 
                RETURNING *
                """
            curr.execute(sql, query_paramters)
            vote_outcome = next(ResultIter(curr, 1), None)
        if vote_outcome and vote.direction == 1:
            response.status_code = status.HTTP_201_CREATED
        elif vote_outcome and vote.direction == 0:
            response.status_code = status.HTTP_204_NO_CONTENT
        else:
            if vote.direction == 0:
                response_message = "Vote does not exist"
                response_code = status.HTTP_404_NOT_FOUND
                raise HTTPException(status_code=response_code, detail=response_message)
    except DBErrors.UniqueViolation as error:
        response_message = "Unable to cast vote. Already voted?"
        response_code = status.HTTP_409_CONFLICT
        raise HTTPException(status_code=response_code, detail=response_message)
    except DBErrors.ForeignKeyViolation as error:
        response_message = "Vote does not exist"
        response_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=response_code, detail=response_message)
    except HTTPException as error:
        response.status_code = error.status_code
        return {"detail": error.detail}
    except (Exception, DBError) as error:
        print(type(error))
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": str(error)}
    return vote_outcome
