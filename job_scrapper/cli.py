import argparse
import threading
import datetime
from typing import List

from connection.sites_client import SitesClient
from connection import mongo_client
from factory import SpiderFactory
from utils import clean_website



def crawl_sites(websites: List):

    connection = SitesClient()
    connection.create_tasks(websites)

# print('Loading websites..')
# sites = SitesClient()
# print('Creating task..')
# created_tasks = sites.create_tasks(target)
# print('Task created')
# print('Executing task')
# # sites.get_tasks(target_ids=['2023-05-05:d3d3Lmdsb2JlLmNvbS5waA:1683291905.424073', '2023-05-05:d3d3Lmhvdi5jbw:1683291956.781889'])
    tasks = connection.get_tasks()
    # tasks = connection.get_tasks()

    # target sites are the sites that have spiders, as websites list can have random websites.
    target_sites  = []
    for task in tasks:
        task_id = task['task_id']
        site_id = connection.get_site_id(task_id)
        target = connection.get_site_by_id(site_id)
        target_sites.append((target, task))


    for target_site, _task in target_sites:

        website = target_site.get('url')
        career_page = target_site.get('careers_url')
        url = f'https://{career_page}'
        factory = SpiderFactory()
        spider = factory.spawn_listSpider(website)()
        # future idea, task should be a class, and should have task function
        start_time = datetime.datetime.utcnow()
        result = spider.crawl(url)
        
        success, error_msg = mongo_client.save_scraped(result.convert_to_collection())
        finished_time = datetime.datetime.utcnow()
        connection.update_task(_task['task_id'],
            started_date=start_time,
            finished_date=finished_time,
            error_message=error_msg
        )
        # update task if finised
        # update also errors
        

    success = True
    return success


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--site", help="Set the site or sites to run")

    args = parser.parse_args()

    if not args.site:
        args.site = '__all__'

    if args.site:
        target_sites = [args.site]
        crawl_sites(target_sites)

    


if __name__ == "__main__":
    main()