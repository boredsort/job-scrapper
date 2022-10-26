import requests
import json
import math
import html
import re
from datetime import date, timedelta

from lib2to3.pytree import Base
from bs4 import BeautifulSoup

from ..base import BaseSpider
from ..constants import NOT_FOUND, EXTRACTION_FAILED
from items.list_job_item import ListJobItem


class GlobeComListSpider(BaseSpider):

    def __init__(self, params={}):
        super().__init__(params)
        self.website = 'www.globe.com'
        self._page=0
        self._list_total=0

    def crawl(self, urls):
        try:

            # url is not used here as it can be scraped through API
            result = self._get_all_items()         
            if result and 'result_items' in result and result['result_items']:
                return self.parse(result)

        except requests.exceptions.HTTPError:
            return {'error': "HTTP ERROR", "url": '' }

        except:
            pass

        return {}

    def parse(self, result):

        def _clean(string):
            return html.unescape(string).strip()

        
        list_jobs = ListJobItem(result['url'], self.website)

        try:

            for item in result['result_items']:

                if 'title' not in item:
                    continue

                BASE_URL = 'https://globe.wd3.myworkdayjobs.com/en-US/GLB_Careers'
                title = _clean(item['title'])
                url = BASE_URL + _clean(item['externalPath'])
                location = _clean(item['locationsText'])
                posted_on = self._transform_word_to_date(_clean(item['postedOn']))
                list_jobs.append_job_list({
                    "title": title,
                    "url": url,
                    "location": location,
                    'extras': {
                        "posted_on": posted_on
                    }
                })

                

        except:
            pass
            # should return something her
        
        return list_jobs

    def _get_data_api(self):    

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
                return response
        except:
            pass
        return None
        
    def _get_all_items(self):

        current_page = 0
        init_url = ''
        total_page = 0

        items = []
        has_next = True
        try:
            while has_next:
                response = self._get_data_api()

                try:
                    _json = json.loads(response.text)
                    if _json:
                        
                        list_total = int(_json['total'])
                        if list_total:
                            self._list_total = list_total

                        job_postings = _json.get('jobPostings',[])
                        if job_postings:
                            items.extend(job_postings)
                        else:
                            break
                except:
                    break

                if self._page == 0:
                    total_page = math.ceil(self._list_total / 20)
                    init_url = response.url

                if total_page <= current_page:
                    has_next = False

                current_page+=1
                self._page=current_page
                

        except:
            pass

        return {'result_items': items, 'url': init_url}

    def _transform_word_to_date(self, value):

        today = date.today()
        post_date = today.strftime("%d/%m/%Y")
        matches = re.search(r'(\d+)', value)
        if matches:
            days_ago = int(matches.group(1))
            dif_date = today - timedelta(days=days_ago)
            post_date = dif_date.strftime("%d/%m/%Y")

        return post_date

        