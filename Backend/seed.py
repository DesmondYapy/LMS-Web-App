from utils.db import engine, SessionLocal
from models.user import Base, User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if not db.query(User).filter(User.email == "admin@test.com").first():
        admin = User(
            email="admin@test.com",
            hashed_password=hash_password("admin123"),
            role="admin"
        )
        instructor = User(
            email="instructor@test.com",
            hashed_password=hash_password("instructor123"),
            role="instructor"
        )
        db.add_all([admin, instructor])
        db.commit()
        print("Seeded admin and instructor accounts.")
    else:
        print("Users already seeded.")

    db.close()

if __name__ == "__main__":
    seed()
