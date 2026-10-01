from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.app.config import settings, ensure_directories

ensure_directories()

DATABASE_URL = f"sqlite:///{settings.SQLITE_DB_PATH}"

# Multi-threaded concurrent SQLite setup with 30s timeout
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
        "timeout": 30.0  # Wait up to 30 seconds for lock instead of throwing OperationalError
    },
    pool_pre_ping=True,
)

# Enable WAL (Write-Ahead Logging) mode for SQLite to support 5-10 concurrent readers/writers
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA synchronous=NORMAL;")
    cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
