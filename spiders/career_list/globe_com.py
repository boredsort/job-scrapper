import requests
import json

from lib2to3.pytree import Base
from bs4 import BeautifulSoup

from ..base import BaseSpider
from ..constants import NOT_FOUND, EXTRACTION_FAILED
from items.list_job_item import ListJobItem


class GlobeComSpider(BaseSpider):

    def __init__(self, params={}):
        super().__init__(params)
        self.website = 'www.globe.com'
        self._page=0
        self._list_total=0

    def crawl(self, urls):
        try:
            headers = {
                "Accept": "application/json",
                "Accept-Encoding":"gzip, deflate",
                "Accept-Language":"en-US",
                "Connection": "keep-alive",
                "Content-Type":"application/json",
                "DNT":"1",
                "Host": "globe.wd3.myworkdayjobs.com",
                "Origin":"https://globe.wd3.myworkdayjobs.com",
                "Referer": "https://globe.wd3.myworkdayjobs.com/GLB_Careers",
                "Sec-Fetch-Dest":"empty",
                "Sec-Fetch-Mode":"cors",
                "Sec-Fetch-Site":"same-origin",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0",
            }
            offset= self._page * 20

            payload = {"appliedFacets":{},"limit":20,"offset":offset,"searchText":""}

            api_url = 'https://globe.wd3.myworkdayjobs.com/wday/cxs/globe/GLB_Careers/jobs'
            response = requests.post(api_url, headers=headers, data=json.dumps(payload))

            if response.status_code in [200, 201]:
                response.encoding = 'utf-8'
                result = { 
                    'raw': response.text,
                    'url': response.url
                }

                return result
        except requests.exceptions.HTTPError:
            return {'error': "HTTP ERROR", "url": response.url }

        raise Exception('Unhandled Exception')

    def parse(self, result):

        try:
            _json = json.loads(result['raw'])
        except:
            pass
            # should return something her

        # the page total only is only found on the offset = 0 request. so store it on the variable
        current_page = 0
        list_total = result['raw']
        if list_total:
             self._list_total = list_total
        
        list_jobs = ListJobItem(result['url'], self.website)

        items = self._get_all_items(current_page)

        current_page
        
    def _get_all_items(self, current_page):

        pass
    # extract data here
    # https://globe.wd3.myworkdayjobs.com/wday/cxs/globe/GLB_Careers/jobs
    # use this as the body
    # {"appliedFacets":{},"limit":20,"offset":0,"searchText":""}