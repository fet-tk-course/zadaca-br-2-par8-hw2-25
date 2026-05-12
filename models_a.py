from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Patient(SQLModel, table=True):
    """Glavna tabela pacijenata u bazi podataka"""
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    date_of_birth: date
    phone: str
    gender: Optional[str] = None
    email: Optional[str] = None
    has_insurance: bool = False
    weight_kg: Optional[float] = None
    allergies: Optional[str] = None
    medical_history: Optional[str] = None

class PatientCreate(SQLModel):
    """Model za kreiranje (POST) - korisnik mora poslati osnovna polja"""
    first_name: str
    last_name: str
    date_of_birth: date
    phone: str
    gender: Optional[str] = None
    email: Optional[str] = None
    has_insurance: bool = False
    weight_kg: Optional[float] = None
    allergies: Optional[str] = None
    medical_history: Optional[str] = None

class PatientUpdate(SQLModel):
    """Model za PATCH - sva polja su opcionalna kako bi se omogućilo djelimično ažuriranje"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    email: Optional[str] = None
    has_insurance: Optional[bool] = None
    weight_kg: Optional[float] = None
    allergies: Optional[str] = None
    medical_history: Optional[str] = None