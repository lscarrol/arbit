from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import xml.etree.ElementTree as ET
import conf.selenium_conf as selenium_conf

def _session(url):
    options = Options()
    options.add_argument(selenium_conf.args['user_agent'])
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    return driver


