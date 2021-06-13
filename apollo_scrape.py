from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import numpy as np
import pandas as pd
import xlrd
import requests
import csv
from bs4 import BeautifulSoup

companies = [
            'Intellia Therapeutics',
            'Amkor Technology',
            'Amicus Therapeutics',
            'Neurocrine Biosciences',
            'CMC Materials',
            'Darling Ingredients',
            'Brooks Automation',
            'Inphi',
            'World Wrestling Entertainment',
            'Science Applications International',
            'Chemocentryx',
            'Chemed',
            'Lithia Motors',
            'Insmed',
            'Beyond Meat',
            'Hecla Mining',
            'CareDx',
            'Amedisys',
            'Simpson Manufacturing',
            'II-VI',
            'Sorrento Therapeutics',
            'Toro',
            'Fate Therapeutics',
            'Mercury Systems',
            'IRhythm Technologies',
            'J2 Global',
            'BlackLine',
            'Thor Industries',
            'Builders FirstSource',
            'LCI Industries',
            'Quaker Chemical',
            'Inspire Medical Systems',
            'Antero Midstream',
            'TopBuild',
            'Bandwidth',
            'STAAR Surgical',
            'PagerDuty',
            'BMC Stock Holdings',
            'Onto Innovation',
            'Upwork',
            'FormFactor',
            'Silgan Holdings',
            'Smartsheet',
            'Shutterstock',
            '2U',
            'Universal Forest Prods',
            'Lattice Semiconductor',
            'Axon Enterprise',
            'Saia'
             ]
categories = ['data', 'VP', 'HR']


driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://app.apollo.io/#/login?redirectTo=https%3A%2F%2Fapp.apollo.io%2F%23%2Fonboarding%2Fbulk%3F_k%3Dnbfzqc&_k=hpz0x5")
time.sleep(0.5)
driver.maximize_window()
time.sleep(2)

driver.find_element_by_name('email').send_keys('daniel_schwartz@college.harvard.edu')
driver.find_element_by_name('password').send_keys('Cessnap1Cessnap1')
logIn = driver.find_element_by_class_name("zp_2z1mP")

time.sleep(1)

logIn.click()

time.sleep(2)


with open('/Users/danielschwartz/downloads/first_run.csv', "a") as f:
    writer = csv.writer(f)
    # writer.writerow(["company", "name", "role", "email"])
    for company_name in companies:
        contact_limit = 5
        search_bar = driver.find_element_by_class_name("zp_MIz8G")
        search_bar.clear()
        time.sleep(1)
        search_bar.send_keys(company_name)

        time.sleep(3)
        # Clicking the 6th entry which should be the compnay (not great)
        try:
            driver.find_element_by_xpath('//*[@id="provider-mounter"]/div/div[2]/div[2]/div/div[1]/div/div[1]/div[1]/div[4]/div/div/div/div/div/div[6]/div[2]').click()
        except Exception:
            continue

        time.sleep(1)

        driver.get(driver.current_url + '/people')
        time.sleep(2)

        for cat in categories:
            
            try:
                search = driver.find_element_by_xpath("//input[@placeholder='Search People...']")
            except:
                continue
            time.sleep(1)
            search.clear()
            time.sleep(0.5)
            search.send_keys(cat)
            search.send_keys(Keys.RETURN)
            time.sleep(0.5)
            page_num_url = driver.current_url
            for i in range(2,5):
                time.sleep(3)
                # page_num_url = driver.current_url
                try:
                    people = driver.find_elements_by_class_name('zp_1svmi')
                    if people == []:
                        break
                    for person in range(len(people)):
                        if contact_limit <= 0:
                            break
                        info = people[person].get_attribute('innerText')
                        tmp = info
                        name = tmp.split('\n')[0]
                        info = info.lower()
                        if 'director' in info or 'sr.' in info or 'senior' in info or 'vp' in info or 'chief' in info or 'vice president' in info:
                            contact_limit -= 1
                            info = info.split('\n')
                            role = info[1].strip()
                            time.sleep(0.5)
                            driver.find_element_by_partial_link_text(name).click()
                            time.sleep(0.5)
                            print('about to try to click')
                            try:
                                driver.find_element_by_xpath('//*[@id="provider-mounter"]/div/div[2]/div[2]/div/div[1]/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div[2]/div/div[2]/div/span/a').click()                        
                                time.sleep(2)
                            except:
                                time.sleep(2)
                                print('cant click email')
                            try:
                                email = driver.find_element_by_xpath('//*[@id="provider-mounter"]/div/div[2]/div[2]/div/div[1]/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div[3]/div/div/div/div/div/div[2]/div/div/span').get_attribute('innerText')
                            except:
                                email = ''
                                print('no email')
                            row = [company_name, name, role, email]
                            writer.writerow(row)
                            print(row)
                            driver.get(page_num_url)
                            print('go to page url')
                            time.sleep(2)
                            break

                    driver.get(str(page_num_url)[:-1]+str(i))
                    page_num_url = str(page_num_url)[:-1]+str(i)
                except Exception:
                    print('exception')
                    driver.get(str(page_num_url)[:-1]+str(i))
                    time.sleep(2)
                    break
