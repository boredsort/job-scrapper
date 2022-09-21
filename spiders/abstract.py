from abc import ABCMeta, abstractmethod


class AbstractSpider(metaclass=ABCMeta):

    @abstractmethod
    def parse(self, result):
        raise NotImplementedError

    @abstractmethod
    def crawl(self, urls):
        raise NotImplementedError