from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import database, models, oauth2, schemas, utils

# create a router instance
router = APIRouter(tags=["Authentication"])


# user login authentication
@router.post("/login")
def user_login(
    user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)
):
    # check for user in the DB using email
    user = (
        db.query(models.User)
        .filter(models.User.u_email == user_credentials.u_email)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )

    # if user is present then verify attempt password with DB stored hashed password
    verify_pass = utils.verify_password(user_credentials.u_password, user.u_password)
    if not verify_pass:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )
    # generate jwt token
    # we are passing a dict containing user_id, we can add more fields too
    access_token = oauth2.create_access_token(payload={"user_id": user.u_id})

    # return the generated JWT token and the type
    # this is bearer type token
    return {"access_token": access_token, "token_type": "bearer"}
