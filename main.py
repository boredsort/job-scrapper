
from connection import mongo_client
from factory import SpiderFactory

def execute():
    website = 'www.globe.com'
    # website = 'www.indivd.com'
    website = 'www.meldcx.com'
    # website = 'www.hov.co'
    factory = SpiderFactory()
    spider = factory.spawn_listSpider(website)()
    # url = 'https://www.globe.com'
    url = 'https://www.hov.co/careers'
    url = 'https://www.meldcx.com/careers'

    # url = 'https://www.meldcx.com/careers'
    # url = 'https://career.indivd.com/jobs'
    result = spider.crawl(url)
    mongo_client.save_scraped(result.convert_to_collection())
    print(result)

if __name__== "__main__":
    
    print('Initiliazing spider')
    execute()