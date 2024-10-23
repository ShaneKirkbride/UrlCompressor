from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Define the database URL for SQLite (local file)
DATABASE_URL = "sqlite:///./urlshortener.db"

# Create a SQLAlchemy engine instance
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency function to get a database session
def get_db():
    from contextlib import contextmanager

    @contextmanager
    def db_session():
        db = SessionLocal()
        try:
            yield db  # Provide the session to the caller
        finally:
            db.close()  # Close the session after use
    return db_session()