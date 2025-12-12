from sqlalchemy import Column, Integer, String, Date, DateTime
from datetime import datetime
from .database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True)
    user_name = Column(String)
    phone = Column(String)
    service = Column(String)
    date = Column(Date)
    request = Column(String)
    status = Column(String, default="Confirmed")
    created_at = Column(DateTime, default=datetime.utcnow)
