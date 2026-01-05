import time
from rabbit_client import RabbitClient
from db import SessionLocal
from printer_added import handle_printer_added

RABBIT_URL = "amqps://ykcdgrfj:OCn_ZAIrZxkwvRpWUY2ZUGKLUiQPDBAm@kangaroo.rmq.cloudamqp.com/ykcdgrfj"
QUEUE = "printer_event"
RETRY_DELAY = 5  # segundos

def process_message(payload):
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
        print("Erro ao processar mensagem:", e)
    finally:
        db.close()

def main():
    print("Worker de impressoras rodando.")

    while True:
        rabbit = RabbitClient(RABBIT_URL)
        try:
            rabbit.consume_added(QUEUE, process_message)
        except Exception as e:
            print("Falha no consumo:", e)
            rabbit.close()
            print(f"Reconectando em {RETRY_DELAY}s...")
            time.sleep(RETRY_DELAY)

if __name__ == "__main__":
    main()
