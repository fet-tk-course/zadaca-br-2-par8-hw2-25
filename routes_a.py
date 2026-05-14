from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select, func
from database import get_session
from models_a import Patient, PatientCreate, PatientUpdate

router = APIRouter(prefix="/patients", tags=["Pacijenti"])


# GET - Lista pacijenata sa filtriranjem po vise parametara
@router.get("/", response_model=List[Patient])
def read_patients(
    last_name: Optional[str] = Query(default=None, description="Pretraga po prezimenu"),
    first_name: Optional[str] = Query(default=None, description="Pretraga po imenu"),
    gender: Optional[str] = Query(default=None, description="Filter po spolu (M/F)"),
    has_insurance: Optional[bool] = Query(default=None, description="Filter po osiguranju"),
    session: Session = Depends(get_session)
):
    statement = select(Patient)

    if last_name:
        statement = statement.where(Patient.last_name.ilike(f"%{last_name}%"))
    if first_name:
        statement = statement.where(Patient.first_name.ilike(f"%{first_name}%"))
    if gender:
        statement = statement.where(Patient.gender == gender)
    if has_insurance is not None:
        statement = statement.where(Patient.has_insurance == has_insurance)

    return session.exec(statement).all()


# POST - Kreiranje novog pacijenta
@router.post("/", response_model=Patient, status_code=status.HTTP_201_CREATED)
def create_patient(data: PatientCreate, session: Session = Depends(get_session)):
    # Provjera duplikata po emailu
    if data.email:
        existing = session.exec(
            select(Patient).where(Patient.email == data.email)
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Pacijent sa emailom '{data.email}' već postoji"
            )

    new_patient = Patient.model_validate(data)
    session.add(new_patient)
    session.commit()
    session.refresh(new_patient)
    return new_patient

@router.get("/count")
def count_patients(session: Session = Depends(get_session)):
    statement = select(func.count(Patient.id))
    ukupno = session.exec(statement).one()
    return {"ukupno": ukupno}


# GET po ID-u
@router.get("/{patient_id}", response_model=Patient)
def read_patient(patient_id: int, session: Session = Depends(get_session)):
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Pacijent nije pronađen")
    return patient


# PUT - potpuna zamjena pacijenta
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


# PATCH - djelimično ažuriranje pacijenta
@router.patch("/{patient_id}", response_model=Patient)
def partial_update_patient(patient_id: int, data: PatientUpdate, session: Session = Depends(get_session)):
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Pacijent nije pronađen")

    # exclude_unset=True osigurava da se azuriraju samo polja koja je korisnik poslao
    patient_data = data.model_dump(exclude_unset=True)
    for key, value in patient_data.items():
        setattr(patient, key, value)

    session.add(patient)
    session.commit()
    session.refresh(patient)
    return patient


# DELETE - brisanje pacijenta
@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: int, session: Session = Depends(get_session)):
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Pacijent nije pronađen")
    session.delete(patient)
    session.commit()