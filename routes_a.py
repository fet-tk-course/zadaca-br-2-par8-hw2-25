from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select
from database import get_session
from models_a import Patient, PatientCreate, PatientUpdate

router = APIRouter(prefix="/patients", tags=["Pacijenti"])

# 1. GET - Lista pacijenata sa filtriranjem
@router.get("/", response_model=List[Patient])
def read_patients(
    last_name: Optional[str] = Query(default=None, description="Pretraga po prezimenu"),
    has_insurance: Optional[bool] = Query(default=None),
    session: Session = Depends(get_session)
):
    statement = select(Patient)
    if last_name:
        statement = statement.where(Patient.last_name.ilike(f"%{last_name}%"))
    if has_insurance is not None:
        statement = statement.where(Patient.has_insurance == has_insurance)
    return session.exec(statement).all()

# 2. POST - Kreiranje novog pacijenta
@router.post("/", response_model=Patient, status_code=status.HTTP_201_CREATED)
def create_patient(data: PatientCreate, session: Session = Depends(get_session)):
    new_patient = Patient.model_validate(data)
    session.add(new_patient)
    session.commit()
    session.refresh(new_patient)
    return new_patient

# 3. GET by ID
@router.get("/{patient_id}", response_model=Patient)
def read_patient(patient_id: int, session: Session = Depends(get_session)):
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Pacijent nije pronađen")
    return patient