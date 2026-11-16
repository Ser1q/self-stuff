from fastapi import FastAPI, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from models import LeadEvent

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.api_route("/webhook/yume", methods=["POST", "GET"])
async def yume_webhook(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
    except:
        data = {
            "raw": (await request.body()).decode("utf-8")
        }

    print("YUME WEBHOOK:", data)

    event = LeadEvent(
        lead_id=data.get("lead_id") if isinstance(data, dict) else None,
        event_type=data.get("event") if isinstance(data, dict) else "unknown",
        payload=data
    )

    db.add(event)
    db.commit()

    return {"status": "ok"}

@app.get("/savvy/events")
def get_unprocessed_events(db: Session = Depends(get_db)):
    events = db.query(LeadEvent).filter(
        LeadEvent.processed_by_savvy == False
    ).all()

    return events

@app.post("/webhook/savvy")
async def savvy_callback(data: dict, db: Session = Depends(get_db)):
    event_id = data.get("event_id")

    event = db.query(LeadEvent).filter(
        LeadEvent.id == event_id
    ).first()

    if not event:
        raise HTTPException(404, "Event not found")

    event.processed_by_savvy = True
    db.commit()

    # здесь позже: POST обратно в Yume

    return {"status": "ok"}