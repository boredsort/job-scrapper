from lib2to3.pytree import Base
from bs4 import BeautifulSoup

from ..base import BaseSpider
from ..constants import NOT_FOUND, EXTRACTION_FAILED
from items.list_job_item import ListJobItem


class GlobeComSpider(BaseSpider):

    pass
    # extract data here
    # https://globe.wd3.myworkdayjobs.com/wday/cxs/globe/GLB_Careers/jobs
    # use this as the body
    # {"appliedFacets":{},"limit":20,"offset":0,"searchText":""}