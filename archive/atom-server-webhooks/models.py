from sqlalchemy import Column, Integer, String, JSON, Boolean
from db import Base

class LeadEvent(Base):
    __tablename__ = "lead_events"

    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer, index=True)
    event_type = Column(String)
    payload = Column(JSON)
    processed_by_savvy = Column(Boolean, default=False)