import os as _os
import re

import unittest
from pool_spreadsheet import *

# Create a player translation dict
player_username = {}
player_username['Aaron, Chip'] = 'aaron_chip'
player_username['Acevedo, Alfonso'] = 'acevedo_alfonso'
player_username['Adams, Daniel O'] = 'adams_daniel'
player_username['Allen, Landon Remote'] = 'allen_landon'
player_username['Barker, Christopher A'] = 'barker_christopher'
player_username['Barnes, Ike K'] = 'barnes_ike'
player_username['Batchler, Wayne'] = 'batchler_wayne'
player_username['Beasley, Tate'] = 'beasley_tate'
player_username['Beckwith, Greg'] = 'beckwith_greg'
player_username['Berger, Matthew A'] = 'berger_matthew'
player_username['Bisbee, Curt'] = 'bisbee_curt'
player_username['Blackmon, Vaughn'] = 'blackmon_vaughn'
player_username['Bowers, Martin L'] = 'bowers_martin'
player_username['Boyce, Jonathan E'] = 'boyce_jonathan'
player_username['Boykin, Jerome W'] = 'boykin_jerome'
player_username['Brokaw, Brantley A'] = 'brokaw_brantley'
player_username['Brunt, DavidRemote'] = 'brunt_david'
player_username['Carter, Chris'] = 'carter_chris'
player_username['Chan, Simon'] = 'chan_simon'
player_username['Christiansen, Amos H'] = 'christiansen_amos'
player_username['Clark, William J'] = 'clark_william'
player_username['Cochcroft, Art'] = 'cochcroft_art'
player_username['Cogan, TimothyX J'] = 'cogan_timothy'
player_username['Cook, Andrew S'] = 'cook_andrew'
player_username['Corley, Ernie'] = 'corley_ernie'
player_username['Crenshaw, Ed'] = 'crenshaw_ed'
player_username['Desetto, Daniel'] = 'desetto_daniel'
player_username['Desing, Scott M'] = 'desing_scott'
player_username['Deuell, Russell A'] = 'deuell_russell'
player_username['Duzan, Steve'] = 'duzan_steve'
player_username['Edwards, Christopher S'] = 'edwards_christoper'
player_username['Emptage, Nick'] = 'emptage_nick'
player_username['Estrada, Carlos A'] = 'estradia_carlos'
player_username['Eusebio, Ariel B'] = 'eusebio_ariel'
player_username['Farren, Kevin M'] = 'farren_kevin'
player_username['Farren, Leslie Remote'] = 'farren_leslie'
player_username['Ferguson, Scott Remote'] = 'ferguson_scott'
player_username['Fonville, Chris'] = 'fonville_chris'
player_username['Fonville, Stephanie Remote'] = 'fonville_stephanie'
player_username['Freedman, Scott Remote'] = 'freedman_scott'
player_username['Gibson, Johnny J'] = 'gibson_johnny'
player_username['Gilmer, Justin T'] = 'gilmer_justin'
player_username['Gindlesperger, Jeffrey C'] = 'gindlesperger_jeffrey'
player_username['Gore, Brandon'] = 'gore_brandon'
player_username['Gregory, Adam J'] = 'gregory_adam'
player_username['Gupta, Ashish O'] = 'gupta_ashish'
player_username['Havens, Ryan C'] = 'havens_ryan'
player_username['Hawk, Robert W'] = 'hawk_robert'
player_username['Hendrick, Matt R'] = 'hendrick_matt'
player_username['Holden, Brent'] = 'holden_brent'
player_username['Holley, Jeremy Remote'] = 'holley_jeremy'
player_username['Howell, David P'] = 'howell_david'
player_username['Hucks, Jason'] = 'hucks_jason'
player_username['Inabinet, Greg'] = 'inabinet_greg'
player_username['James, Larry C'] = 'james_larry'
player_username['Johnson, Robert J'] = 'johnson_robert'
player_username['Kandela, Marwan'] = 'kandela_marwan'
player_username['Kieselhorst, Larry'] = 'kieselhorst_larry'
player_username['Knopf, Greg D'] = 'knopf_greg'
player_username['Knotts, Brian'] = 'knotts_brian'
player_username['Krooswyk, Steven K'] = 'krooswyk_steven'
player_username['Locklear, Dave Remote'] = 'locklear_dave'
player_username['Lovelace, Van'] = 'lovelace_van'
player_username['Luck, Justin'] = 'luck_justin'
player_username['Marsh, Alexander Remote'] = 'marsh_alexander'
player_username['Martin, Douglas C'] = 'martin_douglas'
player_username['McGee, Steve'] = 'mcgee_steve'
player_username['McMahon, Pat'] = 'mcmahon_pat'
player_username['McTeer, Libby'] = 'mcteer_libby'
player_username['Mccall, Sean'] = 'mccall_sean'
player_username['Mccoy, William M'] = 'mccoy_william'
player_username['Mellitz, Elisha B'] = 'mellitz_elisha'
player_username['Miller, James'] = 'miller_james'
player_username['Miller, Robert J'] = 'miller_robert'
player_username['Moore, Kevin B'] = 'moore_kevin'
player_username['Moxley, Dave'] = 'moxley_dave'
player_username['Murphy, William A'] = 'murphy_william'
player_username['Nagorniak, Kristen M'] = 'nagorniak_kristen'
player_username['Nance, Rob'] = 'nance_rob'
player_username['Neeley, Amber Remote'] = 'neeley_amber'
player_username['Neeley, Michael'] = 'neeley_michael'
player_username['Neill, Charles H'] = 'neill_charles'
player_username['Nguyen, Thai'] = 'nguyen_thai'
player_username['Nye, Mike'] = 'nye_mike'
player_username['Parcenka, ThomasX'] = 'parcenka_thomas'
player_username['Parris, Brian W'] = 'parris_brian'
player_username['Patterson, Kevin R'] = 'patterson_kevin'
player_username['Peng, Aaron'] = 'peng_aaron'
player_username['Penrose, Tim Remote'] = 'penrose_tim'
player_username['Powell, LaMar'] = 'powell_lamar'
player_username['Puga, Moises'] = 'puga_moises'
player_username['Pytel, Steven G'] = 'pytel_steven'
player_username['Reams, Byron L'] = 'reams_byron'
player_username['Redalen, Andy'] = 'redalen_andy'
player_username['Redys, Brittany'] = 'redys_brittany'
player_username['Redys, David Remote'] = 'redys_david'
player_username['Reiland, Doug'] = 'reiland_doug'
player_username['Reiland, Will Remote'] = 'reiland_will'
player_username['Robbins, Dale'] = 'robbins_dale'
player_username['Robbins, Thomas D'] = 'robbins_thomas'
player_username['Ruffin, Chris'] = 'ruffin_chris'
player_username['Sams, David'] = 'sams_david'
player_username['Sapp, Carl G'] = 'sapp_carl'
player_username['Schelling, Todd'] = 'schelling_todd'
player_username['Scrivener, Bo'] = 'scrivener_bo'
player_username['Shuey, Jeffrey M'] = 'shuey_jeffrey'
player_username['Smoak, Wilson'] = 'smoak_wilson'
player_username['Staub, Kevin'] = 'staub_kevin'
player_username['Steel, Van Remote'] = 'steel_van'
player_username['Steele, David L'] = 'steele_david'
player_username['Stonecypher, David'] = 'stonecypher_david'
player_username['Straw, Adam D'] = 'straw_adam'
player_username['Strom, Brooker'] = 'strom_brooker'
player_username['Taylor, Adam'] = 'taylor_adam'
player_username['Teasdell, Brian K'] = 'teasdell_brian'
player_username['Tunnell, Justin S'] = 'tunnell_justin'
player_username['Tyson, Ben'] = 'tyson_ben'
player_username['Vang, Tong'] = 'vang_tong'
player_username['Vo, Henry'] = 'vo_henry'
player_username['Warren, Todd Remote'] = 'warren_todd'
player_username['Wells, Jennifer'] = 'wells_jennifer'
player_username['Wells, Seth Remote'] = 'wells_seth'
player_username['White, Jarred'] = 'white_jarred'
player_username['Wiant, Timothy J'] = 'wiant_timothy'
player_username['Willingham, JosephX'] = 'willingham_joseph'
player_username['Winburn, Steve A'] = 'winburn_steve'
player_username['Young, Derick'] = 'young_derick'
player_username['Young, Kenneth'] = 'young_kenneth'

