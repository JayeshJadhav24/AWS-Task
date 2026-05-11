from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.services import s3_service, ses_service

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("/", response_model=List[schemas.TodoResponse])
def get_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_todos(db, skip=skip, limit=limit)


@router.get("/{todo_id}", response_model=schemas.TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.post("/", response_model=schemas.TodoResponse, status_code=201)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    db_todo = crud.create_todo(db, todo)
    if todo.email:
        ses_service.send_todo_created_email(
            recipient_email=str(todo.email),
            todo_title=todo.title,
            todo_id=db_todo.id,
        )
    return db_todo


@router.patch("/{todo_id}", response_model=schemas.TodoResponse)
def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    db_todo = crud.update_todo(db, todo_id, todo)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.delete_todo(db, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if db_todo.attachment:
        s3_service.delete_file(db_todo.attachment)
    return {"message": f"Todo {todo_id} deleted successfully"}


@router.post("/{todo_id}/attachment", response_model=schemas.TodoResponse)
async def upload_attachment(
    todo_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    db_todo = crud.get_todo(db, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    file_url = s3_service.upload_file(file)
    db_todo = crud.update_todo_attachment(db, todo_id, file_url)
    return db_todo
