


import os
import json
import importlib


class SpiderFactory(object):

    WEBSITE_MAP = 'list_map.json'
    CAREER_LIST_DIR = 'career_list'

    def __init__(self):

        self.base_dir = os.getcwd()
        career_list_path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), 
                                                    'spiders', self.__class__.WEBSITE_MAP))
        try:
            with open(career_list_path, 'r') as map_file:
                self.career_spiders = json.load(map_file)
        except:
            raise Exception('Failed to map spiders')
    
    @staticmethod
    def _get_class_name(file_name):
        if not file_name:
            return None

        file_name = file_name.lower()
        splited_name = file_name.split('_')

        class_name = ''
        for word in splited_name:
            class_name += word.capitalize()

        return class_name

    def spawn_listSpider(self, website):
        try:
            website = website.lower()
            file_name = self.career_spiders[website]
            module_path = f'spiders.{self.__class__.CAREER_LIST_DIR}.{file_name}'
            module = importlib.import_module(module_path)
            class_name = f'{self._get_class_name(file_name)}ListSpider'
            return getattr(module, class_name)

        except KeyError:
            raise Exception('Failed to find spider')

        except:
            raise Exception('Unhandled Exception.')
