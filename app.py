from flask import Flask,jsonify
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

def scrape_site(SAMPLE_URL):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("window-size=1920x1080")
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')    
    options.add_argument('--disable-dev-shm-usage')
    
    # options.add_argument('--disable-dev-shm-usage') # Not used 
    driver = webdriver.Chrome(chrome_options=options)
    
    
    driver.get(SAMPLE_URL)
  
    try:
        close = driver.find_element(By.CSS_SELECTOR,"[class^='modal-title']")
        close.click()
    except:
        pass
    menu = driver.find_element(By.LINK_TEXT, 'Agromet Advisories')
    time.sleep(5)
    menu.click()
    submenu = driver.find_element(By.LINK_TEXT, 'Block Level AAS Bulletin')
    time.sleep(5)
    submenu.click()
    #select state
    #inpState = '11'
    inpState= []
    states = {'26' : 'Telangana'}
    for i in states.keys():
         inpState.append(i)
    selectState = Select(driver.find_element_by_id('select_state'))
    time.sleep(5)
    selectState.select_by_value(inpState[0])
    driver.find_element_by_id('select_dist').click() 
    time.sleep(5)
    htmlSource = driver.page_source
    soup= BeautifulSoup(htmlSource,'html.parser')
    content=soup.find(attrs={'id':'select_dist'})
    dist = content.find_all('option')
    return 'output'

    
    
URL = 'https://www.imdagrimet.gov.in/'
app = Flask(__name__)
@app.route('/')
def home():
    result = scrape_site(URL)
    return result
if __name__ == '__main__':
    app.run(debug=False)