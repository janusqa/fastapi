# CORS concerns
from fastapi.middleware.cors import CORSMiddleware

# App concerns
from app import main

# Specify only specific origins that have access to this site
# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
#     "https://www.google.com",
# ]

# Specify that ALL origins have access to this site
origins = ["*"]


def cors_init() -> None:
    main.webapp.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
