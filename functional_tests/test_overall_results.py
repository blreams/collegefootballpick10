from .base import FunctionalTest
from django.core.urlresolvers import reverse
from pick10.tests.unit_test_database import *
import unittest

class OverallResultsTest(FunctionalTest):

    def test_page_up(self):
        pass

    def test_bad_year(self):
        self.__open_results_page(year=1980)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Cannot find a pool for the year 1980',body)

    def __open_results_page(self,year):
        address = self.server_url + reverse('overall_results',args=(year,))
        self.browser.get(address)
