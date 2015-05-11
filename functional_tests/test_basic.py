from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class NewVisitorTest(FunctionalTest):
    def test_home_page_visit(self):
        # There is a cool new online football pool.
        # Check out its homepage (or landing page).
        self.browser.get(self.server_url)
        self.browser.maximize_window()   # Without this I get ElementNotVisibleException

        # Page title and h1 header indicate he is at the right place.
        self.assertIn('College Football Pick 10', self.browser.title)
        header_text = self.browser.find_element_by_id('base_id').text
        self.assertIn('College Football Pick 10', header_text)

        # There should be id="index_h1" element
        body_text = self.browser.find_element_by_id('index_h1').text
        self.assertIn('INDEX page', body_text)

        # He clicks Register to see if he can get in.
        register_link = self.browser.find_element_by_link_text('Register')
        register_link.click()
        WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.ID, 'user_form'))
            )

        # He fills in the form to register himself
        username_box = self.browser.find_element_by_name('username')
        email_box = self.browser.find_element_by_name('email')
        #fname_box = self.browser.find_element_by_name('first_name')
        #lname_box = self.browser.find_element_by_name('last_name')
        password1_box = self.browser.find_element_by_name('password1')
        password2_box = self.browser.find_element_by_name('password2')
        username_box.send_keys('johndoe')
        email_box.send_keys('john.doe@example.com')
        #fname_box.send_keys('John')
        #lname_box.send_keys('Doe')
        password1_box.send_keys('eodnhoj')
        password2_box.send_keys('eodnhoj')
        password2_box.submit()

        # He should be successfully registered and logged in.
        WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.ID, 'thanks_id'))
            )
        ident_text = self.browser.find_element_by_id('ident_id').text
        self.assertIn('johndoe', ident_text)

        # Now he clicks Logout and waits for the index page
        logout_link = self.browser.find_element_by_link_text('Logout')
        logout_link.click()
        WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.ID, 'index_h1'))
            )

        # Now he clicks Login
        login_link = self.browser.find_element_by_link_text('Login')
        login_link.click()
        WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.ID, 'login_form'))
            )
        
        # Try logging in with test user
        username_box = self.browser.find_element_by_name('username')
        password_box = self.browser.find_element_by_name('password')
        username_box.send_keys('johndoe')
        password_box.send_keys('eodnhoj')
        password_box.submit()

        # After successful login, should redirect to Home
        WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.ID, 'home_h1'))
            )
        body_text = self.browser.find_element_by_id('home_h1').text
        self.assertIn('HOME page', body_text)

        #self.browser.save_screenshot('aaa.png')