correct_team_names = [
    'Air Force',
    'Alabama',
    'Appalachian State',
    'Arizona',
    'Arizona State',
    'Arkansas',
    'Army',
    'Auburn',
    'BYU',
    'Ball State',
    'Baylor',
    'Boise State',
    'Boston College',
    'Bowling Green',
    'Brigham Young',
    'Buffalo',
    'California',
    'Central Michigan',
    'Cincinnati',
    'Clemson',
    'Colorado',
    'Colorado State',
    'Connecticut',
    'Duke',
    'East Carolina',
    'Florida',
    'Florida State',
    'Fresno State',
    'Georgia',
    'Georgia Tech',
    'Hawaii',
    'Houston',
    'Illinois',
    'Indiana',
    'Iowa',
    'Iowa State',
    'Kansas',
    'Kansas State',
    'Kentucky',
    'LSU',
    'Louisiana Lafayette',
    'Louisiana Monroe',
    'Louisiana State',
    'Louisiana Tech',
    'Louisville',
    'Marshall',
    'Maryland',
    'Memphis',
    'Miami-Florida',
    'Miami-Ohio',
    'Michigan',
    'Michigan State',
    'Minnesota',
    'Mississippi',
    'Mississippi State',
    'Missouri',
    'NC State',
    'Navy',
    'Nebraska',
    'Nevada',
    'New Mexico',
    'New Mexico State',
    'North Carolina',
    'North Carolina State',
    'Northern Illinois',
    'Northwestern',
    'Notre Dame',
    'Ohio',
    'Ohio State',
    'Oklahoma',
    'Oklahoma State',
    'Oregon',
    'Oregon State',
    'Penn State',
    'Pittsburgh',
    'Purdue',
    'Rutgers',
    'San Diego State',
    'South Carolina',
    'South Florida',
    'Southern Cal',
    'Southern Methodist',
    'Southern Miss',
    'Stanford',
    'Syracuse',
    'TCU',
    'Temple',
    'Tennessee',
    'Texas',
    'Texas A&M',
    'Texas Tech',
    'Troy',
    'Tulane',
    'UAB',
    'UCF',
    'UCLA',
    'UNLV',
    'Utah',
    'Utah State',
    'Vanderbilt',
    'Virginia',
    'Virginia Tech',
    'Wake Forest',
    'Washington',
    'Washington State',
    'West Virginia',
    'Wisconsin',
    'Wyoming',
        ]

