import string

class FBPoolPlayerName:

    def __init__(self,method="no_change"):
        self.__method = method

    def get_name(self,player_name):
        if self.__method == "no_change":
            return player_name
        elif self.__method == "full_name_no_remote":
            return self.__fullname_no_remote(player_name)
        elif self.__method == "hide_lastname":
            return self.__extract_name_and_hide_lastname(player_name)

        raise AssertionError("Invalid method")

    def __fullname_no_remote(self,name):
        return string.replace(name,"Remote","").strip()

    def __extract_name_and_hide_lastname(self,name): 
        words = name.split(',') 
        assert len(words) == 2 
        last_name = words[0].strip() 
        first_name = self.__remove_remote_and_middle_name(words[1]).strip() 
        conflicting_names = self.__adjust_for_same_name(last_name) 
        if conflicting_names == None: 
            return "%s %s." % (first_name,last_name[0]) 
        else: 
            return conflicting_names 
 
    def __adjust_for_same_name(self,last_name): 
        if last_name == "Ferguson": 
            return "Scott Fe." 
        if last_name == "Freedman": 
            return "Scott Fr."
        return None

    def __remove_remote_and_middle_name(self,name):
        words = name.strip().split(' ')
        assert len(words) > 0
        return string.replace(words[0],"Remote","").strip()
