from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup
from lxml import etree
import pytesseract
import cv2
from datetime import datetime
import requests
import schedule
import threading
import json
import os




def iniciar_driver():
    chrome_options = Options()
    arguments = ['--lang=pt-BR', '--window-size=1000,800', '--incognito']
    for argument in arguments:
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1,

    })
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager(version="114.0.5735.90").install()), options=chrome_options)

    return driver


def pagini2(driver, link):
    driver.get(link)

    driver.execute_script('window.scrollTo(0, 320);')
    sleep(2)

    driver.find_element(By.XPATH,'//*[@id="DataInicial"]').click()
    sleep(3)
        
    driver.find_element(By.XPATH,'//th[@class="today"]').click()
    sleep(5)

    driver.find_element(By.XPATH,'//*[@id="btnEnviarFiltroGeral-5231"]').click()
    sleep(1)

    driver.execute_script('window.scrollTo(0, 1900);')
    sleep(200)

driver = iniciar_driver()
link = 'https://www.agrolink.com.br/cotacoes/graos/arroz/'

pagini2(driver, link)