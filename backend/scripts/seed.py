from sqlalchemy import select

import app.models  # noqa: F401
from app.core.security import hash_password
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models import Role, User


def main():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        admin_role = db.execute(select(Role).where(Role.name == "admin")).scalars().first()
        user_role = db.execute(select(Role).where(Role.name == "user")).scalars().first()

        if not admin_role:
            admin_role = Role(name="admin")
            db.add(admin_role)

        if not user_role:
            user_role = Role(name="user")
            db.add(user_role)

        db.commit()

        admin_role = db.execute(select(Role).where(Role.name == "admin")).scalars().first()
        user_role = db.execute(select(Role).where(Role.name == "user")).scalars().first()

        existing_admin = db.execute(
            select(User).where(User.email == "admin@example.com")
        ).scalars().first()

        if not existing_admin:
            db.add(
                User(
                    role_id=admin_role.id,
                    full_name="Admin User",
                    email="admin@example.com",
                    password_hash=hash_password("Admin@123"),
                    is_active=True,
                )
            )

        existing_user = db.execute(
            select(User).where(User.email == "user@example.com")
        ).scalars().first()

        if not existing_user:
            db.add(
                User(
                    role_id=user_role.id,
                    full_name="Normal User",
                    email="user@example.com",
                    password_hash=hash_password("User@123"),
                    is_active=True,
                )
            )

        db.commit()
        print("Seed completed.")
        print("Admin  -> admin@example.com / Admin@123")
        print("User   -> user@example.com / User@123")

    finally:
        db.close()


if __name__ == "__main__":
    main()