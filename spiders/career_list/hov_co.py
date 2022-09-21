from bs4 import BeautifulSoup

from ..base import BaseSpider
from ..constants import NOT_FOUND, EXTRACTION_FAILED
from items.list_job_item import ListJobItem


class HovCoListSpider(BaseSpider):

    def __init__(self, params={}):
        super().__init__(params)
        self.website = 'www.hov.co'


    def parse(self, result):
        assert isinstance(result, dict)

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
        tags = soup.select('#open-positions span + a')
        tags = soup.select('#open-positions div.justify-between.items-center')
        if tags:
            return tags
        return None
        
    def get_title(self, job_tag):
        value = NOT_FOUND
        try:
            tag = job_tag.select_one('span + a')
            if tag:
                value = tag.text.strip()
        except:
            value = EXTRACTION_FAILED
        return value

    def get_url(self, job_tag):
        value = NOT_FOUND
        try:
            tag = job_tag.select_one('a')
            if tag and tag.has_attr('href'):
                value = tag['href']
        except:
            value = EXTRACTION_FAILED
        return value

    def get_location(self, job_tag):
        value = NOT_FOUND
        try:
            tag = job_tag.select_one('.text-gray-400.ml-10.pt-2')
            if tag:
                value = tag.text.strip()
        except:
            value = EXTRACTION_FAILED
        return value
