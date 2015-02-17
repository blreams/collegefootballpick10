from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NewVisitorTest(FunctionalTest):
    def test_home_page_visit(self):
        # There is a cool new online football pool.
        # Check out its homepage (or landing page).
        self.browser.get(self.server_url)

        # Page title and h1 header indicate he is at the right place.
        self.assertIn('College Football Pick 10', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('College Football Pick 10', header_text)

        # There should be a login button
        login_link = self.browser.find_element_by_link_text('Login')

        # Try clicking it, wait for logout button
        login_link.click()
        WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.LINK_TEXT, 'Logout'))
            )
        logout_link = self.browser.find_element_by_link_text('Logout')
        
        # Try clicking logout, wait for login button
        logout_link.click()
        WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.LINK_TEXT, 'Login'))
            )


        
