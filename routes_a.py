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

# 3. GET po ID-u
@router.get("/{patient_id}", response_model=Patient)
def read_patient(patient_id: int, session: Session = Depends(get_session)):
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Pacijent nije pronađen")
    return patient

# 4. PUT - potpuna zamjena
@router.put("/{patient_id}", response_model=Patient)
def update_patient(patient_id: int, data: PatientCreate, session: Session = Depends(get_session)):
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Pacijent nije pronađen")
    patient_data = data.model_dump()
    for key, value in patient_data.items():
        setattr(patient, key, value)
    session.add(patient)
    session.commit()
    session.refresh(patient)
    return patient

# 5. PATCH - djelimično ažuriranje
@router.patch("/{patient_id}", response_model=Patient)
def partial_update_patient(patient_id: int, data: PatientUpdate, session: Session = Depends(get_session)):
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Pacijent nije pronađen")
    patient_data = data.model_dump(exclude_unset=True)
    for key, value in patient_data.items():
        setattr(patient, key, value)
    session.add(patient)
    session.commit()
    session.refresh(patient)
    return patient

# 6. DELETE - brisanje pacijenta
@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: int, session: Session = Depends(get_session)):
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Pacijent nije pronađen")
    session.delete(patient)
    session.commit()