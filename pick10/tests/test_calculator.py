from django.test import TestCase
from pick10.database import Database
from pick10.models import *
from unit_test_database import *

# This class tests the calculator.py file load_week_data function
class CalculatorTests(TestCase):

    def setUp(self):
        test_db = UnitTestDatabase()
        test_db.load_historical_data_for_year(2013)

    def test_blah(self):
        self.fail('Placeholder for tests')
