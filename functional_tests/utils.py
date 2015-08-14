# This class is intended to contain some utility
# functions for functional tests in one place
from pick10.models import *
from django.core.urlresolvers import reverse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Utils:

    def __init__(self,browser,server_url):
        self.browser = browser
        self.server_url = server_url

    def update_games_page(self,year,week_number):
        address = self.server_url + reverse('update_games',args=(year,week_number,))
        self.browser.get(address)

    def week_results_page(self,year,week_number):
        address = self.server_url + reverse('week_results',args=(year,week_number))
        self.browser.get(address)

    def overall_results_page(self,year):
        address = self.server_url + reverse('overall_results',args=(year,))
        self.browser.get(address)

    def player_results_page(self,year,week_number,player_id):
        address = self.server_url + reverse('player_results',args=(year,week_number,player_id))
        self.browser.get(address)

    def tiebreak_page(self,year,week):
        address = self.server_url + reverse('tiebreak',args=(year,week))
        self.browser.get(address)

    def wait_for_page(self,title,timeout=10):
        WebDriverWait(self.browser,timeout,1.0).until(EC.title_is(title))

    def login_unassigned_user(self,name='user1',password='1234'):
        self.create_user(name,password)
        self.login(name,password)

    def login_assigned_user(self,name='puser1',password='1234',player=None):
        return self.login_unassigned_user(name,password)

        # TODO need to implement after UserProfile is working
        user = self.create_user(name,password)
        user_profile = user.get_profile()
        user_profile.player = player
        user_profile.save()
        self.login(name,password)

    def login_superuser(self,name='suser1',password='1234'):
        self.create_superuser(name,password)
        self.login(name,password)

    def login(self,name,password):

        # go to login page
        address = self.server_url + reverse('auth_login')
        self.browser.get(address)

        # fill in user/password
        self.browser.find_element_by_id('id_username').send_keys(name)
        self.browser.find_element_by_id('id_password').send_keys(password)

        # click sign in button
        buttons = self.browser.find_elements_by_tag_name('button')
        for button in buttons:
            if button.text == 'Sign in':
                button.click()
                break

    def logout(self):
        raise AssertionError,"Need to implement"

    def create_user(self,name='user1',email='user1@abc.com',password='1234'):
        user = User.objects.create_user(name,email,password)
        return user

    def create_superuser(self,name='suser1',email='suser1@abc.com',password='1234'):
        user = User.objects.create_superuser(name,email,password)
        return user

    def click_button(self,button_text):
        buttons = self.browser.find_elements_by_tag_name('button')
        for button in buttons:
            if button.text == button_text:
                button.click()
                break

    def click_input_button(self,name):
        self.browser.find_element_by_name(name).click()
