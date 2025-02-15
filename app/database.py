from sqlmodel import SQLModel, create_engine, Session

sqlite_url = "sqlite:///database.db"

engine = create_engine(sqlite_url)


def create_database():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
