import json
from rabbit_client import RabbitClient
from db import SessionLocal
from printer_added import handle_printer_added

RABBIT_URL = "amqps://ykcdgrfj:OCn_ZAIrZxkwvRpWUY2ZUGKLUiQPDBAm@kangaroo.rmq.cloudamqp.com/ykcdgrfj"
QUEUE = "printer_event"

rabbit = RabbitClient(RABBIT_URL)

def on_message(payload):
    if not isinstance(payload, list):
        payload = [payload]

    db = SessionLocal()
    try:
        for event in payload:
            if event.get("type") == "added":
                handle_printer_added(event, db)

        db.commit()
    except Exception as e:
        db.rollback()
        print("Erro ao salvar evento:", e)
    finally:
        db.close()

rabbit.consume_added(QUEUE, on_message)
