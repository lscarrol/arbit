from lib import model
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import xml.etree.ElementTree as ET
import conf.selenium_conf as selenium_conf
import time


MLB_NAME_STORE_MAP = {
    'CHI White Sox' : 'Chicago White Sox',
    'CHI Cubs' : 'Chicago Cubs',
    'CLE Guardians' : 'Cleveland Guardians',
    'CIN Reds' : 'Cincinnati Reds',
    'DET Tigers' : 'Detroit Tigers',
    'MIL Brewers' : 'Milwaukee Brewers',
    'KC Royals' : 'Kansas City Royals',
    'PIT Pirates' : 'Pittsburgh Pirates',
    'MIN Twins' : 'Minnesota Twins',
    'STL Cardinals' : 'St. Louis Cardinals',
    'BAL Orioles' : 'Baltimore Orioles',
    'ATL Braves' : 'Atlanta Braves',
    'BOS Red Sox' : 'Boston Red Sox',
    'MIA Marlins' : 'Miami Marlins',
    'NY Yankees' : 'New York Yankees',
    'NY Mets' : 'New York Mets',
    'TB Rays' : 'Tampa Bay Rays',
    'PHI Phillies' : 'Philadelphia Phillies',
    'TOR Blue Jays' : 'Toronto Blue Jays',
    'WAS Nationals' : 'Washington Nationals',
    'HOU Astros' : 'Houston Astros',
    'ARI Diamondbacks' : 'Arizona Diamondbacks',
    'LA Angels' : 'Los Angeles Angels',
    'COL Rockies' : 'Colorado Rockies',
    'OAK Athletics' : 'Oakland Athletics',
    'LA Dodgers' : 'Los Angeles Dodgers',
    'SEA Mariners' : 'Seattle Mariners',
    'SD Padres' : 'San Diego Padres',
    'TEX Rangers' : 'Texas Rangers',
    'SF Giants' : 'San Francisco Giants'
}

def betrivers_date_parser(string):
    string = string.upper()
    if 'TODAY' in string:
        return model.get_formatted_date()
    elif 'TOMORROW' in string:
        output = model.get_tomorrow_date()
        return output
    elif model.game_is_weekday(string):
        output = model.get_upcoming_date_weekday(string[:3])
        return output
    elif model.extract_date(string):
        extracted_date = model.extract_date(string)
        output = model.get_upcoming_month_date(extracted_date)
        return output
    else:
        return False


def _parse_matchup(matchup, names, odds, dates):
    ml_odds_elements = matchup.find_elements(By.XPATH, ".//ms-event-pick")
    ml_odds_elements_text = [element.text for element in ml_odds_elements if model._is_ml_odds(element.text)]
    if len(ml_odds_elements_text) == 2: #only if there are 2 elements in the money line odds
        #get the money line odds
        odds.extend(ml_odds_elements_text)
        #get the teams
        teams = matchup.find_elements(By.XPATH, './/div[@class="participant"]')
        for team in teams:
            team_text = team.text
            #team_text = MLB_NAME_STORE_MAP[team_text]
            names.append(team_text)
        #get the date
        if 'LIVE' in matchup.text:
            dates.append('LIVE')
        else:
            dates_elements = matchup.find_elements(By.XPATH, './/ms-event-timer')
            for date_element in dates_elements:
                date_text = date_element.text
                date_text = betrivers_date_parser(date_text)
                dates.append(date_text)

def _parse(queue):
    # Set Chrome options
    options = Options()
    #options.add_argument("--headless")  # Set to "--headless" for running in the background
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    driver.get("https://sports.ny.betmgm.com/en/sports/baseball-23/betting/usa-9/mlb-75")
    old_data = driver.find_elements(By.XPATH, '//ms-six-pack-event')
    while True:
        try:
            new_data = driver.find_elements(By.XPATH, '//ms-six-pack-event')
            if new_data != old_data:
                names = []
                odds = []
                dates = []
                for matchup in new_data:
                    _parse_matchup(matchup, names, odds, dates)
                output = []
                for i in range(len(dates)):
                    date = dates[i]
                    team_1 = names[i * 2]
                    team_2 = names[i * 2 + 1]
                    odds_1 = odds[i * 2]
                    odds_2 = odds[i * 2 + 1]
                    output.append([date, team_1, odds_1, team_2, odds_2])
                queue.put(("betmgm", output))

            old_data = new_data
            time.sleep(1)

        except Exception as e:
            print(f"An error occurred in betmgm: {e}")