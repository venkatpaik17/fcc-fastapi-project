from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import database, models, oauth2, schemas

router = APIRouter(prefix="/vote", tags=["Votes"])


# path operation to add/remove a vote
@router.post("/", status_code=status.HTTP_201_CREATED)
def vote_post(
    vote: schemas.VoteCreate,
    db: Session = Depends(database.get_db),
    current_user: schemas.TokenData = Depends(oauth2.get_current_user),
):
    post = (
        db.query(models.Post).filter(models.Post.p_id == vote.post_id).first()
    )  # get that post which is to be voted

    # check if that post exists
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {vote.post_id} does not exist",
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.u_id
    )
    # query the votes table to find the user if he/she has voted or not
    found_vote = vote_query.first()

    # add vote
    if vote.dir:
        # check if user has already voted if yes then raise exception
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with id: {current_user.u_id} has already voted the post with id: {vote.post_id}",
            )

        # else add the vote by creating a entry in votes table
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.u_id)
        db.add(new_vote)
        db.commit()

        return {"message": "Added Vote Successfully"}

    # remove vote
    else:
        # if user has not voted yet then cannot remove the vote
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vote of user with id: {current_user.u_id} for post with id: {vote.post_id} not found",
            )

        # if vote exists the delete that vote by deleting the entry in votes table
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Deleted Vote Successfully"}
