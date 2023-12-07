from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..models.models import User
from ..schemas import user
from ..db.config import get_db
from ..middleware.oauth2 import get_current_user
from ..helpers import utils

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=user.UserOut)
def create_user(user: user.UserCreate, db: Session = Depends(get_db)):

    try:
        #hash the paasword - user.password
        hashed_password = utils.hash(user.password)
        user.password = hashed_password

        new_user = User(**user.dict())

        # add post to our database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    
    except:
        if user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"User already exist")


@router.get("/{id}", response_model=user.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with id: {id} does not exist")
    
    return user


@router.put("/{id}", response_model=user.UserUpdate, status_code=status.HTTP_200_OK)
def update_user(id: int, updated_user: user.UserCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    user_query = db.query(User).filter(User.id == id)

    user = user_query.first()

    # Validation
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"user with id: {id} does not exist")
    
    if user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform request action")
    
    user_query.update(updated_user.dict(), synchronize_session=False)

    db.commit()

    return user_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    user_query  = db.query(User).filter(User.id == id)

    user = user_query.first()

    # Validation
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"user with id: {id} does not exists")
    
    if user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform request action")
    
    user_query .delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT, detail=f"User {user} has been deleted")

