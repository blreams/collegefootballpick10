from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import six

import pytz
import django.utils.timezone as tz
from django.core.exceptions import ObjectDoesNotExist
from .pick_data import PickData
from .database import Database
from .calculator import TEAM1, TEAM2
from .utils import get_timestamp
from .models import Player, Pick, UserProfile
from .models import add_pick, get_game

class EnterPicks:

    def __init__(self,year,week_number,player_id):
        self.year = year
        self.week_number = week_number
        self.player_id = player_id

    def get_game_picks(self):
        profile = UserProfile.objects.get(player__id=self.player_id)
        database = Database()
        week_data = database.load_week_data(self.year,self.week_number)

        player_already_picked = self.player_id in week_data.player_picks
        if player_already_picked:
            picks = { pick.game.gamenum:pick for pick in week_data.player_picks[self.player_id] }

        game_picks = []
        for game in week_data.games.values():
            data = PickData()
            data.number = game.gamenum
            data.team1 = game.team1.team_name
            data.team2 = game.team2.team_name
            data.favored = game.favored
            data.spread = game.spread
            data.kickoff = self.__format_kickoff(game.kickoff, profile.preferredtz)
            data.timestamp = get_timestamp(game.updated)

            if player_already_picked:
                data.pick = picks[game.gamenum].winner
            else:
                data.pick = 0

            if game.favored == TEAM1:
                data.team1_spread = game.spread * -1
                data.team2_spread = ""
            elif game.favored == TEAM2:
                data.team1_spread = ""
                data.team2_spread = game.spread * -1
            else:
                raise AssertionError("Invalid favored value")

            if game.gamenum == 10:
                if player_already_picked:
                    data.team1_predicted_points = picks[game.gamenum].team1_predicted_points
                    data.team2_predicted_points = picks[game.gamenum].team2_predicted_points
                else:
                    data.team1_predicted_points = ""
                    data.team2_predicted_points = ""

            game_picks.append(data)

        return sorted(game_picks,key=lambda pick:pick.number)

    def save_picks(self,picks):
        self.__picks_sanity_check(picks)

        player = Player.objects.get(id=self.player_id)

        update_submit_time = False

        for pick in picks:
            game_number = pick.number
            game = get_game(self.year,self.week_number,game_number)

            existing_pick = self.__get_existing_pick(player,game)

            if existing_pick != None:
                pick_changed = self.__edit_pick(game_number,existing_pick,pick)
                if pick_changed:
                    update_submit_time = True
            else:
                self.__create_pick(player,game,pick)
                update_submit_time = True

        if update_submit_time:
            self.__update_submit_time(player)

    def __picks_sanity_check(self,picks):
        assert len(picks) == 10

        # verify pick for each game number
        picks_by_game = { pick.number:pick for pick in picks }
        game_numbers = sorted(picks_by_game.keys())
        assert game_numbers == [1,2,3,4,5,6,7,8,9,10]

        # verify game 10 has a score entered
        game10 = picks_by_game[10]
        assert type(game10.team1_predicted_points) == int
        assert type(game10.team2_predicted_points) == int
        assert game10.team1_predicted_points >= 0
        assert game10.team2_predicted_points >= 0

        # verify each game has a pick of TEAM1 or TEAM2
        for game_pick in picks:
            assert type(game_pick.pick) == int
            assert game_pick.pick == 1 or game_pick.pick == 2 

    def __get_existing_pick(self,player,game):
        try:
            return Pick.objects.get(player=player,game=game)
        except ObjectDoesNotExist:
            return None

    def __edit_pick(self,game_number,pick_model,pick):
        change = False

        if pick_model.winner != pick.pick:
            pick_model.winner = pick.pick
            change = True

        if game_number == 10:
            if pick_model.team1_predicted_points != pick.team1_predicted_points:
                pick_model.team1_predicted_points = pick.team1_predicted_points
                change = True
            if pick_model.team2_predicted_points != pick.team2_predicted_points:
                pick_model.team2_predicted_points = pick.team2_predicted_points
                change = True

        if change:
            pick_model.save()

        return change

    def __create_pick(self,player,game,pick):
        if game.gamenum == 10:
            p = add_pick(player,game,pick.pick,pick.team1_predicted_points,pick.team2_predicted_points)
        else:
            p = add_pick(player,game,pick.pick)

    def __update_submit_time(self,player):
        game = get_game(self.year,self.week_number,10)
        pick = self.__get_existing_pick(player,game)
        pick.submit_time = tz.now()
        pick.save()

    def __get_local_time(self, tz_date, timezone_name):
        tz = pytz.timezone(timezone_name)
        return tz_date.astimezone(tz)

    def __format_kickoff(self, kickoff, timezone):
        kickoff_localtime = self.__get_local_time(kickoff, timezone)
        date_format = "%a %m/%d/%Y %I:%M %p %Z"
        return kickoff_localtime.strftime(date_format)

