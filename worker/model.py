from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    ForeignKey,
    JSON
)
from sqlalchemy.orm import relationship
from db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    email = Column(String(120), unique=True, nullable=True)


class Printer(Base):
    __tablename__ = "printers"

    id = Column(Integer, primary_key=True)

    # Identidade
    printer_id = Column(String(100), unique=True, nullable=True)
    printer_uuid = Column(String(100), unique=True, nullable=True)

    # Descrição
    name = Column(String(100), nullable=True)
    uri_supported = Column(Text, nullable=True)
    location = Column(String(200), nullable=True)
    info = Column(Text, nullable=True)

    # Controle
    created_at = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, nullable=True)

    # Relacionamentos
    states = relationship(
        "PrinterState",
        back_populates="printer",
        cascade="all, delete-orphan"
    )

    print_jobs = relationship(
        "PrintJob",
        back_populates="printer",
        cascade="all, delete-orphan"
    )


class PrinterState(Base):
    __tablename__ = "printer_states"

    id = Column(Integer, primary_key=True)

    printer_id = Column(
        Integer,
        ForeignKey("printers.id"),
        nullable=False
    )

    # Estado da impressora
    is_accepting_jobs = Column(Boolean, nullable=True)
    state = Column(String(50), nullable=True)
    state_message = Column(Text, nullable=True)
    state_reasons = Column(Text, nullable=True)
    queued_job_count = Column(Integer, nullable=True)

    # Snapshot temporal
    created_at = Column(DateTime, default=datetime.utcnow)

    printer = relationship("Printer", back_populates="states")


class PrintJob(Base):
    __tablename__ = "print_jobs"

    id = Column(Integer, primary_key=True)

    cups_job_id = Column(Integer, nullable=False)

    printer_id = Column(
        Integer,
        ForeignKey("printers.id"),
        nullable=False
    )

    printer = relationship("Printer", back_populates="print_jobs")

    state = Column(String(50), nullable=True)
    user_name = Column(String(100), nullable=True)
    file_name = Column(String(255), nullable=True)

    raw_payload = Column(JSON, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
