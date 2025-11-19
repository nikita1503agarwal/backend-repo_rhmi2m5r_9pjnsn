import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

from database import db, create_document, get_documents
from schemas import Booking, Message, Newsletter

app = FastAPI(title="Monter Medical Skin Care API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"brand": "Monter Medical Skin Care", "status": "ok"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            try:
                response["collections"] = db.list_collection_names()[:10]
                response["database"] = "✅ Connected & Working"
                response["connection_status"] = "Connected"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response


# -------- Booking Endpoints --------
@app.post("/api/bookings", status_code=201)
def create_booking(payload: Booking):
    try:
        booking_id = create_document("booking", payload)
        return {"id": booking_id, "message": "Booking created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/bookings")
def list_bookings(limit: Optional[int] = 50):
    try:
        docs = get_documents("booking", limit=limit)
        # Convert ObjectId to string for safety
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------- Contact Messages --------
@app.post("/api/messages", status_code=201)
def create_message(payload: Message):
    try:
        msg_id = create_document("message", payload)
        return {"id": msg_id, "message": "Message received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------- Newsletter --------
@app.post("/api/newsletter", status_code=201)
def subscribe_newsletter(payload: Newsletter):
    try:
        sub_id = create_document("newsletter", payload)
        return {"id": sub_id, "message": "Subscribed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
