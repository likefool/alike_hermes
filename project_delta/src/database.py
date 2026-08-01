from sqlmodel import create_engine, Session, SQLModel
from pathlib import Path

# Use a local SQLite database for development
# Using absolute path to avoid issues with relative execution
DB_PATH = "sqlite:///projects/project_delta/src/delta_store.db"
engine = create_engine(DB_PATH, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
