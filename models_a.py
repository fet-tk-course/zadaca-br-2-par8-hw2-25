from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date
from pydantic import field_validator

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

    @field_validator('first_name')
    @classmethod
    def first_name_ne_smije_biti_prazan(cls, v):
        if not v.strip():
            raise ValueError('Ime ne smije biti prazan string')
        return v.strip()

    @field_validator('weight_kg')
    @classmethod
    def tezina_mora_biti_pozitivna(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Težina mora biti veća od nule')
        return v

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