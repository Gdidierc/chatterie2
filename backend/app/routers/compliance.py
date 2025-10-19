from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from ..database import get_session
from ..models import ComplianceReminder, DocumentAttachment
from ..schemas import (
    ComplianceReminderCreate,
    ComplianceReminderRead,
    DocumentAttachmentCreate,
    DocumentAttachmentRead,
)

router = APIRouter(prefix="/compliance", tags=["conformité"])


@router.post("/reminders", response_model=ComplianceReminderRead)
def create_reminder(reminder_in: ComplianceReminderCreate, session=Depends(get_session)):
    reminder = ComplianceReminder(**reminder_in.dict(exclude_unset=True))
    session.add(reminder)
    session.commit()
    session.refresh(reminder)
    return reminder


@router.get("/reminders", response_model=list[ComplianceReminderRead])
def list_reminders(session=Depends(get_session), completed: bool | None = None):
    query = select(ComplianceReminder)
    if completed is not None:
        query = query.where(ComplianceReminder.completed == completed)
    query = query.order_by(ComplianceReminder.due_date)
    return session.exec(query).all()


@router.patch("/reminders/{reminder_id}", response_model=ComplianceReminderRead)
def update_reminder(reminder_id: int, reminder_in: ComplianceReminderCreate, session=Depends(get_session)):
    reminder = session.get(ComplianceReminder, reminder_id)
    if not reminder:
        raise HTTPException(status_code=404, detail="Rappel introuvable")
    for field, value in reminder_in.dict(exclude_unset=True).items():
        setattr(reminder, field, value)
    session.add(reminder)
    session.commit()
    session.refresh(reminder)
    return reminder


@router.post("/attachments", response_model=DocumentAttachmentRead)
def create_attachment(attachment_in: DocumentAttachmentCreate, session=Depends(get_session)):
    attachment = DocumentAttachment(**attachment_in.dict(exclude_unset=True))
    session.add(attachment)
    session.commit()
    session.refresh(attachment)
    return attachment


@router.get("/attachments", response_model=list[DocumentAttachmentRead])
def list_attachments(session=Depends(get_session), cat_id: int | None = None, kitten_id: int | None = None):
    query = select(DocumentAttachment)
    if cat_id is not None:
        query = query.where(DocumentAttachment.cat_id == cat_id)
    if kitten_id is not None:
        query = query.where(DocumentAttachment.kitten_id == kitten_id)
    query = query.order_by(DocumentAttachment.id.desc())
    return session.exec(query).all()
