from core.printers.printers_service import PrinterService
from core.jobs.jobs_service import JobService
from core.pycupsclient.cups_client import CupsClient
from time import time, sleep

class EventBuilder:
    def __init__(self, printer_service: PrinterService, job_service: JobService):
        self.printer_service = printer_service
        self.job_service = job_service
        pass
    def build_printer_event(self):
        payload = list()
        events = self.printer_service.build_printer_events()

        #print(events['added'])
        if not(events['added'] == []):
            printers_add = events['added']
            for printer in printers_add:
                
                message = dict()
                message['type'] = 'added'
                message['data'] = events['updates'].get(printer)
                message['timestamp'] = time()

                payload.append(message)
        if not(events['removed']==[]):
            printers_rmv= events['removed']
            for printer in printers_rmv:
                
                message = dict()
                message['type'] = 'removed'
                message['data'] = printer
                message['timestamp'] = time()

                payload.append(message)
        if not(events['updates']=={}):
            
            printers_updates = set(events['updates'].keys()).difference(set(events['added']))

            for printer in printers_updates:

                message = dict()
                message['type'] = 'updated'
                message['data'] = events['updates'].get(printer)
                message['timestamp'] = time()

                if not(message['data'] == {}):
                    payload.append(message)
                
        return payload            


    def build_job_event(self):
        payload = list()
        events  = jobservice.build_job_events()
        if events == {}:
            return payload
        for job in events.keys():
            message = dict()
            message['type'] = 'job'
            message['data'] = events[job]
            message['timestamp'] = time()
            payload.append(message)
        return payload

    def add_metadata(self, event): ...

if __name__ =='__main__':
    cupsclient = CupsClient()
    printerservice = PrinterService(cupsclient)
    jobservice = JobService(cupsclient)
    eventbuilder = EventBuilder(printerservice, jobservice)
    i = 0
    #print(eventbuilder.build_printer_event())
    while(True):
        print(eventbuilder.build_printer_event())
        sleep(5)
        i+=1
        print(i)