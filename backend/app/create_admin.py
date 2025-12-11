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
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        adm_user = os.getenv("ADMIN_USERNAME", "admin")
        adm_pass = os.getenv("ADMIN_PASSWORD", "admin123")
        
        hashed_pw = security.get_password_hash(adm_pass)
        admin_user = models.User(
            username=adm_user,
            password_hash=hashed_pw,
            role=models.UserRole.ADMIN
        )
        db.add(admin_user)
        db.commit()
        print(f"✅ Admin user created: {adm_user} / {'*' * len(adm_pass)}")
        
    finally:
        db.close()

if __name__ == "__main__":
    create_initial_admin()
