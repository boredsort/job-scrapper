import json
from datetime import datetime, timezone

class ListJobItem:

    def __init__(self, source_url, site):
        self.createdAt = datetime.now(timezone.utc).isoformat()
        self.site = site
        self.url = source_url
        self.joblist = []
    
    def append_job_list(self, job):
        if isinstance(job, dict):
            self.joblist.append(job)
        else:
            raise Exception('Job is a dictionary with keys value and url') 

    def get_job_list(self):
        return self.joblist   

    def __str__(self):
        return str(self.joblist)

    def __len__(self):
        return len(self.joblist)

    def convert_to_collection(self):

        col = {
            "createdAt": self.createdAt,
            "website": self.site,
            "source_url": self.url,
            "jobs_list": self.joblist
        }

        return col
    