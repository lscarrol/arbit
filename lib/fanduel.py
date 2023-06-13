from lib import model
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import xml.etree.ElementTree as ET
import conf.selenium_conf as selenium_conf
import time


def fanduel_date_parser(string):
    if game_is_today(string): #if the game is not today
        return model.get_formatted_date()
    elif game_is_weekday(string):
        output = model.get_upcoming_date_weekday(string[:3])
        return output
    elif game_is_month_day(string):
        if string[6] == ',':
            output = model.get_upcoming_month_date(string[:6])
        else:
            output = model.get_upcoming_month_date(string[:5])
        return output
    else:
        return False

def _parse_matchup(matchup, names, odds, dates):
    #check if the word moneyline is anywhere in the text
    ml_odds_elements = matchup.find_elements(By.XPATH, './/div[contains(@aria-label, "Moneyline")]')
    if len(ml_odds_elements) == 2: #only if there are 2 elements in the money line odds
        #get the money line odds
        for ml_odds_element in ml_odds_elements:
            ml_odds_elements_text = ml_odds_element.text
            if ml_odds_elements_text != '':
                odds.append(ml_odds_elements_text)
        #get the teams
        teams = matchup.find_elements(By.XPATH, './/span[@class="ae af gy gz ha hb ge gf gg gk hc s dt br hd h i j ah ai m aj o ak q al cd"]')
        for team in teams:
            team_text = team.text
            #team_text = MLB_NAME_STORE_MAP[team_text]
            names.append(team_text)
        #get the date
        inner_html = matchup.get_attribute("innerHTML")
        if "<title>live event</title>" in inner_html:
            dates.append('LIVE')
        else:
            dates_elements = matchup.find_elements(By.XPATH, './/time[@class="af hz s dm dn ee go h i j ah ai m aj o ak q al gp"]')
            for date_element in dates_elements:
                date_text = date_element.text
                date_text = fanduel_date_parser(date_text)
                dates.append(date_text)

def _parse(queue):
    # Set Chrome options
    options = Options()
    #options.add_argument("--headless")  # Set to "--headless" for running in the background
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    driver.get("https://sportsbook.fanduel.com/navigation/mlb")
    old_data = driver.find_elements(By.XPATH, '//div[@class="gd af s h i j ah ai m aj o ak q al"]')
    while True:
        try:
            new_data = driver.find_elements(By.XPATH, '//div[@class="gd af s h i j ah ai m aj o ak q al"]')
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
                queue.put(("fanduel", output))

            old_data = new_data
            time.sleep(1)

        except Exception as e:
            print(f"An error occurred in fanduel: {e}")

