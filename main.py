
from connection import mongo_client
from factory import SpiderFactory

def execute():
    website = 'www.globe.com'
    factory = SpiderFactory()
    spider = factory.spawn_listSpider(website)()
    url = 'https://www.globe.com'
    # url = 'https://www.meldcx.com/careers'
    result = spider.crawl(url)
    mongo_client.save_scraped(result.convert_to_collection())
    print(result)

if __name__== "__main__":
    
    print('Initiliazing spider')
    execute()