class TestSpreadsheet(unittest.TestCase):


    def test_get_week_numbers(self):
        spreadsheet = PoolSpreadsheet(2013)
        self.assertEquals(sorted(spreadsheet.get_week_numbers()),[1,2,3,4,5,6,7,8,9,10,11,12,13])

    def test_get_pool_winner(self):
        spreadsheet = PoolSpreadsheet(2013)
        self.assertEquals(sorted(spreadsheet.get_pool_winner()),["Neeley, Michael"])

    def test_get_players(self):
        spreadsheet = PoolSpreadsheet(2013)
        players = spreadsheet.get_players()
        self.assertEquals(len(players),55)
        self.__michael_player_info_correct(players['Neeley, Michael'])
        self.__brent_player_info_correct(players['Holden, Brent'])
        self.__rob_player_info_correct(players['Nance, Rob'])

    def test_get_player_info(self):
        spreadsheet = PoolSpreadsheet(2013)
        michael = spreadsheet.get_player_info("Neeley, Michael")
        brent = spreadsheet.get_player_info("Holden, Brent")
        rob = spreadsheet.get_player_info("Nance, Rob")
        self.__michael_player_info_correct(michael)
        self.__brent_player_info_correct(brent)
        self.__rob_player_info_correct(rob)

    def test_get_player_names(self):
        self.maxDiff = None
        spreadsheet = PoolSpreadsheet(2013)
        names = spreadsheet.get_player_names()
        names.sort()
        self.assertEquals(self.__get_2013_player_names(),names)

    def test_get_player_overall_rank(self):
        spreadsheet = PoolSpreadsheet(2013)
        self.assertEquals(1,spreadsheet.get_player_overall_rank("Neeley, Michael"))
        self.assertEquals(4,spreadsheet.get_player_overall_rank("Sams, David"))
        self.assertEquals(37,spreadsheet.get_player_overall_rank("Straw, Adam D"))
        self.assertEquals(55,spreadsheet.get_player_overall_rank("Nance, Rob"))

    def test_get_player_overall_points(self):
        spreadsheet = PoolSpreadsheet(2013)
        self.assertEquals(75,spreadsheet.get_player_overall_points("Neeley, Michael"))
        self.assertEquals(72,spreadsheet.get_player_overall_points("Sams, David"))
        self.assertEquals(61,spreadsheet.get_player_overall_points("Straw, Adam D"))
        self.assertEquals(31,spreadsheet.get_player_overall_points("Nance, Rob"))

    def test_get_player_week_points(self):
        spreadsheet = PoolSpreadsheet(2013)
        self.assertEquals(5,spreadsheet.get_player_week_points("Neeley, Michael",1))
        self.assertEquals(4,spreadsheet.get_player_week_points("Neeley, Michael",2))
        self.assertEquals(7,spreadsheet.get_player_week_points("Neeley, Michael",3))
        self.assertEquals(6,spreadsheet.get_player_week_points("Neeley, Michael",4))
        self.assertEquals(6,spreadsheet.get_player_week_points("Neeley, Michael",5))
        self.assertEquals(3,spreadsheet.get_player_week_points("Neeley, Michael",6))
        self.assertEquals(8,spreadsheet.get_player_week_points("Neeley, Michael",7))
        self.assertEquals(3,spreadsheet.get_player_week_points("Neeley, Michael",8))
        self.assertEquals(6,spreadsheet.get_player_week_points("Neeley, Michael",9))
        self.assertEquals(7,spreadsheet.get_player_week_points("Neeley, Michael",10))
        self.assertEquals(5,spreadsheet.get_player_week_points("Neeley, Michael",11))
        self.assertEquals(8,spreadsheet.get_player_week_points("Neeley, Michael",12))
        self.assertEquals(7,spreadsheet.get_player_week_points("Neeley, Michael",13))
        self.assertEquals(5,spreadsheet.get_player_week_points("Holden, Brent",1))
        self.assertEquals(4,spreadsheet.get_player_week_points("Holden, Brent",2))
        self.assertEquals(6,spreadsheet.get_player_week_points("Holden, Brent",3))
        self.assertEquals(6,spreadsheet.get_player_week_points("Holden, Brent",4))
        self.assertEquals(6,spreadsheet.get_player_week_points("Holden, Brent",5))
        self.assertEquals(5,spreadsheet.get_player_week_points("Holden, Brent",6))
        self.assertEquals(5,spreadsheet.get_player_week_points("Holden, Brent",7))
        self.assertEquals(3,spreadsheet.get_player_week_points("Holden, Brent",8))
        self.assertEquals(8,spreadsheet.get_player_week_points("Holden, Brent",9))
        self.assertEquals(2,spreadsheet.get_player_week_points("Holden, Brent",10))
        self.assertEquals(6,spreadsheet.get_player_week_points("Holden, Brent",11))
        self.assertEquals(3,spreadsheet.get_player_week_points("Holden, Brent",12))
        self.assertEquals(6,spreadsheet.get_player_week_points("Holden, Brent",13))

    def test_get_games(self):
        spreadsheet = PoolSpreadsheet(2013)
        for week_number in range(1,14):
            self.assertEquals(len(spreadsheet.get_games(week_number=week_number)),10)
        week1 = spreadsheet.get_games(week_number=1)
        self.__verify_week1_game_1(week1[1])
        self.__verify_week1_game_2(week1[2])
        self.__verify_week1_game_3(week1[3])
        self.__verify_week1_game_4(week1[4])
        self.__verify_week1_game_5(week1[5])
        self.__verify_week1_game_6(week1[6])
        self.__verify_week1_game_7(week1[7])
        self.__verify_week1_game_8(week1[8])
        self.__verify_week1_game_9(week1[9])
        self.__verify_week1_game_10(week1[10])

    def test_get_picks(self):
        spreadsheet = PoolSpreadsheet(2013)
        for week_number in range(1,14):
            self.assertEquals(len(spreadsheet.get_picks(week_number=week_number)),550)
        picks = spreadsheet.get_picks(week_number=1)
        self.__verify_brent_picks_week1(picks)
        self.__verify_carl_picks_week1(picks)

    def test_get_game_info(self):
        spreadsheet = PoolSpreadsheet(2013)
        self.__verify_week1_game_1(spreadsheet.get_game_info(week_number=1,game_number=1))
        self.__verify_week1_game_2(spreadsheet.get_game_info(week_number=1,game_number=2))
        self.__verify_week1_game_3(spreadsheet.get_game_info(week_number=1,game_number=3))
        self.__verify_week1_game_4(spreadsheet.get_game_info(week_number=1,game_number=4))
        self.__verify_week1_game_5(spreadsheet.get_game_info(week_number=1,game_number=5))
        self.__verify_week1_game_6(spreadsheet.get_game_info(week_number=1,game_number=6))
        self.__verify_week1_game_7(spreadsheet.get_game_info(week_number=1,game_number=7))
        self.__verify_week1_game_8(spreadsheet.get_game_info(week_number=1,game_number=8))
        self.__verify_week1_game_9(spreadsheet.get_game_info(week_number=1,game_number=9))
        self.__verify_week1_game_10(spreadsheet.get_game_info(week_number=1,game_number=10))

    def test_get_game_teams(self):
        spreadsheet = PoolSpreadsheet(2013)
        self.assertEquals(sorted(spreadsheet.get_game_teams(week_number=1,game_number=2)),["Utah","Utah State"])
        self.assertEquals(sorted(spreadsheet.get_game_teams(week_number=3,game_number=4)),["Duke","Georgia Tech"])
        self.assertEquals(sorted(spreadsheet.get_game_teams(week_number=13,game_number=10)),["Alabama","Auburn"])

    def test_get_game_team1(self):
        spreadsheet = PoolSpreadsheet(2013)
        self.assertEquals(spreadsheet.get_game_team1(week_number=6,game_number=7),"Washington")
        self.assertEquals(spreadsheet.get_game_team1(week_number=8,game_number=6),"TCU")
        self.assertEquals(spreadsheet.get_game_team1(week_number=2,game_number=3),"Florida")

    def test_get_game_team2(self):
        spreadsheet = PoolSpreadsheet(2013)
        self.assertEquals(spreadsheet.get_game_team2(week_number=3,game_number=3),"Nebraska")
        self.assertEquals(spreadsheet.get_game_team2(week_number=5,game_number=9),"Alabama")
        self.assertEquals(spreadsheet.get_game_team2(week_number=1,game_number=1),"South Carolina")

    def test_get_game_spread(self):
        spreadsheet = PoolSpreadsheet(2013)
        self.assertEquals(spreadsheet.get_game_spread(week_number=7,game_number=8),5.5)
        self.assertEquals(spreadsheet.get_game_spread(week_number=7,game_number=6),7.5)
        self.assertEquals(spreadsheet.get_game_spread(week_number=2,game_number=10),3.5)

    def test_get_game_favored_team(self):
        spreadsheet = PoolSpreadsheet(2013)
        self.assertEquals(spreadsheet.get_game_favored_team(week_number=2,game_number=3),"team1")
        self.assertEquals(spreadsheet.get_game_favored_team(week_number=1,game_number=10),"team1")
        self.assertEquals(spreadsheet.get_game_favored_team(week_number=3,game_number=7),"team2")

    def test_get_game_team1_score(self):
        spreadsheet = PoolSpreadsheet(2013)
        self.assertEquals(spreadsheet.get_game_team1_score(week_number=3,game_number=4),38)
        self.assertEquals(spreadsheet.get_game_team1_score(week_number=2,game_number=8),28)
        self.assertEquals(spreadsheet.get_game_team1_score(week_number=2,game_number=10),30)

    def test_get_game_team2_score(self):
        spreadsheet = PoolSpreadsheet(2013)
        self.assertEquals(spreadsheet.get_game_team2_score(week_number=2,game_number=6),35)
        self.assertEquals(spreadsheet.get_game_team2_score(week_number=3,game_number=2),13)
        self.assertEquals(spreadsheet.get_game_team2_score(week_number=5,game_number=1),10)

    def test_get_game_winner(self):
        spreadsheet = PoolSpreadsheet(2013)
        self.assertEquals(spreadsheet.get_game_winner(week_number=5,game_number=5),"team2")
        self.assertEquals(spreadsheet.get_game_winner(week_number=7,game_number=1),"team1")
        self.assertEquals(spreadsheet.get_game_winner(week_number=8,game_number=10),"team1")

    def test_get_player_pick(self):
        spreadsheet = PoolSpreadsheet(2013)
        self.assertEquals(spreadsheet.get_player_pick("Edwards, Christopher S",week_number=8,game_number=1),"team1")
        self.assertEquals(spreadsheet.get_player_pick("Edwards, Christopher S",week_number=8,game_number=2),"team1")
        self.assertEquals(spreadsheet.get_player_pick("Edwards, Christopher S",week_number=8,game_number=3),"team1")
        self.assertEquals(spreadsheet.get_player_pick("Edwards, Christopher S",week_number=8,game_number=4),"team2")
        self.assertEquals(spreadsheet.get_player_pick("Edwards, Christopher S",week_number=8,game_number=5),"team1")
        self.assertEquals(spreadsheet.get_player_pick("Edwards, Christopher S",week_number=8,game_number=6),"team1")
        self.assertEquals(spreadsheet.get_player_pick("Edwards, Christopher S",week_number=8,game_number=7),"team2")
        self.assertEquals(spreadsheet.get_player_pick("Edwards, Christopher S",week_number=8,game_number=8),"team1")
        self.assertEquals(spreadsheet.get_player_pick("Edwards, Christopher S",week_number=8,game_number=9),"team2")
        self.assertEquals(spreadsheet.get_player_pick("Edwards, Christopher S",week_number=8,game_number=10),"team2")
        self.assertEquals(spreadsheet.get_player_pick("Holden, Brent",week_number=8,game_number=1),"team1")
        self.assertEquals(spreadsheet.get_player_pick("Holden, Brent",week_number=8,game_number=2),"team2")
        self.assertEquals(spreadsheet.get_player_pick("Holden, Brent",week_number=8,game_number=3),"team1")
        self.assertEquals(spreadsheet.get_player_pick("Holden, Brent",week_number=8,game_number=4),"team1")
        self.assertEquals(spreadsheet.get_player_pick("Holden, Brent",week_number=8,game_number=5),"team1")
        self.assertEquals(spreadsheet.get_player_pick("Holden, Brent",week_number=8,game_number=6),"team2")
        self.assertEquals(spreadsheet.get_player_pick("Holden, Brent",week_number=8,game_number=7),"team2")
        self.assertEquals(spreadsheet.get_player_pick("Holden, Brent",week_number=8,game_number=8),"team1")
        self.assertEquals(spreadsheet.get_player_pick("Holden, Brent",week_number=8,game_number=9),"team1")
        self.assertEquals(spreadsheet.get_player_pick("Holden, Brent",week_number=8,game_number=10),"team2")

    def test_get_player_picks(self):
        spreadsheet = PoolSpreadsheet(2013)

        brent_picks = { 1:"team2", 2:"team2", 3:"team1", 4:"team1", 5:"team1", 6:"team1", 7:"team2", 8:"team2", 9:"team1", 10:"team2" }
        self.assertEquals(spreadsheet.get_player_picks("Holden, Brent",week_number=1),brent_picks)

        byron_picks = { 1:"team1", 2:"team1", 3:"team1", 4:"team1", 5:"team1", 6:"team2", 7:"team1", 8:"team1", 9:"team2", 10:"team1" }
        self.assertEquals(spreadsheet.get_player_picks("Reams, Byron L",week_number=13),byron_picks)

        rob_picks = { 1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None, 8:None, 9:None, 10:None }
        self.assertEquals(spreadsheet.get_player_picks("Nance, Rob",week_number=8),rob_picks)

    def test_get_player_points(self):
        spreadsheet = PoolSpreadsheet(2013)
        self.assertEquals(spreadsheet.get_player_points("Ruffin, Chris",week_number=8),6)
        self.assertEquals(spreadsheet.get_player_points("Wells, Seth Remote",week_number=9),8)
        self.assertEquals(spreadsheet.get_player_points("Gore, Brandon",week_number=8),0)
        # default:  not sure how to treat, spreadsheet has value 2, but is a default, so should be 0?
        # using 0 may cause overall points to be off, read the value directly?
        self.assertEquals(spreadsheet.get_player_points("Ruffin, Chris",week_number=13),0)

    def test_did_player_win_game(self):
        spreadsheet = PoolSpreadsheet(2013)
        self.assertEquals(spreadsheet.did_player_win_game("Neeley, Amber Remote",week_number=8,game_number=4),False)
        self.assertEquals(spreadsheet.did_player_win_game("Bowers, Martin L",week_number=11,game_number=1),False)
        self.assertEquals(spreadsheet.did_player_win_game("Desetto, Daniel",week_number=7,game_number=10),False)
        self.assertEquals(spreadsheet.did_player_win_game("Gore, Brandon",week_number=7,game_number=10),True)
        # default:  won 1 game as filled in by commish, return True or False?
        self.assertEquals(spreadsheet.did_player_win_game("Clark, William J",week_number=7,game_number=8),False)

    def test_did_player_lose_game(self):
        spreadsheet = PoolSpreadsheet(2013)
        self.assertEquals(spreadsheet.did_player_lose_game("Neeley, Amber Remote",week_number=8,game_number=4),True)
        self.assertEquals(spreadsheet.did_player_lose_game("Bowers, Martin L",week_number=11,game_number=1),True)
        self.assertEquals(spreadsheet.did_player_lose_game("Desetto, Daniel",week_number=7,game_number=10),True)
        self.assertEquals(spreadsheet.did_player_lose_game("Gore, Brandon",week_number=7,game_number=10),False)
        # default:  won 1 game as filled in by commish, return True or False?
        self.assertEquals(spreadsheet.did_player_lose_game("Clark, William J",week_number=7,game_number=8),True)

    def test_did_player_default(self):
        spreadsheet = PoolSpreadsheet(2013)
        self.assertEquals(spreadsheet.did_player_default("Allen, Landon Remote",week_number=11),True)
        self.assertEquals(spreadsheet.did_player_default("Inabinet, Greg",week_number=11),False)
        self.assertEquals(spreadsheet.did_player_default("Aaron, Chip",week_number=13),False)
        self.assertEquals(spreadsheet.did_player_default("Allen, Landon Remote",week_number=13),True)

    def test_get_players_that_defaulted(self):
        spreadsheet = PoolSpreadsheet(2013)
        defaulters = self.__get_2013_defaulters_per_week()
        for week_number in defaulters:
            self.assertEquals(sorted(spreadsheet.get_players_that_defaulted(week_number=week_number)),defaulters[week_number])

    def test_get_players_that_defaulted_any_week(self):
        spreadsheet = PoolSpreadsheet(2013)
        defaulters = self.__get_2013_defaulters()
        self.assertEquals(sorted(spreadsheet.get_players_that_defaulted_any_week()),sorted(defaulters))

    def test_get_player_tiebreak_score(self):
        spreadsheet = PoolSpreadsheet(2013)
        self.assertEquals(spreadsheet.get_player_tiebreak_score("Moore, Kevin B",week_number=3),{'team1':21,'team2':24})
        self.assertEquals(spreadsheet.get_player_tiebreak_score("Reams, Byron L",week_number=12),{'team1':23,'team2':20})
        self.assertEquals(spreadsheet.get_player_tiebreak_score("Redys, David Remote",week_number=11),{'team1':None,'team2':None})
        # week 2 Redys, David Remote team2 score missing, team1 score present
        self.assertEquals(spreadsheet.get_player_tiebreak_score("Redys, David Remote",week_number=2),{'team1':35,'team2':0})

    def test_get_week_winner(self):
        spreadsheet = PoolSpreadsheet(2013)
        self.assertEquals(spreadsheet.get_week_winner(week_number=1),"Murphy, William A")
        self.assertEquals(spreadsheet.get_week_winner(week_number=2),"Hendrick, Matt R")
        self.assertEquals(spreadsheet.get_week_winner(week_number=3),"Steel, Van Remote")
        self.assertEquals(spreadsheet.get_week_winner(week_number=4),"Shuey, Jeffrey M")
        self.assertEquals(spreadsheet.get_week_winner(week_number=5),"Nguyen, Thai")
        self.assertEquals(spreadsheet.get_week_winner(week_number=6),"Nguyen, Thai")
        self.assertEquals(spreadsheet.get_week_winner(week_number=7),"Locklear, Dave Remote")
        self.assertEquals(spreadsheet.get_week_winner(week_number=8),"Hendrick, Matt R")
        self.assertEquals(spreadsheet.get_week_winner(week_number=9),"Wells, Seth Remote")
        self.assertEquals(spreadsheet.get_week_winner(week_number=10),"Robbins, Dale")
        self.assertEquals(spreadsheet.get_week_winner(week_number=11),"Edwards, Christopher S")
        self.assertEquals(spreadsheet.get_week_winner(week_number=12),"Farren, Kevin M")
        self.assertEquals(spreadsheet.get_week_winner(week_number=13),"Chan, Simon")

    def test_get_teams(self):
        spreadsheet = PoolSpreadsheet(2013)
        teams = spreadsheet.get_teams()
        self.assertEquals(len(teams),126)
        self.assertTrue(self.__team_exists(teams,"Georgia Tech","Atlantic Coast"))
        self.assertTrue(self.__team_exists(teams,"Cincinnati","American Athletic"))
        self.assertTrue(self.__team_exists(teams,"Illinois","Big Ten"))
        self.assertTrue(self.__team_exists(teams,"Western Kentucky","Sun Belt"))

    def test_get_team_names(self):
        spreadsheet = PoolSpreadsheet(2013)
        names = sorted(spreadsheet.get_team_names())
        self.assertEquals(len(names),126)
        self.assertIn("Georgia Tech",names)
        self.assertIn("TCU",names)
        self.assertIn("Southern Methodist",names)
        self.assertIn("Purdue",names)
        self.assertIn("Middle Tennessee",names)
        self.assertIn("Army",names)
        self.assertIn("Akron",names)
        self.assertIn("UNLV",names)
        self.assertIn("California",names)
        self.assertIn("South Carolina",names)
        self.assertIn("South Alabama",names)

    def test_get_conferences(self):
        spreadsheet = PoolSpreadsheet(2013)
        conferences = self.__get_conferences()
        self.assertEquals(sorted(spreadsheet.get_conferences()),sorted(conferences))

    def test_get_teams_in_conference(self):
        spreadsheet = PoolSpreadsheet(2013)
        self.assertEquals(spreadsheet.get_teams_in_conference("Bad Name"),None)
        self.assertEquals(sorted(spreadsheet.get_teams_in_conference("Sun Belt")),sorted(self.__get_teams_in_sunbelt()))
        self.assertEquals(sorted(spreadsheet.get_teams_in_conference("Atlantic Coast")),sorted(self.__get_teams_in_acc()))

    def __get_2013_player_names(self):
        players = [ "Neeley, Michael", "Marsh, Alexander Remote", "Robbins, Dale", "Ferguson, Scott Remote",
        "Hendrick, Matt R", "Neeley, Amber Remote", "Sams, David", "Steel, Van Remote", "Christiansen, Amos H",
        "Brunt, DavidRemote", "Chan, Simon", "Edwards, Christopher S", "Farren, Kevin M", "James, Larry C",
        "Nguyen, Thai", "Shuey, Jeffrey M", "Bowers, Martin L", "Farren, Leslie Remote", "Fonville, Chris",
        "Neill, Charles H", "White, Jarred", "Winburn, Steve A", "Emptage, Nick", "Holden, Brent",
        "Murphy, William A", "Reams, Byron L", "Carter, Chris", "Moore, Kevin B", "Aaron, Chip",
        "Locklear, Dave Remote", "McGee, Steve", "Wells, Seth Remote", "Gore, Brandon", "Gregory, Adam J",
        "Johnson, Robert J", "Young, Kenneth", "Desetto, Daniel", "Peng, Aaron", "Ruffin, Chris",
        "Sapp, Carl G", "Straw, Adam D", "Inabinet, Greg", "Boykin, Jerome W", "Powell, LaMar",
        "Staub, Kevin", "Martin, Douglas C", "Freedman, Scott Remote", "Holley, Jeremy Remote", "Desing, Scott M",
        "Penrose, Tim Remote", "Puga, Moises", "Allen, Landon Remote", "Clark, William J", "Redys, David Remote",
        "Nance, Rob" ]
        players.sort()
        return players

    def __get_2013_defaulters_per_week(self):
        d = dict()
        d[1] = [ "Sapp, Carl G" ]
        d[2] = [ "Clark, William J", "Freedman, Scott Remote"  ]
        d[3] = [ "Nance, Rob" ]
        d[4] = [ "Freedman, Scott Remote", "Nance, Rob" ]
        d[5] = [ "Clark, William J", "Desing, Scott M", "Nance, Rob" ]
        d[6] = [ "Nance, Rob", "Powell, LaMar" ]
        d[7] = [ "Clark, William J", "Nance, Rob", "Powell, LaMar", "Redys, David Remote" ] 
        d[8] = [ "Holley, Jeremy Remote", "Nance, Rob" ] 
        d[9] = [ "Boykin, Jerome W", "Nance, Rob", "Young, Kenneth" ]
        d[10] = [ "Boykin, Jerome W", "Nance, Rob" ]
        d[11] = [ "Allen, Landon Remote", "Clark, William J", "Nance, Rob", "Redys, David Remote" ]
        d[12] = []
        d[13] = [ "Allen, Landon Remote", "Clark, William J", "Freedman, Scott Remote", "Holley, Jeremy Remote", "Inabinet, Greg", "Nance, Rob", "Ruffin, Chris", "Wells, Seth Remote" ]
        return d

    def __get_2013_defaulters(self):
        defaulters_per_week = self.__get_2013_defaulters_per_week()
        defaulters = set()
        for wknum in defaulters_per_week:
            for defaulter_name in defaulters_per_week[wknum]:
                defaulters.add(defaulter_name)
        return list(defaulters)

    def __get_conferences(self):
        return ['Atlantic Coast','Pacific 12', 'Southeastern', 'Mountain West', 
                'Big 12', 'Big Ten', 'American Athletic', 'Conference USA', 
                'Independents', 'Mid American', 'Sun Belt']

    def __get_teams_in_sunbelt(self):
        return [ "Arkansas State", "Georgia State", "Louisiana Lafayette", "Louisiana Monroe",
                "South Alabama", "Texas State", "Troy", "Western Kentucky" ]

    def __get_teams_in_acc(self):
        return [ "Clemson", "Florida State", "North Carolina", "Pittsburgh",
                "Syracuse", "Boston College", "Duke", "Georgia Tech",
                "Maryland", "Miami-Florida", "NC State", "Virginia",
                "Virginia Tech", "Wake Forest" ]

    def __team_exists(self,teams,name,conference):
        for team in teams:
            if team.name == name and team.conference == conference:
                return True
        return False

    def __michael_player_info_correct(self,player):
        self.assertEquals(player.name,"Neeley, Michael")
        self.assertEquals(player.overall_rank,1)
        self.assertEquals(player.overall_points,75)
        self.assertEquals(player.week_points,{1:5,2:4,3:7,4:6,5:6,6:3,7:8,8:3,9:6,10:7,11:5,12:8,13:7})

    def __brent_player_info_correct(self,player):
        self.assertEquals(player.name, "Holden, Brent")
        self.assertEquals(player.overall_rank,23)
        self.assertEquals(player.overall_points,65)
        self.assertEquals(player.week_points,{1:5,2:4,3:6,4:6,5:6,6:5,7:5,8:3,9:8,10:2,11:6,12:3,13:6})

    def __rob_player_info_correct(self,player):
        self.assertEquals(player.name,"Nance, Rob")
        self.assertEquals(player.overall_rank,55)
        self.assertEquals(player.overall_points,31)
        self.assertEquals(player.week_points,{1:4,2:4,3:2,4:3,5:3,6:2,7:1,8:0,9:2,10:2,11:1,12:5,13:2})

    def __verify_week1_game_1(self,game):
        self.assertEquals(game.number,1)
        self.assertEquals(game.team1,"North Carolina")
        self.assertEquals(game.team2,"South Carolina")
        self.assertEquals(game.team1_score,10)
        self.assertEquals(game.team2_score,27)
        self.assertEquals(game.favored,"team2")
        self.assertEquals(game.spread,11.5)
        self.assertEquals(game.winner,"team2")
        self.assertEquals(game.state,"final")

    def __verify_week1_game_2(self,game):
        self.assertEquals(game.number,2)
        self.assertEquals(game.team1,"Utah State")
        self.assertEquals(game.team2,"Utah")
        self.assertEquals(game.team1_score,26)
        self.assertEquals(game.team2_score,30)
        self.assertEquals(game.favored,"team2")
        self.assertEquals(game.spread,2.5)
        self.assertEquals(game.winner,"team2")
        self.assertEquals(game.state,"final")

    def __verify_week1_game_3(self,game):
        self.assertEquals(game.number,3)
        self.assertEquals(game.team1,"Mississippi State")
        self.assertEquals(game.team2,"Oklahoma State")
        self.assertEquals(game.team1_score,3)
        self.assertEquals(game.team2_score,21)
        self.assertEquals(game.favored,"team2")
        self.assertEquals(game.spread,12.5)
        self.assertEquals(game.winner,"team2")
        self.assertEquals(game.state,"final")

    def __verify_week1_game_4(self,game):
        self.assertEquals(game.number,4)
        self.assertEquals(game.team1,"Penn State")
        self.assertEquals(game.team2,"Syracuse")
        self.assertEquals(game.team1_score,23)
        self.assertEquals(game.team2_score,17)
        self.assertEquals(game.favored,"team1")
        self.assertEquals(game.spread,7.5)
        self.assertEquals(game.winner,"team2")
        self.assertEquals(game.state,"final")

    def __verify_week1_game_5(self,game):
        self.assertEquals(game.number,5)
        self.assertEquals(game.team1,"LSU")
        self.assertEquals(game.team2,"TCU")
        self.assertEquals(game.team1_score,37)
        self.assertEquals(game.team2_score,27)
        self.assertEquals(game.favored,"team1")
        self.assertEquals(game.spread,4.5)
        self.assertEquals(game.winner,"team1")
        self.assertEquals(game.state,"final")

    def __verify_week1_game_6(self,game):
        self.assertEquals(game.number,6)
        self.assertEquals(game.team1,"Boise State")
        self.assertEquals(game.team2,"Washington")
        self.assertEquals(game.team1_score,6)
        self.assertEquals(game.team2_score,38)
        self.assertEquals(game.favored,"team2")
        self.assertEquals(game.spread,3.5)
        self.assertEquals(game.winner,"team2")
        self.assertEquals(game.state,"final")

    def __verify_week1_game_7(self,game):
        self.assertEquals(game.number,7)
        self.assertEquals(game.team1,"Northwestern")
        self.assertEquals(game.team2,"California")
        self.assertEquals(game.team1_score,44)
        self.assertEquals(game.team2_score,30)
        self.assertEquals(game.favored,"team1")
        self.assertEquals(game.spread,5.5)
        self.assertEquals(game.winner,"team1")
        self.assertEquals(game.state,"final")

    def __verify_week1_game_8(self,game):
        self.assertEquals(game.number,8)
        self.assertEquals(game.team1,"Colorado")
        self.assertEquals(game.team2,"Colorado State")
        self.assertEquals(game.team1_score,41)
        self.assertEquals(game.team2_score,27)
        self.assertEquals(game.favored,"team2")
        self.assertEquals(game.spread,2.5)
        self.assertEquals(game.winner,"team1")
        self.assertEquals(game.state,"final")

    def __verify_week1_game_9(self,game):
        self.assertEquals(game.number,9)
        self.assertEquals(game.team1,"Florida State")
        self.assertEquals(game.team2,"Pittsburgh")
        self.assertEquals(game.team1_score,41)
        self.assertEquals(game.team2_score,13)
        self.assertEquals(game.favored,"team1")
        self.assertEquals(game.spread,10.5)
        self.assertEquals(game.winner,"team1")
        self.assertEquals(game.state,"final")

    def __verify_week1_game_10(self,game):
        self.assertEquals(game.number,10)
        self.assertEquals(game.team1,"Georgia")
        self.assertEquals(game.team2,"Clemson")
        self.assertEquals(game.team1_score,35)
        self.assertEquals(game.team2_score,38)
        self.assertEquals(game.favored,"team1")
        self.assertEquals(game.spread,2.5)
        self.assertEquals(game.winner,"team2")
        self.assertEquals(game.state,"final")

    def __verify_brent_picks_week1(self,picks):
        brent_picks = { pick.game_number:pick for pick in picks if pick.player_name == "Holden, Brent" }
        self.assertEquals(len(brent_picks),10)
        self.assertEquals(brent_picks[1].game_number,1)
        self.assertEquals(brent_picks[2].game_number,2)
        self.assertEquals(brent_picks[3].game_number,3)
        self.assertEquals(brent_picks[4].game_number,4)
        self.assertEquals(brent_picks[5].game_number,5)
        self.assertEquals(brent_picks[6].game_number,6)
        self.assertEquals(brent_picks[7].game_number,7)
        self.assertEquals(brent_picks[8].game_number,8)
        self.assertEquals(brent_picks[9].game_number,9)
        self.assertEquals(brent_picks[10].game_number,10)
        self.assertEquals(brent_picks[1].winner,"team2")
        self.assertEquals(brent_picks[2].winner,"team2")
        self.assertEquals(brent_picks[3].winner,"team1")
        self.assertEquals(brent_picks[4].winner,"team1")
        self.assertEquals(brent_picks[5].winner,"team1")
        self.assertEquals(brent_picks[6].winner,"team1")
        self.assertEquals(brent_picks[7].winner,"team2")
        self.assertEquals(brent_picks[8].winner,"team2")
        self.assertEquals(brent_picks[9].winner,"team1")
        self.assertEquals(brent_picks[10].winner,"team2")

        for game_number in range(1,10):
            self.assertFalse(brent_picks[game_number].default)
            self.assertEquals(brent_picks[game_number].team1_score,None)
            self.assertEquals(brent_picks[game_number].team2_score,None)

        self.assertFalse(brent_picks[10].default)
        self.assertEquals(brent_picks[10].team1_score,24)
        self.assertEquals(brent_picks[10].team2_score,31)

    def __verify_carl_picks_week1(self,picks):
        carl_picks = { pick.game_number:pick for pick in picks if pick.player_name == "Sapp, Carl G" }
        self.assertEquals(len(carl_picks),10)
        self.assertEquals(carl_picks[1].game_number,1)
        self.assertEquals(carl_picks[2].game_number,2)
        self.assertEquals(carl_picks[3].game_number,3)
        self.assertEquals(carl_picks[4].game_number,4)
        self.assertEquals(carl_picks[5].game_number,5)
        self.assertEquals(carl_picks[6].game_number,6)
        self.assertEquals(carl_picks[7].game_number,7)
        self.assertEquals(carl_picks[8].game_number,8)
        self.assertEquals(carl_picks[9].game_number,9)
        self.assertEquals(carl_picks[10].game_number,10)
        self.assertEquals(carl_picks[1].winner,None)
        self.assertEquals(carl_picks[2].winner,None)
        self.assertEquals(carl_picks[3].winner,None)
        self.assertEquals(carl_picks[4].winner,None)
        self.assertEquals(carl_picks[5].winner,None)
        self.assertEquals(carl_picks[6].winner,None)
        self.assertEquals(carl_picks[7].winner,None)
        self.assertEquals(carl_picks[8].winner,None)
        self.assertEquals(carl_picks[9].winner,None)
        self.assertEquals(carl_picks[10].winner,None)

        for game_number in range(1,11):
            self.assertTrue(carl_picks[game_number].default)
            self.assertEquals(carl_picks[game_number].team1_score,None)
            self.assertEquals(carl_picks[game_number].team2_score,None)

