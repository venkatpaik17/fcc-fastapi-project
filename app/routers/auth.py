from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, models, oauth2, schemas, utils

# create a router instance
router = APIRouter(tags=["Authentication"])


# user login authentication, generated token format should be Token model
@router.post("/login", response_model=schemas.Token)
# using request form as dependency, fields will be username, password
def user_login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    # check for user in the DB using email
    user = (
        db.query(models.User)
        .filter(models.User.u_email == user_credentials.username)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )

    # if user is present then verify attempt password with DB stored hashed password
    verify_pass = utils.verify_password(user_credentials.password, user.u_password)
    if not verify_pass:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )
    # generate jwt token
    # we are passing a dict containing user_id, we can add more fields too
    access_token = oauth2.create_access_token(payload={"user_id": user.u_id})

    # return the generated JWT token and the type
    # this is bearer type token
    # This JSON format is very important as per oauth2 spec
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
