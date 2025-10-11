from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from ..database import get_session
from ..models import AdoptionFollowUp, FamilyLead, LeadInteraction, Reservation
from ..schemas import (
    AdoptionFollowUpCreate,
    AdoptionFollowUpRead,
    FamilyLeadCreate,
    FamilyLeadRead,
    FamilyLeadUpdate,
    LeadInteractionCreate,
    LeadInteractionRead,
    ReservationCreate,
    ReservationRead,
)

router = APIRouter(prefix="/leads", tags=["familles"])


@router.post("", response_model=FamilyLeadRead)
def create_lead(lead_in: FamilyLeadCreate, session=Depends(get_session)):
    lead = FamilyLead(**lead_in.dict())
    session.add(lead)
    session.commit()
    session.refresh(lead)
    return lead


@router.get("", response_model=list[FamilyLeadRead])
def list_leads(session=Depends(get_session), status: str | None = None):
    query = select(FamilyLead)
    if status:
        query = query.where(FamilyLead.status == status)
    query = query.order_by(FamilyLead.qualification_score.is_(None), FamilyLead.qualification_score.desc(), FamilyLead.last_name)
    return session.exec(query).all()


@router.get("/{lead_id}", response_model=FamilyLeadRead)
def get_lead(lead_id: int, session=Depends(get_session)):
    lead = session.get(FamilyLead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Famille introuvable")
    return lead


@router.patch("/{lead_id}", response_model=FamilyLeadRead)
def update_lead(lead_id: int, lead_update: FamilyLeadUpdate, session=Depends(get_session)):
    lead = session.get(FamilyLead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Famille introuvable")
    for field, value in lead_update.dict(exclude_unset=True).items():
        setattr(lead, field, value)
    session.add(lead)
    session.commit()
    session.refresh(lead)
    return lead


@router.post("/{lead_id}/interactions", response_model=LeadInteractionRead)
def add_interaction(lead_id: int, interaction_in: LeadInteractionCreate, session=Depends(get_session)):
    if not session.get(FamilyLead, lead_id):
        raise HTTPException(status_code=404, detail="Famille introuvable")
    interaction = LeadInteraction(lead_id=lead_id, **interaction_in.dict(exclude_unset=True))
    session.add(interaction)
    session.commit()
    session.refresh(interaction)
    return interaction


@router.get("/{lead_id}/interactions", response_model=list[LeadInteractionRead])
def list_interactions(lead_id: int, session=Depends(get_session)):
    if not session.get(FamilyLead, lead_id):
        raise HTTPException(status_code=404, detail="Famille introuvable")
    query = select(LeadInteraction).where(LeadInteraction.lead_id == lead_id).order_by(LeadInteraction.interaction_date.desc())
    return session.exec(query).all()


@router.post("/reservations", response_model=ReservationRead)
def create_reservation(reservation_in: ReservationCreate, session=Depends(get_session)):
    if not session.get(FamilyLead, reservation_in.lead_id):
        raise HTTPException(status_code=404, detail="Famille introuvable")
    reservation = Reservation(**reservation_in.dict())
    session.add(reservation)
    session.commit()
    session.refresh(reservation)
    return reservation


@router.get("/reservations", response_model=list[ReservationRead])
def list_reservations(session=Depends(get_session)):
    query = select(Reservation).order_by(Reservation.reservation_date.desc())
    return session.exec(query).all()


@router.post("/followups", response_model=AdoptionFollowUpRead)
def create_followup(followup_in: AdoptionFollowUpCreate, session=Depends(get_session)):
    if not session.get(Reservation, followup_in.reservation_id):
        raise HTTPException(status_code=404, detail="Réservation introuvable")
    followup = AdoptionFollowUp(**followup_in.dict())
    session.add(followup)
    session.commit()
    session.refresh(followup)
    return followup


@router.get("/followups", response_model=list[AdoptionFollowUpRead])
def list_followups(session=Depends(get_session), completed: bool | None = None):
    query = select(AdoptionFollowUp)
    if completed is not None:
        query = query.where(AdoptionFollowUp.completed == completed)
    query = query.order_by(AdoptionFollowUp.followup_date)
    return session.exec(query).all()
