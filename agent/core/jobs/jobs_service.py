from core.pycupsclient.cups_client import CupsClient
import os, json



STATE_PATH = os.path.join(
    os.path.dirname(__file__),   
    "..",
    "state",
    "state_jobs.json"
)
STATE_PATH = os.path.abspath(STATE_PATH)
class JobService:
    def __init__(self, cups_client: CupsClient):
        self.cups_client = cups_client
        self.jobs_previous_state = self.load_state()
    
    def save_state(self, state: dict):
        if isinstance(state, dict):
            self.jobs_previous_state = state
            os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)

            with open(STATE_PATH, "w", encoding="utf-8") as f:
                json.dump(state, f)
            
    def load_state(self):
        if not os.path.exists(STATE_PATH):
            return {}

        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)


    def fetch_current_state(self):
        jobs = self.cups_client.list_jobs()
        if not(jobs==None):
            current_state = dict()
            for job in jobs:
                job_state = self.cups_client.get_job(job)

                current_state[job] = job_state
                #job_state None,  erro de rede
            
            

            return current_state
        #Retorno none = igual a falha global
        return None

    def filter_completed(self, jobs: dict):
        if isinstance(jobs, dict):
            filter = [job for job in jobs if (jobs.get(job).get('job-state')==9 or jobs.get(job).get('job-state')=='completed')]
            filtered = dict()
            for key in filter:
                filtered[key] = jobs[key]
            return filtered
        return {}

    def detect_new_jobs(self, current:dict, previous:dict):
        if not(isinstance(current, dict)):
            return False
        
        if current == {}:
            return False
        
        if self.filter_completed(current) == self.filter_completed(previous):
            return False
        return True
        
    def compare_jobs(self, job_current: dict, job_previous: dict):
        if not(isinstance(job_current, dict)):
            return None
        if not(isinstance(job_previous, dict)):
            return None
        try:
            if job_current['job-uuid'] == job_previous['job-uuid']: return True
            else: return False
        except:
            return False
    def identify_new_jobs(self, current: dict, previous: dict):
        if not(isinstance(current,dict)):
            return {}
        if not(isinstance(previous,dict)):
            return {}
        if previous =={}:
            return current
        new_jobs = dict()

        for key_current in current.keys():
            current_job = current.get(key_current)
            equals = False
            for key_previous in previous.keys():
                previous_job = previous.get(key_previous)
                equals = equals or self.compare_jobs(current_job, previous_job)
            if equals is False:
                new_jobs[key_current] = current[key_current]
        return new_jobs
            
                
    def build_job_events(self):
        previous = self.jobs_previous_state
        current =self.fetch_current_state()
        #print(current)
        current = self.filter_completed(current)
        #print(current)
        payload  = self.identify_new_jobs(current, previous)
        self.save_state(current)
        self.jobs_previous_state = current
        return payload

if __name__ == "__main__":
    cupsclient = CupsClient()
    jobservice = JobService(cupsclient)
    
    #print(jobservice.filter_completed(jobservice.fetch_current_state()))

    #print(jobservice.detect_new_jobs(jobservice.fetch_current_state(), {}))
    a = jobservice.fetch_current_state().get(1)
    b = jobservice.fetch_current_state().get(2)
    print(jobservice.build_job_events())