from core.rabbit.rabbit_client import RabbitClient
from core.transforms.event_builder import EventBuilder
import json

class RabbitPublisher:
    def __init__(self, rabbit_client: RabbitClient, event_builder: EventBuilder):
        if (isinstance(rabbit_client, RabbitClient)):
            self.rabbit_client = rabbit_client
        if (isinstance(event_builder, EventBuilder)):
            self.event_builder = event_builder 

    def publish_printer_event(self):
        try:
            printer_events = self.event_builder.build_printer_event()
            print(printer_events)
            for event in printer_events:
                event = json.dumps(event, default=str)
                self.rabbit_client.publish("printer_event", event)
        except:
            print("Lista Vazia")

    def publish_job_event(self):
        try:
            job_events = self.event_builder.build_job_event()
            for event in job_events:
                event=json.dumps(event, default=str)
                self.rabbit_client.publish("job_event", event)
        except:
            pass
