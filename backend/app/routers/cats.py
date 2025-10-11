from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from ..database import get_session
from ..models import Cat, CatGeneticTest, CatHealthEvent, CatMeasurement
from ..schemas import (
    CatCreate,
    CatRead,
    CatUpdate,
    GeneticTestCreate,
    GeneticTestRead,
    HealthEventCreate,
    HealthEventRead,
    MeasurementCreate,
    MeasurementRead,
)

router = APIRouter(prefix="/cats", tags=["cats"])


@router.post("", response_model=CatRead)
def create_cat(cat_in: CatCreate, session=Depends(get_session)):
    cat = Cat(**cat_in.dict())
    session.add(cat)
    session.commit()
    session.refresh(cat)
    return cat


@router.get("", response_model=list[CatRead])
def list_cats(session=Depends(get_session)):
    cats = session.exec(select(Cat).order_by(Cat.call_name)).all()
    return cats


@router.get("/{cat_id}", response_model=CatRead)
def get_cat(cat_id: int, session=Depends(get_session)):
    cat = session.get(Cat, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Chat introuvable")
    return cat


@router.patch("/{cat_id}", response_model=CatRead)
def update_cat(cat_id: int, cat_update: CatUpdate, session=Depends(get_session)):
    cat = session.get(Cat, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Chat introuvable")
    for field, value in cat_update.dict(exclude_unset=True).items():
        setattr(cat, field, value)
    session.add(cat)
    session.commit()
    session.refresh(cat)
    return cat


@router.delete("/{cat_id}", status_code=204)
def delete_cat(cat_id: int, session=Depends(get_session)):
    cat = session.get(Cat, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Chat introuvable")
    session.delete(cat)
    session.commit()


@router.post("/{cat_id}/measurements", response_model=MeasurementRead)
def add_measurement(cat_id: int, measurement_in: MeasurementCreate, session=Depends(get_session)):
    if not session.get(Cat, cat_id):
        raise HTTPException(status_code=404, detail="Chat introuvable")
    measurement = CatMeasurement(cat_id=cat_id, **measurement_in.dict(exclude_unset=True))
    session.add(measurement)
    session.commit()
    session.refresh(measurement)
    return measurement


@router.get("/{cat_id}/measurements", response_model=list[MeasurementRead])
def list_measurements(cat_id: int, session=Depends(get_session)):
    if not session.get(Cat, cat_id):
        raise HTTPException(status_code=404, detail="Chat introuvable")
    query = select(CatMeasurement).where(CatMeasurement.cat_id == cat_id).order_by(CatMeasurement.recorded_at)
    return session.exec(query).all()


@router.post("/{cat_id}/genetic-tests", response_model=GeneticTestRead)
def add_genetic_test(cat_id: int, test_in: GeneticTestCreate, session=Depends(get_session)):
    if not session.get(Cat, cat_id):
        raise HTTPException(status_code=404, detail="Chat introuvable")
    test = CatGeneticTest(cat_id=cat_id, **test_in.dict(exclude_unset=True))
    session.add(test)
    session.commit()
    session.refresh(test)
    return test


@router.get("/{cat_id}/genetic-tests", response_model=list[GeneticTestRead])
def list_genetic_tests(cat_id: int, session=Depends(get_session)):
    if not session.get(Cat, cat_id):
        raise HTTPException(status_code=404, detail="Chat introuvable")
    query = select(CatGeneticTest).where(CatGeneticTest.cat_id == cat_id).order_by(CatGeneticTest.result_date.desc())
    return session.exec(query).all()


@router.post("/{cat_id}/health-events", response_model=HealthEventRead)
def add_health_event(cat_id: int, event_in: HealthEventCreate, session=Depends(get_session)):
    if not session.get(Cat, cat_id):
        raise HTTPException(status_code=404, detail="Chat introuvable")
    event = CatHealthEvent(cat_id=cat_id, **event_in.dict(exclude_unset=True))
    session.add(event)
    session.commit()
    session.refresh(event)
    return event


@router.get("/{cat_id}/health-events", response_model=list[HealthEventRead])
def list_health_events(cat_id: int, session=Depends(get_session)):
    if not session.get(Cat, cat_id):
        raise HTTPException(status_code=404, detail="Chat introuvable")
    query = select(CatHealthEvent).where(CatHealthEvent.cat_id == cat_id).order_by(CatHealthEvent.event_date.desc())
    return session.exec(query).all()
