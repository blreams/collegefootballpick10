from pick10.models import *
from pick10.database import *

# Assumes user is already authenticated

class UserAccess:

    def __init__(self,user):
        self.__determine_user_type(user)

    def is_public_user(self):
        return self.__user_type == 'public'

    def is_private_user(self):
        return self.__user_type == 'private'

    def is_superuser(self):
        return self.__is_superuser

    def get_player(self):
        return self.__player

    def is_player(self,player_id):
        return self.__player != None and self.__player.id == player_id

    def is_player_in_year(self,year):
        if self.__player == None:
            return False
        players_in_year = Database().load_players(year)
        return self.__player.id in players_in_year

    def get_profile(self):
        return self.__profile

    def __determine_user_type(self,user):
        self.__user_type = 'public'
        self.__profile = None
        self.__player = None
        self.__is_superuser = user.is_superuser

        try:
            profile = UserProfile.objects.get(user=user)
            self.__profile = profile
            if profile.player != None:
                self.__user_type = 'private'
                self.__player = profile.player
        except:
            return

