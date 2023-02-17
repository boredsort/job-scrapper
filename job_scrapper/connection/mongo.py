
import re
import uuid
from datetime import date
from typing import List

import pymongo



class SitesClient:


    def __init__(self):
        self._client = pymongo.MongoClient('mongodb://localhost:27017')
        self._db = self._client['dbjobscraper']
        self._collection = self._db['company_websites']

    def create_tasks(self, websites: List):

        items = []
        if '__all__' in websites:
            for site in self._collection.find():
                items.append(site)
        else:
            # for a specific website only
            for site in websites:
                found = self._collection.find_one({
                    'uuid': self.create_uuid(site)
                })

                if found:
                    items.append(found)

        today = str(date.today())
        task_id = None

        # connect to task collection
        task_con = self._db['task']

        created_tasks = []

        for item in items:
            task_id = self.create_task_id(today, item.get('uuid'))
            task = {
                "task_id": task_id,
                "started_date": None,
                "finished_date": None,
                "error_message": None
            }
            
            task_con.insert_one(task)
            created_tasks.append(task)

        return created_tasks

    def get_tasks(self, target_date=None) -> List:

        if not target_date:
            target_date = str(date.today())


        tasks = []

        try:
            # connect to task collection
            task_con = self._db['task']
            t_rgx = re.compile(f'{target_date}:([a-z,A-Z,0-9,-]+)')

            for found in task_con.find({"task_id": t_rgx}):
                tasks.append(found)


            print(tasks)

        except:
            pass
        return tasks



    @staticmethod
    def create_task_id(date, uuid):
        return f'{date}:{uuid}'

    @staticmethod
    def create_uuid(url):
        if 'http' not in url:
            url = f'https://{url}' 

        return str(uuid.uuid3(uuid.NAMESPACE_DNS, url))

target = ['www.google.com', 'www.hov.co']
# target = ['__all__']

sites = SitesClient()
# sites.create_tasks(target)
sites.get_tasks()

'''
    Task format should be
    {
        "task_id": "2023-02-17:0000-000000000",
        "started_date": "<somedatetime>",
        "finished_date": "<somedatetime>",
        "error_message": ""
    }



'''