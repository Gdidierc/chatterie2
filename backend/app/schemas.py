from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class CatBase(BaseModel):
    call_name: str
    pedigree_name: Optional[str] = None
    birth_date: Optional[date] = None
    sex: Optional[str] = None
    color_ems: Optional[str] = None
    status: Optional[str] = None
    microchip: Optional[str] = None
    cat_id_number: Optional[str] = None
    eu_passport: Optional[str] = None
    is_neutered: Optional[bool] = None
    sire_id: Optional[int] = None
    dam_id: Optional[int] = None
    notes: Optional[str] = None


class CatCreate(CatBase):
    pass


class CatRead(CatBase):
    id: int

    class Config:
        orm_mode = True


class CatUpdate(BaseModel):
    call_name: Optional[str] = None
    pedigree_name: Optional[str] = None
    birth_date: Optional[date] = None
    sex: Optional[str] = None
    color_ems: Optional[str] = None
    status: Optional[str] = None
    microchip: Optional[str] = None
    cat_id_number: Optional[str] = None
    eu_passport: Optional[str] = None
    is_neutered: Optional[bool] = None
    sire_id: Optional[int] = None
    dam_id: Optional[int] = None
    notes: Optional[str] = None


class MeasurementCreate(BaseModel):
    recorded_at: Optional[datetime] = None
    weight_kg: Optional[float] = None
    length_cm: Optional[float] = None
    feeding_notes: Optional[str] = None


class MeasurementRead(MeasurementCreate):
    id: int

    class Config:
        orm_mode = True


class GeneticTestCreate(BaseModel):
    test_name: str
    status: str
    laboratory: Optional[str] = None
    result_date: Optional[date] = None
    document_path: Optional[str] = None


class GeneticTestRead(GeneticTestCreate):
    id: int

    class Config:
        orm_mode = True


class HealthEventCreate(BaseModel):
    category: str
    label: str
    event_date: date
    due_date: Optional[date] = None
    notes: Optional[str] = None
    document_path: Optional[str] = None


class HealthEventRead(HealthEventCreate):
    id: int

    class Config:
        orm_mode = True


class LitterBase(BaseModel):
    name: str
    queen_id: int
    sire_id: int
    mating_date: Optional[date] = None
    birth_date: Optional[date] = None
    notes: Optional[str] = None


class LitterCreate(LitterBase):
    pass


class LitterUpdate(BaseModel):
    name: Optional[str] = None
    queen_id: Optional[int] = None
    sire_id: Optional[int] = None
    mating_date: Optional[date] = None
    birth_date: Optional[date] = None
    notes: Optional[str] = None


class LitterRead(LitterBase):
    id: int

    class Config:
        orm_mode = True


class KittenBase(BaseModel):
    name: str
    sire_id: Optional[int] = None
    dam_id: Optional[int] = None
    sex: Optional[str] = None
    color_estimate: Optional[str] = None
    birth_time: Optional[datetime] = None
    birth_weight_g: Optional[int] = None
    collar_color: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class KittenCreate(KittenBase):
    litter_id: int


class KittenUpdate(BaseModel):
    name: Optional[str] = None
    sire_id: Optional[int] = None
    dam_id: Optional[int] = None
    sex: Optional[str] = None
    color_estimate: Optional[str] = None
    birth_time: Optional[datetime] = None
    birth_weight_g: Optional[int] = None
    collar_color: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class KittenRead(KittenBase):
    id: int
    litter_id: int

    class Config:
        orm_mode = True


class KittenWeightCreate(BaseModel):
    recorded_at: Optional[datetime] = None
    weight_g: Optional[int] = None


class KittenWeightRead(KittenWeightCreate):
    id: int

    class Config:
        orm_mode = True


class FamilyLeadBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    has_children: Optional[bool] = None
    has_other_pets: Optional[str] = None
    allergy_notes: Optional[str] = None
    budget_range: Optional[str] = None
    preferred_color: Optional[str] = None
    preferred_gender: Optional[str] = None
    tags: Optional[str] = None
    qualification_score: Optional[int] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class FamilyLeadCreate(FamilyLeadBase):
    pass


class FamilyLeadRead(FamilyLeadBase):
    id: int

    class Config:
        orm_mode = True


class FamilyLeadUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    has_children: Optional[bool] = None
    has_other_pets: Optional[str] = None
    allergy_notes: Optional[str] = None
    budget_range: Optional[str] = None
    preferred_color: Optional[str] = None
    preferred_gender: Optional[str] = None
    tags: Optional[str] = None
    qualification_score: Optional[int] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class LeadInteractionCreate(BaseModel):
    interaction_date: Optional[datetime] = None
    channel: Optional[str] = None
    summary: str


class LeadInteractionRead(LeadInteractionCreate):
    id: int

    class Config:
        orm_mode = True


class ReservationCreate(BaseModel):
    kitten_id: int
    lead_id: int
    reservation_date: date
    deposit_amount: Optional[float] = None
    payment_schedule: Optional[str] = None
    kyc_status: Optional[str] = None
    contract_path: Optional[str] = None


class ReservationRead(ReservationCreate):
    id: int

    class Config:
        orm_mode = True


class AdoptionFollowUpCreate(BaseModel):
    reservation_id: int
    followup_date: date
    reminder_type: str
    completed: Optional[bool] = None
    notes: Optional[str] = None


class AdoptionFollowUpRead(AdoptionFollowUpCreate):
    id: int

    class Config:
        orm_mode = True


class ComplianceReminderCreate(BaseModel):
    cat_id: Optional[int] = None
    kitten_id: Optional[int] = None
    due_date: date
    category: str
    description: str
    completed: Optional[bool] = None
    completed_at: Optional[datetime] = None


class ComplianceReminderRead(ComplianceReminderCreate):
    id: int

    class Config:
        orm_mode = True


class DocumentAttachmentCreate(BaseModel):
    cat_id: Optional[int] = None
    kitten_id: Optional[int] = None
    litter_id: Optional[int] = None
    lead_id: Optional[int] = None
    file_path: str
    label: Optional[str] = None
    description: Optional[str] = None


class DocumentAttachmentRead(DocumentAttachmentCreate):
    id: int

    class Config:
        orm_mode = True
