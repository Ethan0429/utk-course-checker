import random
import sys
import time
import os
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import smtplib

load_dotenv()

TIMEOUT_TIME = 10
login_url = 'https://cas.tennessee.edu/cas/login?TARGET=https%3A%2F%2Fbannerreg.utk.edu%2FStudentRegistrationSsb%2Flogin%2Fcas'


def login():

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')

    # service = webdriver.chrome.service.Service('driver/chromedriver')
    driver = webdriver.Chrome(
        options=options)

    driver.get(login_url)

    WebDriverWait(driver, TIMEOUT_TIME).until(
        EC.presence_of_element_located((By.ID, 'password'))
    )

    # login
    driver.find_element(By.ID, 'username').send_keys(os.getenv('USERNAME'))
    driver.find_element(By.ID, 'password').send_keys(os.getenv('PASSWORD'))
    driver.find_element(By.NAME, 'submit').send_keys(Keys.RETURN)

    print('Push sent...')
    # wait for registerLink id to appear
    WebDriverWait(driver, TIMEOUT_TIME*6).until(
        EC.presence_of_element_located((By.ID, 'registerLink'))
    )

    # click registerLink
    driver.find_element(By.ID, 'registerLink').send_keys(Keys.RETURN)

    # wait until s2id_txt_term id appears
    WebDriverWait(driver, TIMEOUT_TIME).until(
        EC.presence_of_element_located((By.ID, 's2id_txt_term'))
    )

    # click s2id_txt_term
    driver.find_element(By.ID, 's2id_txt_term').click()

    # wait until 202320 id appears
    WebDriverWait(driver, TIMEOUT_TIME).until(
        EC.presence_of_element_located((By.ID, '202320'))
    )

    # click 202320
    driver.find_element(By.ID, '202320').click()

    # wait until term-go id appears
    WebDriverWait(driver, TIMEOUT_TIME).until(
        EC.presence_of_element_located((By.ID, 'term-go'))
    )

    # click term-go
    driver.find_element(By.ID, 'term-go').click()

    # get cookies
    time.sleep(5)
    cookies = driver.get_cookies()
    driver.quit()
    return cookies


def listen(cookies, watchlist):
    while True:
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])

        if session.get('https://cas.tennessee.edu/cas/login?TARGET=https%3a%2f%2fmyutk.utk.edu%2fCASLogin.aspx').status_code != 302:
            print('Session expired, logging in again...')
            return watchlist

        session.post(
            'https://bannerreg.utk.edu/StudentRegistrationSsb/ssb/classSearch/resetDataForm')

        if watchlist is None:
            with open('watchlist.txt', 'r') as f:
                watchlist = f.read().splitlines()
                watchlist = [[course, False] for course in watchlist]

        for course in watchlist:
            time.sleep(5)
            course_abrv, course_num = course[0].split(' ')

            search_url = f'https://bannerreg.utk.edu/StudentRegistrationSsb/ssb/searchResults/searchResults?txt_subject={course_abrv}&txt_courseNumber={course_num}&txt_term=202320&startDatepicker=&endDatepicker=&pageOffset=0&pageMaxSize=10&sortColumn=subjectDescription&sortDirection=asc'

            search_results = session.get(search_url).json()

            if search_results['ztcEncodedImage'] is None:
                print('Session expired, logging in again...')
                return watchlist

            session.post(
                'https://bannerreg.utk.edu/StudentRegistrationSsb/ssb/classSearch/resetDataForm')

            msg = f'Course: {search_results["data"][0]["courseTitle"]}\nSeats Available: {search_results["data"][0]["seatsAvailable"]}\n' if int(
                search_results['data'][0]['seatsAvailable']) != 0 else None

            if msg is not None:
                course[1] = True
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(os.getenv('EMAIL'), os.getenv('EMAIL_PASSWORD'))
                server.sendmail(from_addr=os.getenv('EMAIL'), to_addrs=os.getenv(
                    'EMAIL'), msg=f'Subject: {course_abrv} {course_num} is open!\n\n{msg}')
                server.quit()
                watchlist.remove(course)

        time.sleep(300)


if __name__ == '__main__':
    with open('watchlist.txt', 'r') as f:
        watchlist = f.read().splitlines()
        watchlist = [[course, False] for course in watchlist]
    while True:
        try:
            watchlist = listen(login(), watchlist)
        except Exception as e:
            print(e)
            print('Error, retrying...')
            pass
