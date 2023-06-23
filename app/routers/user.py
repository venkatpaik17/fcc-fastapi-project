from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db

# create a router instance
router = APIRouter(prefix="/users", tags=["Users"])


# create a new user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.get_hash(user.u_password)  # generated a hashed password
    user.u_password = hashed_password  # update the user model
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# get the specific user through id
@router.get("/{id}", response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    specific_user = db.query(models.User).filter(models.User.u_id == id).first()
    if not specific_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist",
        )

    return specific_user
