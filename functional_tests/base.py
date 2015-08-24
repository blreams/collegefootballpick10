import sys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.conf import settings
from selenium import webdriver

class FunctionalTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super(FunctionalTest, cls).setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super(FunctionalTest, cls).tearDownClass()

    def setUp(self):
        if settings.SELENIUM_WEBDRIVER_STRING:
            if settings.SELENIUM_WEBDRIVER_STRING == 'firefox':
                self.browser = webdriver.Firefox()
            elif settings.SELENIUM_WEBDRIVER_STRING == 'phantomjs':
                self.browser = webdriver.PhantomJS()
        else:
            # This will be the default webdriver if not setup in settings via environment
            self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

