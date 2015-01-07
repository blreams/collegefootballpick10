from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(FunctionalTest):
    def test_home_page_visit(self):
        # Byron has heard about a cool new online football pool.
        # Check out its homepage.
        self.browser.get(self.server_url)

        # Page title and h1 header indicate he is at the right place.
        self.assertIn('College Football Pick 10', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('College Football Pick 10', header_text)
        
