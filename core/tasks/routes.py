from fastapi import APIRouter, Path, Query, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from tasks.schemas import TaskCreateSchema, TaskUpdateSchema, TaskResponseSchema
from tasks.models import TaskModel
from core.database import get_db
from typing import List

# router = APIRouter(tags=["tasks"], prefix="/todo")
router = APIRouter(tags=["tasks"])


@router.get("/tasks", response_model=List[TaskResponseSchema])
async def retrieve_tasks_list(
    completed: bool = Query(None, description="Filter tasks based on their completion status"),
    limit: int = Query(10, gt=0, le=50, description="Limit the number of items returned"),
    offset: int = Query(0, ge=0, description="Number of items to skip before returning results"),
    db: Session = Depends(get_db),
):
    query = db.query(TaskModel)
    if completed is not None:
        query = query.filter_by(is_completed=completed)
    return query.limit(limit).offset(offset).all()


@router.get("/tasks/{task_id}", response_model=TaskResponseSchema)
async def retrieve_tasks_detail(task_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    task_obj = db.query(TaskModel).filter_by(id=task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not Found")
    return task_obj


@router.post("/tasks", response_model=TaskResponseSchema)
async def create_task(request: TaskCreateSchema, db: Session = Depends(get_db)):
    # task_obj = TaskModel(title=request.title, description=request.description, is_completed=request.is_completed)
    # print(request.model_dump())
    task_obj = TaskModel(**request.model_dump())
    db.add(task_obj)
    db.commit()
    db.refresh(task_obj)
    return task_obj


@router.put("/tasks/{task_id}", response_model=TaskResponseSchema)
async def update_task(request: TaskUpdateSchema, task_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    task_obj = db.query(TaskModel).filter_by(id=task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        # task_obj.title = request.title
        # task_obj.description = request.description
        # task_obj.is_completed = request.is_completed
        for field, value in request.model_dump(exclude_unset=True).items():
            setattr(task_obj, field, value)
        db.commit()
        db.refresh(task_obj)
        return task_obj


@router.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    task_obj = db.query(TaskModel).filter_by(id=task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        db.delete(task_obj)
        db.commit()
        # return JSONResponse({"detail": "The task is deleted"}, status_code=200) # The response body is omitted because the endpoint returns 204 No Content. 
