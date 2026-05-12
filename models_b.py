from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel, Field


class Appointment(SQLModel, table=True):
    """Glavna tabela termina pregleda u bazi podataka"""

    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    appointment_time: datetime
    procedure_name: str
    duration_minutes: int
    price: float = 0.0
    status: str = "scheduled"
    is_confirmed: bool = False
    notes: Optional[str] = None


class AppointmentCreate(SQLModel):
    """Model za kreiranje (POST) - korisnik mora poslati osnovna polja"""

    patient_id: int
    appointment_time: datetime
    procedure_name: str
    duration_minutes: int
    price: float = 0.0
    status: str = "scheduled"
    is_confirmed: bool = False
    notes: Optional[str] = None


class AppointmentUpdate(SQLModel):
    """Model za PATCH - sva polja su opcionalna kako bi se omogućilo djelimično ažuriranje"""

    patient_id: Optional[int] = None
    appointment_time: Optional[datetime] = None
    procedure_name: Optional[str] = None
    duration_minutes: Optional[int] = None
    price: Optional[float] = None
    status: Optional[str] = None
    is_confirmed: Optional[bool] = None
    notes: Optional[str] = None