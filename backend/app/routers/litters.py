from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from ..database import get_session
from ..models import Kitten, KittenWeight, Litter
from ..schemas import (
    KittenCreate,
    KittenRead,
    KittenUpdate,
    KittenWeightCreate,
    KittenWeightRead,
    LitterCreate,
    LitterRead,
    LitterUpdate,
)

router = APIRouter(prefix="/litters", tags=["portées"])


@router.post("", response_model=LitterRead)
def create_litter(litter_in: LitterCreate, session=Depends(get_session)):
    litter = Litter(**litter_in.dict())
    session.add(litter)
    session.commit()
    session.refresh(litter)
    return litter


@router.get("", response_model=list[LitterRead])
def list_litters(session=Depends(get_session)):
    query = select(Litter).order_by(Litter.birth_date.is_(None), Litter.birth_date.desc())
    return session.exec(query).all()


@router.get("/{litter_id}", response_model=LitterRead)
def get_litter(litter_id: int, session=Depends(get_session)):
    litter = session.get(Litter, litter_id)
    if not litter:
        raise HTTPException(status_code=404, detail="Portée introuvable")
    return litter


@router.patch("/{litter_id}", response_model=LitterRead)
def update_litter(litter_id: int, litter_update: LitterUpdate, session=Depends(get_session)):
    litter = session.get(Litter, litter_id)
    if not litter:
        raise HTTPException(status_code=404, detail="Portée introuvable")
    for field, value in litter_update.dict(exclude_unset=True).items():
        setattr(litter, field, value)
    session.add(litter)
    session.commit()
    session.refresh(litter)
    return litter


@router.post("/{litter_id}/kittens", response_model=KittenRead)
def add_kitten(litter_id: int, kitten_in: KittenCreate, session=Depends(get_session)):
    if litter_id != kitten_in.litter_id:
        raise HTTPException(status_code=400, detail="Identifiant portée incohérent")
    if not session.get(Litter, litter_id):
        raise HTTPException(status_code=404, detail="Portée introuvable")
    kitten = Kitten(**kitten_in.dict())
    session.add(kitten)
    session.commit()
    session.refresh(kitten)
    return kitten


@router.get("/{litter_id}/kittens", response_model=list[KittenRead])
def list_kittens(litter_id: int, session=Depends(get_session)):
    if not session.get(Litter, litter_id):
        raise HTTPException(status_code=404, detail="Portée introuvable")
    query = select(Kitten).where(Kitten.litter_id == litter_id).order_by(Kitten.name)
    return session.exec(query).all()

@router.patch("/kittens/{kitten_id}", response_model=KittenRead)
def update_kitten(kitten_id: int, kitten_update: KittenUpdate, session=Depends(get_session)):
    kitten = session.get(Kitten, kitten_id)
    if not kitten:
        raise HTTPException(status_code=404, detail="Chaton introuvable")
    for field, value in kitten_update.dict(exclude_unset=True).items():
        setattr(kitten, field, value)
    session.add(kitten)
    session.commit()
    session.refresh(kitten)
    return kitten


@router.post("/kittens/{kitten_id}/weights", response_model=KittenWeightRead)
def add_kitten_weight(kitten_id: int, weight_in: KittenWeightCreate, session=Depends(get_session)):
    if not session.get(Kitten, kitten_id):
        raise HTTPException(status_code=404, detail="Chaton introuvable")
    record = KittenWeight(kitten_id=kitten_id, **weight_in.dict(exclude_unset=True))
    session.add(record)
    session.commit()
    session.refresh(record)
    return record


@router.get("/kittens/{kitten_id}/weights", response_model=list[KittenWeightRead])
def list_kitten_weights(kitten_id: int, session=Depends(get_session)):
    if not session.get(Kitten, kitten_id):
        raise HTTPException(status_code=404, detail="Chaton introuvable")
    query = select(KittenWeight).where(KittenWeight.kitten_id == kitten_id).order_by(KittenWeight.recorded_at)
    return session.exec(query).all()
