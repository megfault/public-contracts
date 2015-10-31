import os
import shutil
from django.core import management

import django.test

import requests
import requests.exceptions

from contracts.crawler import EntitiesCrawler, ContractsCrawler, TendersCrawler


def _has_remote_access():
    try:
        response = requests.get('http://www.base.gov.pt', timeout=1)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False
    except requests.exceptions.ReadTimeout:
        return False

HAS_REMOTE_ACCESS = _has_remote_access()


class CrawlerTestCase(django.test.TestCase):
    """
    Changes the directory of the crawlers to '_data' and creates the directory
    in the setUp, and erases the directory in tearDown.
    """
    @classmethod
    def setUpClass(cls):
        if os.path.exists('_data'):
            shutil.rmtree('_data')
        os.makedirs('_data')

        for klass in [EntitiesCrawler, ContractsCrawler, TendersCrawler]:
            klass.object_directory = '_data'

        super(CrawlerTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(CrawlerTestCase, cls).tearDownClass()
        shutil.rmtree('_data')

        for klass in [EntitiesCrawler, ContractsCrawler, TendersCrawler]:
            klass.object_directory = 'data'

    @staticmethod
    def create_static_fixture():
        management.call_command('populate_contracts', static=True)

    @staticmethod
    def add_contracts(*args):
        c = ContractsCrawler()
        for base_id in args:
            c.update_instance(base_id)

    @staticmethod
    def add_tenders(*args):
        c = TendersCrawler()
        for base_id in args:
            c.update_instance(base_id)
