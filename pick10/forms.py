from django.contrib.auth.models import User
from django import forms
from models import UserProfile, get_yearlist, get_createweek_year_week, get_teamlist
from datetime import datetime

import pytz

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('company', 'preferredtz')

def year_choices():
    yearlist = get_yearlist()
    thisyear = datetime.now().year
    if thisyear not in yearlist:
        yearlist.append(thisyear)
    return tuple((i, i) for i in yearlist)

week_choices = tuple((i, i) for i in range(1, 14))
class CreateWeekForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CreateWeekForm, self).__init__(*args, **kwargs)
        (defaultyear, defaultweek) = get_createweek_year_week()
        self.initial['year'] = defaultyear
        self.initial['week'] = defaultweek
        self.fields['year'] = forms.ChoiceField(choices=year_choices())
        self.fields['week'] = forms.ChoiceField(choices=week_choices)

team_choices = tuple((t, t) for t in get_teamlist())
class EditWeekForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(EditWeekForm, self).__init__(*args, **kwargs)
        self.fields['game1_team1'] = forms.ChoiceField(choices=team_choices)
        self.fields['game1_team2'] = forms.ChoiceField(choices=team_choices)

