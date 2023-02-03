from bs4 import BeautifulSoup

from ..base import BaseSpider
from ..constants import NOT_FOUND, EXTRACTION_FAILED
from items.list_job_item import ListJobItem


class MeldcxComListSpider(BaseSpider):

    def __init__(self, params={}):
        super().__init__(params)
        self.website = 'www.meldcx.com'

    def parse(self, result):

        soup = BeautifulSoup(result['raw'], 'lxml')
        tags = self.get_job_tags(soup)

        list_jobs = ListJobItem(result['url'], self.website)

        for tag in tags:
            job_title = self.get_title(tag)
            url = self.get_url(tag)
            location = self.get_location(tag)
            list_jobs.append_job_list({
                "title": job_title,
                "url": url,
                "location": location
            })
        return list_jobs
        
    def crawl(self, urls):
        result = super().crawl(urls)
        
        return self.parse(result)

    def get_job_tags(self, soup):
        tags = soup.select('.collection-item-content-wrapper')
        if tags:
            return tags
        return None

    def get_title(self, job_tag):
        value = NOT_FOUND
        try:
            if job_tag:
                tag = job_tag.select_one('.card-item-title.job')
                if tag:
                    value = tag.get_text().strip()
        except:
            value = EXTRACTION_FAILED
        return value

    def get_location(self, job_tag):
        value = NOT_FOUND
        try:
            if job_tag:
                tag = job_tag.select_one('.location-text')
                if tag:
                    value = tag.get_text().strip()
        except:
            value = EXTRACTION_FAILED
        return value

    def get_url(self, job_tag):
        value = NOT_FOUND
        try:
            if job_tag:
                tag = job_tag.select_one('.link-wrapper.careers a')
                if tag:
                    value = tag['href']
        except:
            value = EXTRACTION_FAILED
        return value

    