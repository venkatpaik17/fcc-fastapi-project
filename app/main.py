from fastapi import FastAPI

from . import models
from .database import engine
from .routers import auth, post, user

# connection is established and tables are created
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# order of path operations matters. Be careful while defining paths
@app.get("/")
def root():
    return {"message": "Hello World!"}


app.include_router(post.router)  # inlcude the post router
app.include_router(user.router)  # include the user router
app.include_router(auth.router)  # include the auth router
