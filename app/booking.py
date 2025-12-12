from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import Booking
from datetime import datetime

router = APIRouter(prefix="/booking", tags=["Booking"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/new")
async def create_booking(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user:
        return {"error": "Not logged in"}

    form = await request.form()

    form_date = form.get("date")
    if form_date:
        date_obj = datetime.strptime(form_date, "%Y-%m-%d").date()
    else:
        date_obj = None

    new_booking = Booking(
        user_email=user["email"],
        user_name=user["name"],
        phone=form.get("phone"),
        service=form.get("service"),
        date=date_obj, #form.get("date"),
        request=form.get("request"),
        status="Confirmed"
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return {"success": True}


@router.get("/all")
def get_user_bookings(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user:
        return []

    return db.query(Booking).filter(
        Booking.user_email == user["email"]
    ).order_by(Booking.id.desc()).all()
