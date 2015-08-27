# This class is intended to contain some utility
# functions for functional tests in one place
from pick10.models import *
from pick10.database import *
from django.core.urlresolvers import reverse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime as dt

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
        address = self.server_url + reverse('tiebreak',args=(year,week,))
        self.browser.get(address)

    def enter_picks_page(self,year,week,player_id):
        address = self.server_url + reverse('enter_picks',args=(year,week,player_id,))
        self.browser.get(address)

    def update_page(self,year,week):
        address = self.server_url + reverse('update_pages',args=(year,week,))
        self.browser.get(address)

    def wait_for_page(self,title,timeout=10):
        WebDriverWait(self.browser,timeout,1.0).until(EC.title_is(title))

    def get_player_from_public_name(self,year,name):
        players = Database().load_players(year)
        for player_id in players:
            player = players[player_id]
            if player and player.public_name == name:
                return player
        raise AssertionError,"Could not find player %d" % (name)

    def get_player_from_private_name(self,year,name):
        players = Database().load_players(year)
        for player_id in players:
            player = players[player_id]
            if player and player.private_name == name:
                return player
        raise AssertionError,"Could not find player %d" % (name)

    def get_player_from_ss_name(self,year,name):
        players = Database().load_players(year)
        for player_id in players:
            player = players[player_id]
            if player and player.ss_name == name:
                return player
        raise AssertionError,"Could not find player %d" % (name)

    def login_unassigned_user(self,name='user1',password='1234'):
        self.create_user(name,password)
        self.login(name,password)

    def login_assigned_user(self,name='puser1',password='1234',player=None):
        user = self.create_user(name,password)
        assert player != None,'Create player not supported yet'
        user_profile = UserProfile.objects.create(user=user,player=player)
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

    def create_user_with_profile(self,name='user1',email='user1@abc.com',password='1234',player=None):
        user = self.create_user(name,email,password)
        user_profile = UserProfile.objects.create(user=user,player=player)
        return user,user_profile

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

    def click_radio_button(self,name,value):
        elements = self.browser.find_elements_by_name(name)
        for e in elements:
            if e.get_attribute('value') == value:
                e.click()
                return
        raise AssertionError,"Could not find radio button"

    def set_input_text(self,name,text):
        self.browser.find_element_by_name(name).clear()
        self.browser.find_element_by_name(name).send_keys(text)

    def set_pick_deadline_to_expired(self,year,week_number):
        week = get_week(year,week_number)
        naive_dt_now = dt.datetime.now()
        naive_dt_deadline = dt.datetime(naive_dt_now.year, naive_dt_now.month, naive_dt_now.day, 16, 0, 0) - timedelta(days=1)
        deadline = pytz.timezone('US/Eastern').localize(naive_dt_deadline)
        week.pick_deadline = deadline
        week.lock_picks = False
        week.save()

    def set_pick_deadline_not_expired(self,year,week_number,days_until_expired=1):
        week = get_week(year,week_number)
        naive_dt_now = dt.datetime.now()
        naive_dt_deadline = dt.datetime(naive_dt_now.year, naive_dt_now.month, naive_dt_now.day, 16, 0, 0) + timedelta(days=days_until_expired)
        deadline = pytz.timezone('US/Eastern').localize(naive_dt_deadline)
        week.pick_deadline = deadline
        week.lock_picks = False
        week.save()

    def lock_picks(self,year,week_number):
        week = get_week(year,week_number)
        week.lock_picks = True
        week.save()

    def unlock_picks(self,year,week_number):
        week = get_week(year,week_number)
        week.lock_picks = False
        week.save()

    def unlock_game_scores(self,year,week_number):
        week = get_week(year,week_number)
        week.lock_scores = False
        week.save()
