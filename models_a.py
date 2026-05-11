from sqlmodel import SQLModel, Field
from typing import Optional

class Patient(SQLModel, table=True):
    """Glavna tabela pacijenata u bazi podataka"""
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str 
    last_name: str 
    date_of_birth: str  
    phone: str
    gender: Optional[str] = None 
    email: Optional[str] = None
    
    has_insurance: bool = False  
    allergies: Optional[str] = None  
    medical_history: Optional[str] = None 
    last_visit: Optional[str] = None 

class PatientCreate(SQLModel):
    """Model za kreiranje (POST) - korisnik mora poslati osnovna polja"""
    first_name: str
    last_name: str
    date_of_birth: str
    phone: str
    gender: Optional[str] = None
    email: Optional[str] = None
    has_insurance: bool = False
    allergies: Optional[str] = None
    medical_history: Optional[str] = None

class PatientUpdate(SQLModel):
    """Model za PATCH - sva polja su opcionalna kako bi se omogućilo djelimično ažuriranje"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    email: Optional[str] = None
    has_insurance: Optional[bool] = None
    allergies: Optional[str] = None
    medical_history: Optional[str] = None
    last_visit: Optional[str] = None