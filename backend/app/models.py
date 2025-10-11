from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


class Cat(SQLModel, table=True):
    __tablename__ = "cats"

    id: Optional[int] = Field(default=None, primary_key=True)
    call_name: str = Field(index=True)
    pedigree_name: Optional[str] = None
    birth_date: Optional[date] = None
    sex: Optional[str] = Field(description="M/F")
    color_ems: Optional[str] = Field(description="EMS code (FIFe)")
    status: str = Field(default="chaton")
    microchip: Optional[str] = Field(default=None, unique=True, index=True)
    cat_id_number: Optional[str] = Field(default=None, description="CatID/registre")
    eu_passport: Optional[str] = None
    is_neutered: bool = Field(default=False)
    sire_id: Optional[int] = Field(default=None, foreign_key="cats.id")
    dam_id: Optional[int] = Field(default=None, foreign_key="cats.id")
    notes: Optional[str] = None

    sire: Optional["Cat"] = Relationship(sa_relationship_kwargs={"remote_side": "Cat.id"}, back_populates="offspring_sired")
    dam: Optional["Cat"] = Relationship(sa_relationship_kwargs={"remote_side": "Cat.id"}, back_populates="offspring_dam")
    offspring_sired: list["Cat"] = Relationship(back_populates="sire", sa_relationship_kwargs={"primaryjoin": "Cat.sire_id==Cat.id"})
    offspring_dam: list["Cat"] = Relationship(back_populates="dam", sa_relationship_kwargs={"primaryjoin": "Cat.dam_id==Cat.id"})
    genetic_tests: list["CatGeneticTest"] = Relationship(back_populates="cat")
    health_events: list["CatHealthEvent"] = Relationship(back_populates="cat")
    measurements: list["CatMeasurement"] = Relationship(back_populates="cat")


class CatGeneticTest(SQLModel, table=True):
    __tablename__ = "cat_genetic_tests"

    id: Optional[int] = Field(default=None, primary_key=True)
    cat_id: int = Field(foreign_key="cats.id", index=True)
    test_name: str
    status: str = Field(description="Result summary such as OK/Porteur/Atteint")
    laboratory: Optional[str] = None
    result_date: Optional[date] = None
    document_path: Optional[str] = None

    cat: "Cat" = Relationship(back_populates="genetic_tests")


class CatHealthEvent(SQLModel, table=True):
    __tablename__ = "cat_health_events"

    id: Optional[int] = Field(default=None, primary_key=True)
    cat_id: int = Field(foreign_key="cats.id", index=True)
    category: str = Field(description="vaccin, vermifuge, antiparasitaire, visite, etc.")
    label: str
    event_date: date
    due_date: Optional[date] = Field(default=None, description="Next reminder if applicable")
    notes: Optional[str] = None
    document_path: Optional[str] = None

    cat: "Cat" = Relationship(back_populates="health_events")


class CatMeasurement(SQLModel, table=True):
    __tablename__ = "cat_measurements"

    id: Optional[int] = Field(default=None, primary_key=True)
    cat_id: int = Field(foreign_key="cats.id", index=True)
    recorded_at: datetime = Field(default_factory=datetime.utcnow)
    weight_kg: Optional[float] = None
    length_cm: Optional[float] = None
    feeding_notes: Optional[str] = None

    cat: "Cat" = Relationship(back_populates="measurements")


class HeatCycle(SQLModel, table=True):
    __tablename__ = "heat_cycles"

    id: Optional[int] = Field(default=None, primary_key=True)
    queen_id: int = Field(foreign_key="cats.id", index=True)
    start_date: date
    end_date: Optional[date] = None
    intensity: Optional[str] = None
    notes: Optional[str] = None


class MatingRecord(SQLModel, table=True):
    __tablename__ = "mating_records"

    id: Optional[int] = Field(default=None, primary_key=True)
    queen_id: int = Field(foreign_key="cats.id", index=True)
    sire_id: int = Field(foreign_key="cats.id", index=True)
    date: date
    type: str = Field(description="interne/externe")
    contract_path: Optional[str] = None
    proof_path: Optional[str] = None
    notes: Optional[str] = None


