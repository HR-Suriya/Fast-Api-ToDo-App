# fastapi-neon/fastapi_neon/main.py

from contextlib import asynccontextmanager
from typing import Union, Optional, Annotated
from fastapi_neon import settings
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import FastAPI, Depends, HTTPException


class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    body: str = Field(index=True)
    author: str = Field(index=True)


# only needed for psycopg 3 - replace postgresql
# with postgresql+psycopg in settings.DATABASE_URL
connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)


# recycle connections after 5 minutes
# to correspond with the compute scale down
engine = create_engine(
    connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# The first part of the function, before the yield, will
# be executed before the application starts.
# https://fastapi.tiangolo.com/advanced/events/#lifespan-function
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan, title="Hello World API with DB", 
    version="0.0.1",
    servers=[
        {
            "url": "http://localhost:8000", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
        ])

def get_session():
    with Session(engine) as session:
        yield session


@app.get("/")
def read_root():
    return {"Hi": "API"}


@app.get("/todos/", response_model=list[Todo])
def read_todos(session: Annotated[Session, Depends(get_session)]):
        todos = session.exec(select(Todo)).all()
        return todos


@app.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: int, session: Annotated[Session, Depends(get_session)]):
    todo = session.exec(select(Todo).where(Todo.id == todo_id)).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.post("/todos/", response_model=Todo)
def create_todo(todo: Todo, session: Annotated[Session, Depends(get_session)]):
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_todo: Todo, session: Annotated[Session, Depends(get_session)]):
    existing_todo = session.get(Todo, todo_id)
    if not existing_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Update fields based on the provided data
    for field, value in updated_todo.dict().items():
        setattr(existing_todo, field, value)
    
    session.commit()
    session.refresh(existing_todo)
    return existing_todo


@app.patch("/todos/{todo_id}", response_model=Todo)
def partial_update_todo(todo_id: int, updated_fields: dict, session: Annotated[Session, Depends(get_session)]):
    existing_todo = session.get(Todo, todo_id)
    if not existing_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Update specific fields based on the provided data
    for field, value in updated_fields.items():
        setattr(existing_todo, field, value)
    
    session.commit()
    session.refresh(existing_todo)
    return existing_todo


@app.delete("/todos/{todo_id}", response_model=dict)
def delete_todo(todo_id: int, session: Annotated[Session, Depends(get_session)]):
    existing_todo = session.get(Todo, todo_id)
    if not existing_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    session.delete(existing_todo)
    session.commit()
    return {"message": "Todo deleted successfully"}

