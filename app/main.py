# fastapi concerns
from fastapi import FastAPI

# schemas concerns
import app.api.schemas_pd as schemas_pd
from app.routes import posts, users, admin, auth, votes

# CORS concerns
from app import cors


# to start fastapi server at command enter the below
# uvicorn <packagedir>.<name_of_file_server_is_in>:<name_of_server_variable> --reload
# eg: uvicorn main:app --reload or if in an app dir uvicorn app.main:app --reload
# --reload restarts server when code is changed and saved.
# DO NOT USE IT IN PRODUCTION.
webapp = FastAPI()
cors.cors_init()

webapp.include_router(posts.router)
webapp.include_router(users.router)
webapp.include_router(admin.router)
webapp.include_router(auth.router)
webapp.include_router(votes.router)


@webapp.get("/", response_model=schemas_pd.InfoResponse)
def root():
    return {"detail": "Demo Social API!"}
