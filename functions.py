from scraped import TfrrsWebPage

# urls:
CONFERENCE = "https://www.tfrrs.org/leagues/1398.html"
WHEATON_TRACK = "https://www.tfrrs.org/teams/IL_college_m_Wheaton_IL.html"
WHEATON_XC = "https://www.tfrrs.org/teams/xc/IL_college_m_Wheaton_IL.html"
# output_folder = '/Users/hudsonthomas/Desktop/Tffrs_data/recent_results'


def get_last_4_races_xc_cciw(output_folder):

    conference_page = TfrrsWebPage(CONFERENCE)
    recent_meets = conference_page.tables["MEET RESULTS"]["MEET"]

    race_counter = 0
    for meet_name, meet_url in recent_meets:
        if "xc" in meet_url:
            meet_page = TfrrsWebPage(meet_url)
            meet_page.to_csv(output_folder)
            race_counter += 1

        if race_counter == 4:
            break


def get_last_4_races_track_cciw(output_folder):

    conference_page = TfrrsWebPage(CONFERENCE)
    recent_meets = conference_page.tables["MEET RESULTS"]["MEET"]

    race_counter = 0
    for meet_name, meet_url in recent_meets:
        if not "xc" in meet_url:
            meet_page = TfrrsWebPage(meet_url)
            meet_page.to_csv(output_folder)
            race_counter += 1

        if race_counter == 4:
            break

def calculate_athlete_season_avg(athlete):
    wheaton_page = TfrrsWebPage(WHEATON_XC)

    athletes = wheaton_page.tables['ROSTER']['NAME']
    athletes = {name: url for name, url in athletes}
    athlete_url = athletes[athlete]

    athlete_page = TfrrsWebPage(athlete_url)
    a = 1



#calculate_athlete_season_avg('Caraway, Joe')

metrics = []
plotters = []
savers = [get_last_4_races_xc_cciw, get_last_4_races_track_cciw]

#get_last_4_races_mens_xc_conference(output_folder)
