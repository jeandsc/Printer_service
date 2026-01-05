from core.pycupsclient.cups_client import CupsClient
import os, json

RELEVANT_PRINTER_ATTRIBUTES = [
    "printer-is-accepting-jobs",
    "printer-state",
    "printer-state-message",
    "printer-state-reasons",
    "queued-job-count",
    "printer-uri-supported",
    "printer-location",
    "printer-info",
    "printer-uuid",
    "printer-id",
    "printer-name"
]

STATE_PATH = os.path.join(
    os.path.dirname(__file__),   
    "..",
    "state",
    "state_printers.json"
)
STATE_PATH = os.path.abspath(STATE_PATH)

def minimize_dict(dictionaire: dict, keys: list):
    minimized_dict = dict()
    for key in keys:
        minimized_dict[key] = dictionaire[key]
    return minimized_dict


class PrinterService:

    def __init__(self, cups_client: CupsClient):
        self.cups_client = cups_client
        self.printers_previous_state = self.load_state()

    def save_state(self, state: dict):
        if isinstance(state, dict):
            self.printers_previous_state = state
            os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)

            with open(STATE_PATH, "w", encoding="utf-8") as f:
                json.dump(state, f)
            
    
    def load_state(self):
        if not os.path.exists(STATE_PATH):
            return {}

        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def fetch_current_state(self):
        printers = self.cups_client.list_printers()
        if not(printers==None):
            current_state = dict()
            for printer in printers:
                printer_state = self.cups_client.get_printer(printer)
                printer_state = minimize_dict(printer_state, RELEVANT_PRINTER_ATTRIBUTES)
                current_state[printer] = printer_state
                #printer_state None, impressora offline
            
            

            return current_state
        #Retorno none = igual a falha global
        return None


    def detect_changes(self):
        current = self.fetch_current_state()
        if not(current ==None):
            if self.printers_previous_state != current:
                return True
            return False
        
        ####Sem conexão
        return None
    def build_printer_events(self):
        previous = self.printers_previous_state
        current = self.fetch_current_state()
        payload = dict()

        payload['added'] = self.printers_added(previous, current)
        payload['removed'] = self.printers_removed(previous, current)
        payload['updates'] = self.printers_updates(previous, current)
        self.save_state(current)
        return payload
    def printers_added(self, previous: dict, current:dict):
        if not(isinstance(current, dict)):
            return []
        previous_printers = set(previous.keys())
        current_printers = set(current.keys())
        if previous_printers == current_printers:
            return []
        if not(previous_printers==current_printers):
            return list(current_printers.difference(previous_printers))
    
    def printers_removed(self, previous: dict, current:dict):
        if not(isinstance(current, dict)):
            return []
        previous_printers = set(previous.keys())
        current_printers = set(current.keys())
        if previous_printers == current_printers:
            return []
        if not(previous_printers==current_printers):
            removed= list(previous_printers.difference(current_printers))
            printers_removed = list()
            for printer_rmv in removed:
                uuid =previous.get(printer_rmv).get('printer-uuid')
                printers_removed.append((printer_rmv, uuid))
            return printers_removed
    def printers_updates(self, previous:dict, current:dict):
        if not(isinstance(current, dict)):
            return {}
        if (list(previous.keys())==[]):
            return current
        updates = {}
        for printer in current.keys():
            try:
                updates[printer] = self.compare_printers(previous[printer], current[printer])
                if not(updates[printer] =={}):
                    updates[printer]['printer-name'] = current[printer].get('printer-name')
                    updates[printer]['printer-uuid'] = current[printer].get('printer-uuid')
            except:
                updates[printer] = current[printer]
        return updates
    def compare_printers(self, previous_printer:dict, current_printer:dict):
        if not(isinstance(previous_printer, dict)):
            return {}
        if not(isinstance(current_printer, dict)):
            return {}
        if not(previous_printer.keys()==current_printer.keys()):
            return {}
        updates = {}
        for key in previous_printer.keys():
            if current_printer.get(key)!=previous_printer.get(key):
                updates[key] =current_printer.get(key)
            
        return updates
if __name__ == "__main__":
    cupsclient = CupsClient()
    printerservice = PrinterService(cupsclient)
    '''
    for i in [x for x in printerservice.fetch_current_state().get("imp1").keys()]:
        print(i)
    '''
    #print(printerservice.fetch_current_state())
    #print(printerservice.detect_changes())
    a = printerservice.build_printer_events()
    print(a)
    #printerservice.save_state(1)
    print([printerservice.fetch_current_state().keys()])
    #print(printerservice.fetch_current_state().get("imp1").keys())
    #a = {}
    #print(list(a.keys()))