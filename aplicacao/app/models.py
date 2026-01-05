from datetime import datetime, timezone
from app import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)










class Printer(db.Model):
    __tablename__ = "printers"

    id = db.Column(db.Integer, primary_key=True)

    # Identidade
    printer_id = db.Column(db.String(100), unique=True, nullable=True)
    printer_uuid = db.Column(db.String(100), unique=True, nullable=True)

    # Descrição
    name = db.Column(db.String(100), nullable=True)
    uri_supported = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(200), nullable=True)
    info = db.Column(db.Text, nullable=True)

    # Controle
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, nullable=True)

    # Relacionamento
    states = db.relationship(
        "PrinterState",
        back_populates="printer",
        cascade="all, delete-orphan"
    )

    print_jobs = db.relationship(
    "PrintJob",
    back_populates="printer",
    cascade="all, delete-orphan"
)



class PrinterState(db.Model):
    __tablename__ = "printer_states"

    id = db.Column(db.Integer, primary_key=True)

    printer_id = db.Column(
        db.Integer,
        db.ForeignKey("printers.id"),
        nullable=False
    )

    # Estado da impressora
    is_accepting_jobs = db.Column(db.Boolean, nullable=True)
    state = db.Column(db.String(50), nullable=True)
    state_message = db.Column(db.Text, nullable=True)
    state_reasons = db.Column(db.Text, nullable=True)
    queued_job_count = db.Column(db.Integer, nullable=True)

    # Timestamp do snapshot
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    printer = db.relationship("Printer", back_populates="states")

class PrintJob(db.Model):
    __tablename__ = "print_jobs"

    id = db.Column(db.Integer, primary_key=True)

    # Identidade mínima
    cups_job_id = db.Column(db.Integer, nullable=False)

    printer_id = db.Column(
        db.Integer,
        db.ForeignKey("printers.id"),
        nullable=False
    )

    printer = db.relationship("Printer", back_populates="print_jobs")

    # Campos que você QUASE COM CERTEZA vai usar
    state = db.Column(db.String(50), nullable=True)
    user_name = db.Column(db.String(100), nullable=True)
    file_name = db.Column(db.String(255), nullable=True)

    # Payload completo do CUPS
    raw_payload = db.Column(db.JSON, nullable=False)

    # Controle temporal
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)