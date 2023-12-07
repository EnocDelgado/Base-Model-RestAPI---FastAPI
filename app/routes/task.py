from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..models.models import Task
from ..schemas import task
from ..db.config import get_db
from ..middleware.oauth2 import get_current_user
from typing import  List, Optional

router = APIRouter(
    prefix="/tasks",
    tags=['Tasks']
)

@router.get("/", response_model=List[task.Task])
def get_tasks(db: Session = Depends(get_db), 
              current_user: int = Depends(get_current_user), 
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    

    tasks = db.query(Task).limit(limit).offset(skip).all()

    return tasks


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=task.Task)
def create_task(task: task.TaskCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    new_task = Task(owner_id=current_user.id, **task.dict())
    # add task to our database
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@router.get("/{id}", response_model=task.Task)
def get_task(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    
    task = db.query(Task).group_by(
            Task.id).filter(Task.id == id).first()

    # Validation
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"task with id: {id} was not found")
    
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform request action")
    
    return task


@router.put("/{id}", response_model=task.Task, status_code=status.HTTP_200_OK)
def update_task(id: int, updated_task: task.TaskCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    task_query = db.query(Task).filter(Task.id == id)

    task = task_query.first()

    # Validation
    if task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"task with id: {id} does not exist")
    
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform request action")
    
    task_query.update(updated_task.dict(), synchronize_session=False)

    db.commit()

    return task_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    task_query  = db.query(Task).filter(Task.id == id)

    task = task_query.first()

    # Validation
    if task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"task with id: {id} does not exists")
    
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform request action")
    
    task_query .delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT, detail=f"task with id: {task} has been deleted")
