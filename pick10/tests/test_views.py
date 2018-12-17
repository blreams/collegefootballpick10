from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape

from pick10.views import home
from pick10.models import Team

from unittest import skip

class HomeViewTest(TestCase):
    def test_home_view_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'pick10/home.html')