class PregnancyTimeline(SQLModel, table=True):
    __tablename__ = "pregnancies"

    id: Optional[int] = Field(default=None, primary_key=True)
    queen_id: int = Field(foreign_key="cats.id", index=True)
    sire_id: int = Field(foreign_key="cats.id", index=True)
    mating_id: Optional[int] = Field(default=None, foreign_key="mating_records.id")
    due_date: Optional[date] = Field(description="Estimated due date")
    confirmation_date: Optional[date] = None
    notes: Optional[str] = None


class Litter(SQLModel, table=True):
    __tablename__ = "litters"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    queen_id: int = Field(foreign_key="cats.id", index=True)
    sire_id: int = Field(foreign_key="cats.id", index=True)
    mating_date: Optional[date] = None
    birth_date: Optional[date] = None
    notes: Optional[str] = None


class Kitten(SQLModel, table=True):
    __tablename__ = "kittens"

    id: Optional[int] = Field(default=None, primary_key=True)
    litter_id: int = Field(foreign_key="litters.id", index=True)
    name: str
    sire_id: Optional[int] = Field(default=None, foreign_key="cats.id")
    dam_id: Optional[int] = Field(default=None, foreign_key="cats.id")
    sex: Optional[str] = None
    color_estimate: Optional[str] = None
    birth_time: Optional[datetime] = None
    birth_weight_g: Optional[int] = None
    collar_color: Optional[str] = None
    status: str = Field(default="disponible")
    notes: Optional[str] = None


class KittenWeight(SQLModel, table=True):
    __tablename__ = "kitten_weights"

    id: Optional[int] = Field(default=None, primary_key=True)
    kitten_id: int = Field(foreign_key="kittens.id", index=True)
    recorded_at: datetime = Field(default_factory=datetime.utcnow)
    weight_g: Optional[int] = None


class FamilyLead(SQLModel, table=True):
    __tablename__ = "family_leads"

    id: Optional[int] = Field(default=None, primary_key=True)
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
    tags: Optional[str] = Field(default=None, description="comma-separated tags")
    qualification_score: Optional[int] = Field(default=None, description="0-100")
    status: str = Field(default="prospect")
    notes: Optional[str] = None


class LeadInteraction(SQLModel, table=True):
    __tablename__ = "lead_interactions"

    id: Optional[int] = Field(default=None, primary_key=True)
    lead_id: int = Field(foreign_key="family_leads.id", index=True)
    interaction_date: datetime = Field(default_factory=datetime.utcnow)
    channel: Optional[str] = None
    summary: str


class Reservation(SQLModel, table=True):
    __tablename__ = "reservations"

    id: Optional[int] = Field(default=None, primary_key=True)
    kitten_id: int = Field(foreign_key="kittens.id", index=True)
    lead_id: int = Field(foreign_key="family_leads.id", index=True)
    reservation_date: date
    deposit_amount: Optional[float] = None
    payment_schedule: Optional[str] = None
    kyc_status: Optional[str] = Field(default="pending")
    contract_path: Optional[str] = None


class AdoptionFollowUp(SQLModel, table=True):
    __tablename__ = "adoption_followups"

    id: Optional[int] = Field(default=None, primary_key=True)
    reservation_id: int = Field(foreign_key="reservations.id", index=True)
    followup_date: date
    reminder_type: str = Field(description="J+30, J+180, etc.")
    completed: bool = Field(default=False)
    notes: Optional[str] = None


class ComplianceReminder(SQLModel, table=True):
    __tablename__ = "compliance_reminders"

    id: Optional[int] = Field(default=None, primary_key=True)
    cat_id: Optional[int] = Field(default=None, foreign_key="cats.id", index=True)
    kitten_id: Optional[int] = Field(default=None, foreign_key="kittens.id", index=True)
    due_date: date
    category: str
    description: str
    completed: bool = Field(default=False)
    completed_at: Optional[datetime] = None


class DocumentAttachment(SQLModel, table=True):
    __tablename__ = "document_attachments"

    id: Optional[int] = Field(default=None, primary_key=True)
    cat_id: Optional[int] = Field(default=None, foreign_key="cats.id", index=True)
    kitten_id: Optional[int] = Field(default=None, foreign_key="kittens.id", index=True)
    litter_id: Optional[int] = Field(default=None, foreign_key="litters.id", index=True)
    lead_id: Optional[int] = Field(default=None, foreign_key="family_leads.id", index=True)
    file_path: str
    label: Optional[str] = None
    description: Optional[str] = None
