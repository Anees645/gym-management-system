from sqlmodel import SQLModel, create_engine, Session

db_url = "postgresql://neondb_owner:npg_hdaNf1tWqoU9@ep-sparkling-flower-at7io76p-pooler.c-9.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
engine = create_engine(db_url)


def create_tables():
    from app.models import Users, Members, Trainers

    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
