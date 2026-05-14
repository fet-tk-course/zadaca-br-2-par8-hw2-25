from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from database import get_session
from models_a import Patient
from models_b import Appointment, AppointmentCreate, AppointmentUpdate
from sqlalchemy import func

router = APIRouter(prefix="/appointments", tags=["Termini pregleda"])


@router.get("/", response_model=List[Appointment])
def read_appointments(
    patient_id: Optional[int] = Query(default=None, description="Filter po ID-u pacijenta"),
    status_filter: Optional[str] = Query(default=None, description="Filter po statusu termina"),
    is_confirmed: Optional[bool] = Query(default=None, description="Filter po potvrdi termina"),
    session: Session = Depends(get_session)
):
    # Dohvata sve termine pregleda uz opcionalno filtriranje
    statement = select(Appointment)

    if patient_id is not None:
        statement = statement.where(Appointment.patient_id == patient_id)

    if status_filter is not None:
        statement = statement.where(Appointment.status == status_filter)

    if is_confirmed is not None:
        statement = statement.where(Appointment.is_confirmed == is_confirmed)

    appointments = session.exec(statement).all()
    return appointments


@router.post("/", response_model=Appointment, status_code=status.HTTP_201_CREATED)
def create_appointment(
    appointment_data: AppointmentCreate,
    session: Session = Depends(get_session)
):
    # Provjerava da li pacijent postoji prije kreiranja termina
    patient = session.get(Patient, appointment_data.patient_id)

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Pacijent nije pronađen"
        )
    # Provjerava da li isti pacijent već ima termin u istom vremenu
    existing_appointment = session.exec(
        select(Appointment).where(
            Appointment.patient_id == appointment_data.patient_id,
            Appointment.appointment_time == appointment_data.appointment_time
        )
    ).first()

    if existing_appointment is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Pacijent već ima termin u odabranom vremenu"
        )

    appointment = Appointment.model_validate(appointment_data)

    session.add(appointment)
    session.commit()
    session.refresh(appointment)

    return appointment

@router.get("/statistics")
def get_appointment_statistics(
    session: Session = Depends(get_session)
):
    # Vraća osnovnu statistiku za termine pregleda
    total_appointments = session.exec(
        select(func.count(Appointment.id))
    ).one()

    average_price = session.exec(
        select(func.avg(Appointment.price))
    ).one()

    confirmed_appointments = session.exec(
        select(func.count(Appointment.id)).where(Appointment.is_confirmed == True)
    ).one()

    return {
        "ukupno_termina": total_appointments,
        "prosjek_cijene": round(average_price or 0, 2),
        "potvrdjeni_termini": confirmed_appointments
    }

@router.get("/{appointment_id}", response_model=Appointment)
def read_appointment(
    appointment_id: int,
    session: Session = Depends(get_session)
):
    # Dohvata jedan termin pregleda po ID-u
    appointment = session.get(Appointment, appointment_id)

    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Termin pregleda nije pronađen"
        )

    return appointment


@router.put("/{appointment_id}", response_model=Appointment)
def replace_appointment(
    appointment_id: int,
    appointment_data: AppointmentCreate,
    session: Session = Depends(get_session)
):
    # Potpuno mijenja podatke postojećeg termina pregleda
    appointment = session.get(Appointment, appointment_id)

    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Termin pregleda nije pronađen"
        )

    patient = session.get(Patient, appointment_data.patient_id)

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Pacijent nije pronađen"
        )

    appointment_dict = appointment_data.model_dump()

    for key, value in appointment_dict.items():
        setattr(appointment, key, value)

    session.add(appointment)
    session.commit()
    session.refresh(appointment)

    return appointment


@router.patch("/{appointment_id}", response_model=Appointment)
def update_appointment(
    appointment_id: int,
    appointment_data: AppointmentUpdate,
    session: Session = Depends(get_session)
):
    # Djelimično ažurira samo polja koja su poslana u zahtjevu
    appointment = session.get(Appointment, appointment_id)

    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Termin pregleda nije pronađen"
        )

    appointment_dict = appointment_data.model_dump(exclude_unset=True)

    if "patient_id" in appointment_dict:
        patient = session.get(Patient, appointment_dict["patient_id"])

        if patient is None:
            raise HTTPException(
                status_code=404,
                detail="Pacijent nije pronađen"
            )

    for key, value in appointment_dict.items():
        setattr(appointment, key, value)

    session.add(appointment)
    session.commit()
    session.refresh(appointment)

    return appointment


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(
    appointment_id: int,
    session: Session = Depends(get_session)
):
    # Briše termin pregleda iz baze
    appointment = session.get(Appointment, appointment_id)

    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Termin pregleda nije pronađen"
        )

    session.delete(appointment)
    session.commit()

    return None