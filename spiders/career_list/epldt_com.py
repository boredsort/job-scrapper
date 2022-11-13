from bs4 import BeautifulSoup

from ..base import BaseSpider
from ..constants import NOT_FOUND, EXTRACTION_FAILED
from items.list_job_item import ListJobItem


class Epldt_ComListSpider(BaseSpider):

    def __init__(self, params={}):
        super().__init__(params)
        self.website = 'www.epldt.com'


    def crawl(self, urls):
        pass

    def parse(self, result):
        pass

    'https://www.epldt.com/careers/'