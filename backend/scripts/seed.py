from app.core.database import Base, SessionLocal, engine
from app.core.security import hash_password
from app.models import Exam, Organization, Role, User, UserRole


def run() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        org = db.query(Organization).filter(Organization.code == "default").first()
        if org is None:
            org = Organization(name="Default Institute", code="default")
            db.add(org)
            db.commit()
            db.refresh(org)

        for role_name in ("super_admin", "staff", "viewer"):
            if db.query(Role).filter(Role.name == role_name).first() is None:
                db.add(Role(name=role_name, description=f"{role_name} role"))
        db.commit()

        admin = db.query(User).filter(User.email == "admin@example.com").first()
        if admin is None:
            admin = User(
                organization_id=org.id,
                full_name="System Admin",
                email="admin@example.com",
                hashed_password=hash_password("admin123"),
                role=UserRole.SUPER_ADMIN,
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)

        exam = db.query(Exam).filter(Exam.title == "Sample OMR Exam").first()
        if exam is None:
            exam = Exam(
                organization_id=org.id,
                owner_id=admin.id,
                title="Sample OMR Exam",
                subject="Mathematics",
                description="Seeded sample exam",
                total_questions=50,
                options_per_question=4,
                positive_marks=1,
                negative_marks=0,
                negative_marking_enabled=False,
                answer_key={str(i): "A" for i in range(1, 51)},
            )
            db.add(exam)
            db.commit()
        print("Seed complete")
    finally:
        db.close()


if __name__ == "__main__":
    run()

