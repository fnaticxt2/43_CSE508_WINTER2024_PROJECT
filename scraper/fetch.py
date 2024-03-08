from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

import urllib.parse
import csv
from time import gmtime, strftime

import time

def getdriver():
    options = Options()
    #For Cron
    #options.add_argument("--headless")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    return driver

def login(driver,url):
    driver.get(url)
    time.sleep(4)
    username_elm = driver.find_element(By.XPATH,"//input[@name='session_key']")
    password_elm = driver.find_element(By.XPATH,"//input[@name='session_password']")

    username_elm.send_keys(email)
    password_elm.send_keys(password)
    time.sleep(4)
    driver.find_element(By.XPATH,"//button[@type='submit']").click()
    return driver

def createfile(filename):
    with open(filename, 'w', newline='') as f:      
        writer = csv.writer(f)
        f.close()

def addHeader(filename):
    fields=["id","label","title","company_name","location","fetch time","job time","jd","url"]
    with open(filename, 'a', newline='', encoding="utf-8") as f:      
        writer = csv.writer(f)
        writer.writerow(fields)
        f.close()

def autoScroll(element):
    elm_height = driver.execute_script("return arguments[0].scrollHeight", element)
    current_height=0
    while current_height < elm_height:
        driver.execute_script("arguments[0].scroll("+str(current_height)+","+str(current_height+50)+");", element)
        current_height+=200
        time.sleep(1)

if __name__ == "__main__":
    
    email=""
    password=""

    base_url = "https://www.linkedin.com"

    labels = ["Software Developer","Web Developer","Data Analyst","Systems Analyst","Network Engineer","Database Administrator","Quality Assurance (QA) Engineer","IT Support Engineer","Cybersecurity Analyst","Machine Learning Engineer","Cloud Engineer","DevOps Engineer","IT Project Manager","UI/UX Designer","Mobile App Developer"]

    driver=getdriver()

    filename = "data.csv"
    createfile(filename)
    addHeader(filename)
    
    driver=login(driver,base_url)
    time.sleep(50)

    i=1

    for label in labels:
        
        url = base_url+'/jobs/search/?keywords='+urllib.parse.quote_plus(label)+'&location=India&locationId=&geoId=102713980&f_TPR=r86400&f_PP=105282602%2C105214831%2C106164952%2C105556991%2C104990346'

        driver.get(url)
        time.sleep(5)

        element = driver.find_element(By.CLASS_NAME, 'jobs-search-results-list')
        autoScroll(element)
        time.sleep(2)
        
        
        try:
            joblist=driver.find_elements(By.CLASS_NAME, 'jobs-search-results__list-item')
        except NoSuchElementException:
            continue

        url_jobs = []
        for jobcard in joblist:
            try:
                joblinks = jobcard.find_elements(By.TAG_NAME, 'a')
            except NoSuchElementException:
                continue
            jonurl=""
            title=""
            if len(joblinks) > 0:
                joblink = joblinks[0]
                joburl = joblink.get_attribute("href")
                url_jobs.append(joburl)
        
        for url_job in url_jobs:
            driver.get(url_job)
            time.sleep(4)
            
            try:
                title=driver.find_element(By.CLASS_NAME, 'job-details-jobs-unified-top-card__job-title').text
            except NoSuchElementException:
                continue

            company_name=""
            job_time=""
            try:
                detail_container = driver.find_element(By.CLASS_NAME, 'job-details-jobs-unified-top-card__primary-description-container')
                
                company_name = detail_container.find_element(By.TAG_NAME, 'a').text
                job_time = detail_container.find_elements(By.TAG_NAME, 'span')[2].text

            except NoSuchElementException:
                pass
            
            
            try:
                driver.execute_script("window.scroll(0,300);")
                time.sleep(1)
                more_button = driver.find_element(By.CLASS_NAME,"jobs-description__footer-button")
                if more_button:
                    more_button.click()
            except Exception:
                print("Exception")
                pass
            
            
            try:
                job_details = driver.find_element(By.ID, 'job-details').text
            except NoSuchElementException:
                job_details=""

            try:
                driver.execute_script("window.scroll(0,900);")
                time.sleep(1)
                location = driver.find_element(By.CLASS_NAME, 'jobs-unified-top-card__bullet').text
            except NoSuchElementException:
                location=""


            curr_time = strftime("%H:%M:%S", gmtime())

            print(i)
            print(title)

            with open(filename, 'a', newline='', encoding="utf-8") as f:      
                writer = csv.writer(f)
                writer.writerow([i,label,title,company_name,location,curr_time,job_time,job_details,url_job])
                f.close()
            
            i=i+1


        




       


    