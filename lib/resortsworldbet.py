from lib import model
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import xml.etree.ElementTree as ET
import conf.selenium_conf as selenium_conf
import time

def _parse_matchup(matchup, names, odds, dates):
    #check if the word moneyline is anywhere in the text
    ml_odds_elements = matchup.find_elements(By.XPATH, './/button')
    #since there is no exact identifier for moneyline odds on pointsbet, we will have o look through all
    #the elements and choose what is moneyline and what is not
    money_line_odds = []
    for ml_odds_element in ml_odds_elements:
        ml_odds_element_text = ml_odds_element.text
        if model._is_ml_odds(ml_odds_element_text):
            money_line_odds.append(ml_odds_element_text)
    if len(money_line_odds) == 2: #only if there are 2 elements in the money line odds
        #add those odds to the odds list
        odds.extend(money_line_odds)
        #get the teams
        teams = matchup.find_elements(By.XPATH, './/p[@class="f1433yxm f18qd5f1 fxmujud"]')
        for team in teams:
            team_text = team.text
            #team_text = MLB_NAME_STORE_MAP[team_text]
            names.append(team_text)
        #get the date
        #check if game is live
        game_is_live = matchup.find_elements(By.XPATH, './/span[@class="fzmd45l"]')
        if game_is_live != []:
            dates.append('LIVE')
        else:
            dates_elements = matchup.find_elements(By.XPATH, './/span[@class="fhbnz7c fp77qq7"]')
            for date_element in dates_elements:
                date_text = date_element.text
                if ':' in date_text:
                    date_text = model._date_parser(date_text)
                    dates.append(date_text)

def _parse(queue):
    # Set Chrome options
    options = Options()
    #options.add_argument("--headless")  # Set to "--headless" for running in the background
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    driver.get("https://resortsworldbet.com/sports/baseball/MLB")
    old_data = driver.find_elements(By.XPATH, '//div[@class="f1gfplum"]')
    while True:
        try:
            new_data = driver.find_elements(By.XPATH, '//div[@class="f1gfplum"]')
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
                queue.put(("resort world", output))

            old_data = new_data
            time.sleep(1)

        except Exception as e:
            print(f"An error occurred in resortsworldbet: {e}")




