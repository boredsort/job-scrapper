import requests

from .abstract import AbstractSpider

class BaseSpider(AbstractSpider):

    def __init__(self, params={}):
        assert isinstance(params, dict)
        self.params = params
        self.website = None

    def parse(self, result: dict):
        return result

    def crawl(self, urls):
        try:
            headers = {
                'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'accept-encoding': 'gzip,deflate'
            }
            response = requests.get(urls, headers=headers)

            if response.status_code in [200, 201]:
                response.encoding = 'utf-8'
                result = { 
                    'raw': response.text,
                    'url': response.url
                }

                return result

        except requests.exceptions.HTTPError:
            pass

