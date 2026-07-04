from sqlmodel import SQLModel, create_engine, Session

db_url = "postgresql://postgres:55422653@localhost:5432/gym_management_system"
engine = create_engine(db_url)


def create_tables():
    from app.models import Users, Members, Trainers

    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