def get_player_years_dict():
    dirname = _os.getcwd() + '/excel_history/data/'
    RE_FILE_SS = re.compile(r'^pool_(\d{4})_standings.xls')
    filelist = sorted([f for f in _os.listdir(dirname) if RE_FILE_SS.match(f)])

    player_years = {}
    for f in filelist:
        year = RE_FILE_SS.match(f).groups()[0]
        spreadsheet = PoolSpreadsheet(year)
        players = spreadsheet.get_player_names()
        for player in players:
            if player_years.get(player) is None:
                player_years[player] = [year]
            else:
                player_years[player].append(year)

    return player_years

def get_team_years_weeks_dict():
    dirname = _os.getcwd() + '/excel_history/data/'
    RE_FILE_SS = re.compile(r'^pool_(\d{4})_standings.xls')
    filelist = sorted([f for f in _os.listdir(dirname) if RE_FILE_SS.match(f)])

    team_years_weeks = {}
    for f in filelist:
        year = RE_FILE_SS.match(f).groups()[0]
        spreadsheet = PoolSpreadsheet(year)
        for week in spreadsheet.get_week_numbers():
            games = spreadsheet.get_games(week)
            for gamenum in games:
                game = games[gamenum]
                for team in (game.team1, game.team2):
                    if team_years_weeks.get(team) is None:
                        team_years_weeks[team] = []
                    team_years_weeks[team].append((year, week, game.number,))

    return team_years_weeks

if __name__ == "__main__":
    unittest.main()
