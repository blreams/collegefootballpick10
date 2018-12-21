from .base import FunctionalTest
from django.urls import reverse
from pick10.tests.unit_test_database import UnitTestDatabase
#from pick10.models import *
#from pick10.calculator import *
import unittest
from django.contrib.auth.models import User
from django.test.client import Client
from .utils import Utils
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CommissionerAccessTest(FunctionalTest):

    def setUp(self):
        super(CommissionerAccessTest, self).setUp()
        self.utils = Utils(self.browser,self.server_url)

    def test_commissioner_login(self):
        test_db = UnitTestDatabase()
        test_db.setup_week_not_started(1978,1)
        self.utils.login_superuser(name='Byron')
        self.__verify_superuser_logged_in(name='Byron')

    def __verify_superuser_logged_in(self,name):
        logged_in_text = self.browser.find_element_by_id('ident_id').text
        expected = 'Logged in as: %s' % (name)
        self.assertEquals(expected,logged_in_text)
        commish_menu = self.browser.find_element_by_link_text('Commish')
        commish_menu.click()
        WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.LINK_TEXT, 'Commissioner'))
            )
        self.assertEquals('Commissioner',self.browser.find_element_by_id('commissioner_id').text)

