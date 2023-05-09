
import re
import uuid
from datetime import date, datetime
from typing import List

import pymongo


class SitesClient:


    def __init__(self):
        self._client = pymongo.MongoClient('mongodb://172.17.0.2:27017')
        self._db = self._client['dbjobscraper']
        self._collection = self._db['company_sites']

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

        created_tasks = []
        if items:

            task_id = None

            # connect to task collection
            task_con = self._db['task']

            for item in items:
                task_id = self.create_task_id(item.get('site_id'))
                task = {
                    "task_id": task_id,
                    "started_date": None,
                    "finished_date": None,
                    "error_message": None
                }
                
                new_task = task_con.insert_one(task)
                created_tasks.append(new_task.inserted_id)

        return created_tasks

    def get_tasks(self, **kwargs) -> List:

        """
        Return task base on ids or date
        Prioritize ids
        """
        target_date = None
        target_ids = []
        if kwargs and 'target_ids' in kwargs:
            target_ids = kwargs.get('target_ids')

        elif kwargs and 'target_date' in kwargs:
            target_date = kwargs.get('target_date')

        else:
            target_date = str(date.today())

        tasks = []

        try:
            # connect to task collection
            task_con = self._db['task']
            if target_ids:
                for _id in target_ids:
                    task = task_con.find_one({"task_id": _id})
                    if task:
                        tasks.append(task)


            elif target_date:
                t_rgx = re.compile(f'{target_date}:([a-z,A-Z,0-9,-]+)')

                for found in task_con.find({"task_id": t_rgx}):
                    tasks.append(found)

        except:
            pass
        return tasks
    
    def update_task(self, task_id, **kwargs):
        started_date = None
        finished_date = None
        error_msg = None

        values = {}

        try:
            if kwargs: 
                started_date = kwargs.get('started_date')
                finished_date = kwargs.get('finished_date')
                error_msg = kwargs.get('error_message')

                if started_date:
                    values.update({'started_date': started_date})
                if finished_date:
                    values.update({'finished_date': finished_date})
                if error_msg:
                    values.update({'error_message': error_msg})

            
            doc = self._collection.find_one_and_update({'task_id': task_id},
                                                        {'$inc': values})
            if doc:
                return True

        except:
            pass
        return None


    def get_site_by_id(self, site_id):

        found = None
        try:
            found = self._collection.find_one({
                "site_id": site_id
            })
        except:
            pass

        return found

    @staticmethod
    def create_task_id(uuid):
        stamp = datetime.now().timestamp()
        today = str(date.today())

        return f'{today}:{uuid}:{stamp}'

    @staticmethod
    def create_uuid(url):
        if 'http' not in url:
            url = f'https://{url}' 

        return str(uuid.uuid3(uuid.NAMESPACE_DNS, url))

    @staticmethod
    def get_site_id(task_id):
        try:
            return task_id.split(':')[1]
        except:
            pass

        return None


# target = ['www.google.com', 'www.hov.co']
# target = ['__all__']

# print('Loading websites..')
# sites = SitesClient()
# print('Creating task..')
# created_tasks = sites.create_tasks(target)
# print('Task created')
# print('Executing task')
# # sites.get_tasks(target_ids=['2023-05-05:d3d3Lmdsb2JlLmNvbS5waA:1683291905.424073', '2023-05-05:d3d3Lmhvdi5jbw:1683291956.781889'])
# taks = sites.get_tasks(target_date='2023-05-05')

'''
    Task format should be
    {
        "task_id": "2023-02-17:0000-000000000",
        "started_date": "<somedatetime>",
        "finished_date": "<somedatetime>",
        "error_message": ""
    }



'''