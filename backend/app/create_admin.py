from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import SQLALCHEMY_DATABASE_URL
from app import models, security

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_initial_admin():
    db = SessionLocal()
    try:
        # Check if admin exists
        admin = db.query(models.User).filter(models.User.username == "admin").first()
        if admin:
            print("Admin user already exists.")
            return

        print("Creating default admin user...")
        hashed_pw = security.get_password_hash("admin123")
        admin_user = models.User(
            username="admin",
            password_hash=hashed_pw,
            role=models.UserRole.ADMIN
        )
        db.add(admin_user)
        db.commit()
        print("✅ Admin user created: admin / admin123")
        
    finally:
        db.close()

if __name__ == "__main__":
    create_initial_admin()
