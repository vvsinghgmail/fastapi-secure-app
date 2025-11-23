from sqlmodel import Session, select

from app.db.session import engine
from app.models.user import User, UserRole
from app.models.blog import Blog
from app.core.security import get_password_hash


def main():
    with Session(engine) as session:
        # Admin
        admin_email = "admin@uat.local"
        user_email = "user@uat.local"

        existing_admin = session.exec(
            select(User).where(User.email == admin_email)
        ).first()
        if not existing_admin:
            admin = User(
                email=admin_email,
                hashed_password=get_password_hash("AdminPass123!"),
                role=UserRole.admin,
            )
            session.add(admin)
            print("Created admin user")

        existing_user = session.exec(
            select(User).where(User.email == user_email)
        ).first()
        if not existing_user:
            user = User(
                email=user_email,
                hashed_password=get_password_hash("UserPass123!"),
                role=UserRole.user,
            )
            session.add(user)
            print("Created normal user")

        session.commit()

        # Sample blogs
        admin = session.exec(
            select(User).where(User.email == admin_email)
        ).first()
        user = session.exec(
            select(User).where(User.email == user_email)
        ).first()

        if admin:
            blog1 = Blog(
                title="Admin Blog",
                content="Admin-written blog content",
                is_published=True,
                owner_id=admin.id,
            )
            session.add(blog1)

        if user:
            blog2 = Blog(
                title="User Blog",
                content="User-written blog content",
                is_published=False,
                owner_id=user.id,
            )
            session.add(blog2)

        session.commit()
        print("Seeded blogs")


if __name__ == "__main__":
    main()

