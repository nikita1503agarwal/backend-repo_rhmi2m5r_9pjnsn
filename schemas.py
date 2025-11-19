"""
Database Schemas for Monter Medical Skin Care

Each Pydantic model becomes a MongoDB collection with the lowercase class name.
- Booking -> "booking"
- Message -> "message"
- Newsletter -> "newsletter"
- Service -> "service" (used mainly for typing/validation)
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import date


class Booking(BaseModel):
    full_name: str = Field(..., min_length=2, description="Vor- und Nachname")
    email: EmailStr = Field(..., description="E-Mail-Adresse")
    phone: Optional[str] = Field(None, description="Telefonnummer")
    service: str = Field(..., description="Dienstleistung")
    category: str = Field(..., description="Kategorie der Dienstleistung")
    preferred_date: Optional[date] = Field(None, description="Wunschtermin")
    notes: Optional[str] = Field(None, description="Notizen oder besondere Hinweise")
    agree_policy: bool = Field(..., description="Einwilligung Datenschutz & Bedingungen")


class Message(BaseModel):
    full_name: str = Field(..., min_length=2, description="Name")
    email: EmailStr = Field(..., description="E-Mail-Adresse")
    subject: str = Field(..., min_length=3, description="Betreff")
    message: str = Field(..., min_length=10, description="Nachricht")


class Newsletter(BaseModel):
    email: EmailStr
    consent: bool = Field(..., description="Einwilligung zum Erhalt des Newsletters")


class FAQ(BaseModel):
    question: str
    answer: str


class Service(BaseModel):
    slug: str
    title: str
    category: str
    summary: str
    details: Optional[str] = None
    benefits: Optional[List[str]] = None
    faqs: Optional[List[FAQ]] = None
    price_hint: Optional[str] = None
