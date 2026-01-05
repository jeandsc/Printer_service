from core.pycupsclient.cups_client import CupsClient
from core.printers.printers_service import PrinterService
from core.jobs.jobs_service import JobService
from core.rabbit.rabbit_client import RabbitClient
from core.transforms.event_builder import EventBuilder
from core.rabbit.publisher import RabbitPublisher
from time import sleep
url = ""
cups_client = CupsClient()
printer_service = PrinterService(cups_client)
job_service = JobService(cups_client)
event_builder = EventBuilder(printer_service, job_service)
rabbit_client = RabbitClient(url)
rabbit_publisher = RabbitPublisher(rabbit_client, event_builder)

def run_cycle(self): ...
def handle_printer_cycle(self): ...
def handle_job_cycle(self): ...
def sleep_until_next_cycle(self): ...

while(True):
    rabbit_publisher.publish_printer_event()
    rabbit_publisher.publish_job_event()
    sleep(5)
