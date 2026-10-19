from app.database.base import Base
from app.database.models import User, AgentRun, AuditLog
from app.database.session import engine


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")


if __name__ == "__main__":
    create_tables()