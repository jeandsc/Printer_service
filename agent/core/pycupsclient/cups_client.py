import cups
from time import sleep, time

class CupsClient:
    def __init__(self, max_retries = 4, retry_delay =2):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.conn  = self.connect()
        #self.last_printers = {}
        #self.last_jobs = {}
        self.timestamp_connection = 0
        #self.timestamp_jobs = 0
    def connect(self):
        attempt = 0
        while attempt < self.max_retries:
            try:
                self.conn = cups.Connection(host="localhost", port=631)
                #print("Conectado ao CUPS")
                return self.conn
            except (cups.IPPError, cups.HTTPError, RuntimeError) as e:
                attempt += 1
                #print(f"Tentativa {attempt} falhou: {e}")
                sleep(self.retry_delay**attempt)
        #print("Não foi possível conectar ao CUPS após várias tentativas")
        self.conn = None
        return None
    def list_printers(self):
        if not(self.conn is None):
            try:
                printers = self.conn.getPrinters()
                #self.last_printers = printers
                #self.timestamp_printers = time()
                self.timestamp_connection = time()
                return list(printers.keys())
            except:
                #print("Erro ao listar impressoras:")
                return None
        
        return None

        
    
    def list_jobs(self):
        if not(self.conn is None):
            try:
                jobs = self.conn.getJobs(which_jobs='all', my_jobs=False)
                self.timestamp_connection = time()
                return list(jobs.keys())
            except:
                print("Erro ao listar Trabalhos:")
                return None

        return None

    def get_printer(self, name: str):
        if not(self.conn is None):
            try:
                printer = self.conn.getPrinterAttributes(name)
                self.timestamp_connection = time()
                return printer
            except:
                print("Erro ao listar impressoras:")
                return None

        return None
        #if 

    def get_job(self, job_id: int):
        if not(self.conn is None):
            try:

                job = self.conn.getJobAttributes(job_id)
                self.timestamp_connection = time()
                return job
            except:
                print("Erro ao listar trabalho:")
                return None
        return None
    def get_timestamp_conn(self):
        return self.timestamp_connection
        
if __name__ == "__main__":
    a = CupsClient()
    #print(a.list_printers())
    print(a.list_jobs())
    #print(a.get_printer(a.list_printers()[0]))
    print("###########################################################")
    #print(a.get_job(a.list_jobs()[0]))
    for atribute in a.get_job(a.list_jobs()[0]).keys():
        print(atribute)