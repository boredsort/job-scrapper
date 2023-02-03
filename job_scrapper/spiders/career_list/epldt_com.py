from bs4 import BeautifulSoup
import requests
import re
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import cloudscraper

from ..base import BaseSpider
from ..constants import NOT_FOUND, EXTRACTION_FAILED
from items.list_job_item import ListJobItem


class EpldtComListSpider(BaseSpider):

    def __init__(self, params={}):
        super().__init__(params)
        self.website = 'www.epldt.com'


    def crawl(self, urls):

        try:
            headers = {
                "Host": "www.epldt.com",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "DNT": "1",
                "Connection": "keep-alive",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "cross-site"
            }

            # session = requests.Session()
            # retry = Retry(connect=3, backoff_factor=0.5)
            # adapter = HTTPAdapter(max_retries=retry)
            # session.mount('http://', adapter)
            # session.mount('https://', adapter)

            # cookies = self.get_cookies()
            scraper = cloudscraper.create_scraper()

            response = scraper.get(urls, headers=headers)
            if response.status_code in [200, 201]:
                soup = BeautifulSoup(response.text, 'lxml')
                security = self.get_security_code(soup)

                items = self.get_all_items(security)

                if items:
                    return self.parse(items)
        except:
            pass

        return {}

    def get_cookies(self):
        url = 'https://www.epldt.com'

        response = requests.get(url)
        if response:
            pass

    def parse(self, result):

        return self.parse(result)


    def get_job_tags(self, soup):
        pass

    def get_title(self, soup):
        pass

    def get_url(self, soup):
        pass
    def get_security_code(self, soup):
        tag = soup.select_one('script:contains(var ajaxurl)')
        if tag:
            txt = tag.get_text().strip()
            matches = re.search(r"'security':\s?'([.*?])'", txt)
            if matches:
                return matches.group(1)
        return None


    def get_all_items(self, security):

        page = 1
        next = True
        items = []
        while(next):
            raw = self.get_data(security, page)
            if raw:
                soup = BeautifulSoup(raw, 'lxml')
                tags = self.get_job_tags(soup)
                items.extend(tags)
            else:
                next = False
            page+=1

    def get_data(self, security, page):

        url = 'https://www.epldt.com/wp-admin/admin-ajax.php'

        payload = f'action=load_jobs_by_ajax&page={page}&security={security}'

        try:
            headers = {
                "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0",
                "Accept":"*/*",
                "Accept-Language":"en-US,en;q=0.5",
                "Accept-Encoding":"gzip, deflate",
                "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With":"XMLHttpRequest",
                "Origin":"https://www.epldt.com",
                "DNT":1,
                "Connection":"keep-alive",
                "Referer":"https://www.epldt.com/careers/",
                "Sec-Fetch-Dest":"empty",
                "Sec-Fetch-Mode":"cors",
                "Sec-Fetch-Site":"same-origin",
                "TE":"trailers"
            }

            response = requests.post(url, headers=headers, data=payload)

            if response.status_code in [200, 201]:
                return response.text

        except:
            pass
        return None

        'https://www.epldt.com/careers/'