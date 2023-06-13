import lib.model as model
import lib.selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import xml.etree.ElementTree as ET
import conf.selenium_conf as sel

def _parse():
    options = Options()
    options.add_argument(sel.args['user_agent'])
    driver = webdriver.Chrome(options=options)
    driver.get("https://ny.pointsbet.com/sports/baseball/MLB")
    #driver = selenium._session("https://ny.pointsbet.com/sports/baseball/MLB")
    matchups = driver.find_elements(By.XPATH, '//div[@class="f3wis39"]')
    print(matchups)
    names = []
    odds = []
    dates = []
    #date doesnt need to change ig bc its always available
    for matchup in matchups:
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
            teams = matchup.find_elements(By.XPATH, './/p[@class="f1433yxm flyt76h f1wtz5iq f1rokedd"]')
            for team in teams:
                team_text = team.text
                #team_text = MLB_NAME_STORE_MAP[team_text]
                names.append(team_text)
            #get the date
            #check if game is live
            game_is_live = matchup.find_elements(By.XPATH, './/span[@class="f19o8v8p f18z9xf9"]')
            if game_is_live != []:
                dates.append('LIVE')
            else:
                dates_elements = matchup.find_elements(By.XPATH, './/span[@class="fnapeds f1pfs6av"]')
                for date_element in dates_elements:
                    date_text = date_element.text
                    if ':' in date_text:
                        date_text = model._date_parser(date_text)
                        dates.append(date_text)
    
    output = []
    for i in range(len(dates)):
        date = dates[i]
        team_1 = names[i * 2]
        team_2 = names[i * 2 + 1]
        odds_1 = odds[i * 2]
        odds_2 = odds[i * 2 + 1]
        output.append([date, team_1, odds_1, team_2, odds_2])
    while(True):
       pass
    return model.dictionarify(output)