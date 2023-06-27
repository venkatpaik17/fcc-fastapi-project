from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import auth, post, user, vote

# connection is established and tables are created, only needed if using sqlalchemy for create operations. Not required if using alembic (DB Migr tool)
# models.Base.metadata.create_all(bind=engine)


# creating a fastapi instance
app = FastAPI()

# CORS (Cross Origin Resource Sharing)
# define origins for CORS, this is useful if any other domain should gain access to our api endpoints. If CORS is not implemented by default browser implements SOP (Single Origin Policy)
origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# order of path operations matters. Be careful while defining paths
@app.get("/")
def root():
    return {"message": "Hello World!"}


app.include_router(post.router)  # inlcude the post router
app.include_router(user.router)  # include the user router
app.include_router(auth.router)  # include the auth router
app.include_router(vote.router)  # include the vote router
