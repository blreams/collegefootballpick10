from django.contrib.auth.models import User
from django import forms
from models import UserProfile, Team
from models import get_yearlist, get_createweek_year_week, get_teamlist, get_default_pick_deadline
from django.utils import timezone

import pytz

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')

def team_choices():
    teamlist = [(team.team_name, team.team_name) for team in Team.objects.all().order_by('team_name')]
    return tuple([('--------', '--------')] + teamlist)

class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['favorite_team'] = forms.ChoiceField(choices=team_choices())

    class Meta:
        model = UserProfile
        fields = ('company', 'preferredtz', 'favorite_team')

    def clean_favorite_team(self):
        team_name = self.cleaned_data['favorite_team']
        if team_name != '--------':
            valid_team_names = [team.team_name for team in Team.objects.all()]
            if team_name not in valid_team_names:
                raise forms.ValidationError("Your team is not in the database")
        else:
            team_name = ''
        return team_name

def year_choices():
    yearlist = get_yearlist()
    thisyear = timezone.now().year
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


class EditWeekSelForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(EditWeekSelForm, self).__init__(*args, **kwargs)
        (defaultyear, defaultweek) = get_createweek_year_week()
        self.initial['year'] = defaultyear
        self.initial['week'] = defaultweek
        self.fields['year'] = forms.ChoiceField(choices=year_choices())
        self.fields['week'] = forms.ChoiceField(choices=week_choices)


class EditWeekForm(forms.Form):
    def __init__(self, *args, **kwargs):
        weekfields = {}
        if 'weekfields' in kwargs:
            weekfields = kwargs.pop('weekfields')
        gamefields = {}
        if 'gamefields' in kwargs:
            gamefields = kwargs.pop('gamefields')
        super(EditWeekForm, self).__init__(*args, **kwargs)
        self.initial['pick_deadline'] = get_default_pick_deadline()
        self.initial['lock_picks'] = weekfields.get('lock_picks')
        self.fields['lock_picks'] = forms.ChoiceField(widget=forms.RadioSelect, choices=((True, 'Yes'), (False, 'No')))
        self.fields['pick_deadline'] = forms.DateTimeField(widget=forms.DateTimeInput)
        for i in range(1, 11):
            gamestr = 'game%d_' % i

            self.initial[gamestr + 'team1'] = gamefields.get(gamestr + 'team1')
            self.initial[gamestr + 'team2'] = gamefields.get(gamestr + 'team2')
            if gamefields.get(gamestr + 'favored') is not None:
                self.initial[gamestr + 'favored'] = 'Team%d' % gamefields[gamestr + 'favored']
            self.initial[gamestr + 'spread'] = gamefields.get(gamestr + 'spread')
            self.initial[gamestr + 'kickoff'] = gamefields.get(gamestr + 'kickoff')

            self.fields[gamestr + 'team1'] = forms.ChoiceField(choices=tuple((t, t) for t in get_teamlist()))
            self.fields[gamestr + 'team2'] = forms.ChoiceField(choices=tuple((t, t) for t in get_teamlist()))
            self.fields[gamestr + 'favored'] = forms.ChoiceField(widget=forms.RadioSelect, choices=tuple(('Team%d' % i, 'Team%d' % i) for i in range(1, 3)))
            self.fields[gamestr + 'spread'] = forms.DecimalField(decimal_places=1)
            self.fields[gamestr + 'kickoff'] = forms.DateTimeField(widget=forms.DateTimeInput, required=False)

    def clean(self):
        cleaned_data = super(EditWeekForm, self).clean()

        # This validates that all teams are unique
        teamset = set()
        duplicateteamset = set()
        numuniqueteams = 0
        for i in range(1, 11):
            gamestr = 'game%d_' % i
            teamset.add(cleaned_data[gamestr + 'team1'])
            if len(teamset) == numuniqueteams:
                duplicateteamset.add(cleaned_data[gamestr + 'team1'])
            numuniqueteams = len(teamset)
            teamset.add(cleaned_data[gamestr + 'team2'])
            if len(teamset) == numuniqueteams:
                duplicateteamset.add(cleaned_data[gamestr + 'team2'])
            numuniqueteams = len(teamset)


        # This validates spread
        for i in range(1, 11):
            gamestr = 'game%d_' % i
            spread = cleaned_data.get(gamestr + 'spread')
            if spread is not None:
                x = int(spread * 2)
                if x % 2 == 0:
                    msg = 'Game %d spread must be offset by 1/2 point (ie. 0.5, 1.5, etc.)' % i
                    self.add_error(gamestr + 'spread', msg)

        if duplicateteamset:
            raise forms.ValidationError(
                    'Duplicate teams found: %s.' % ','.join(duplicateteamset)
                    )

