from app.database.repositories.user import (
    create_user,
    get_user_by_username,
)
from app.database.session import SessionLocal
from app.security.auth import password_hash
from app.security.rbac import Role


DEVELOPMENT_USERS = [
    {
        "username": "viewer",
        "password": "Viewer@123",
        "role": Role.VIEWER.value,
    },
    {
        "username": "analyst",
        "password": "Analyst@123",
        "role": Role.ANALYST.value,
    },
    {
        "username": "operator",
        "password": "Operator@123",
        "role": Role.OPERATOR.value,
    },
    {
        "username": "admin",
        "password": "Admin@123",
        "role": Role.ADMIN.value,
    },
]


def seed_users() -> None:
    db = SessionLocal()

    try:
        for user_data in DEVELOPMENT_USERS:

            existing_user = get_user_by_username(
                db,
                user_data["username"],
            )

            if existing_user is not None:
                print(
                    f"User '{user_data['username']}' "
                    f"already exists. Skipping."
                )
                continue

            hashed_password = password_hash.hash(
                user_data["password"]
            )

            create_user(
                db,
                username=user_data["username"],
                password_hash=hashed_password,
                role=user_data["role"],
                is_active=True,
            )

            print(
                f"Created user: "
                f"{user_data['username']} "
                f"({user_data['role']})"
            )

    finally:
        db.close()


if __name__ == "__main__":
    seed_users()