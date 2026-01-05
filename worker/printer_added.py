from datetime import datetime
from sqlalchemy.orm import Session
from model import Printer, PrinterState
import json

def handle_printer_added(event: dict, db: Session):
    data = event["data"]

    printer = (
        db.query(Printer)
        .filter(
            (Printer.printer_id == data.get("printer-id")) |
            (Printer.printer_uuid == data.get("printer-uuid"))
        )
        .first()
    )

    if printer:
        printer.last_seen = datetime.utcnow()
        db.commit()
        return

    printer = Printer(
        printer_id=data.get("printer-id"),
        printer_uuid=data.get("printer-uuid"),
        name=data.get("printer-name"),
        location=data.get("printer-location"),
        info=data.get("printer-info"),
        created_at=datetime.utcnow(),
        last_seen=datetime.utcnow()
    )

    db.add(printer)
    db.flush()  # garante printer.id

    state = PrinterState(
        printer_id=printer.id,
        is_accepting_jobs=data.get("printer-is-accepting-jobs"),
        state=data.get("printer-state"),
        state_message=data.get("printer-state-message"),

        # 🔧 CORREÇÃO AQUI
        state_reasons=json.dumps(
            data.get("printer-state-reasons", [])
        ),

        queued_job_count=data.get("queued-job-count"),
        created_at=datetime.utcnow()
    )

    db.add(state)
    db.commit()
