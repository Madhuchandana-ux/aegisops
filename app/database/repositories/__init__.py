from sqlalchemy.orm import Session

from app.database.models.user import User


def get_user_by_username(
    db: Session,
    username: str,
) -> User | None:
    """
    Find a user by username.
    """

    return (
        db.query(User)
        .filter(User.username == username)
        .first()
    )


def create_user(
    db: Session,
    *,
    username: str,
    password_hash: str,
    role: str,
    is_active: bool = True,
) -> User:
    """
    Create a new database user.
    """

    user = User(
        username=username,
        password_hash=password_hash,
        role=role,
        is_active=is_active,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user