from typing import Optional
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String, Text, Date
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Mapped, mapped_column, relationship
from flask_login import UserMixin
import enum
from datetime import date, timedelta

class Base(DeclarativeBase, MappedAsDataclass):
    pass

db = SQLAlchemy(model_class=Base)

class Status(enum.Enum):
    NOT_APPLIED = "Pas encore postulé"
    APPLIED_WAITINGFORREPLY = "Postulé, attente d'une réponse"
    APPLIED_WAITINGFORINTERVIEW = "Postulé, entretien prévu"
    INTERVIEWED_WAITINGFORREPLY = "Entretien passé, attente d'une réponse"
    REFUSED = "Refusé"
    CANCELLED = "Annulé"

class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    # TODO ntfy_endpoint: Mapped[str] = mapped_column(String(255))
    job_offers: Mapped[list["JobOffer"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def get_id(self):
        return self.id
    
class JobOffer(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"), nullable=False)
    company: Mapped["Company"] = relationship(back_populates="job_offers")
    
    location: Mapped[str] = mapped_column()
    status: Mapped["Status"]
    application_date: Mapped[date] = mapped_column(Date, nullable=False)
    reminder_date: Mapped[Optional[date]] = mapped_column(Date)

    notes: Mapped[str] = mapped_column(Text)
    resume: Mapped[str] = mapped_column(String(255))
    application_letter: Mapped[str] = mapped_column(Text)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.application_date and not self.reminder_date:
            self.reminder_date = self.application_date + timedelta(days=7)

class Company(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    website: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    notes: Mapped[str] = mapped_column(Text)

    job_offers: Mapped[list["JobOffer"]] = relationship(back_populates="company")
