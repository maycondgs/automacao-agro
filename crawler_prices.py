from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as condicao_esperada
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
from lxml import etree 
from PIL import Image
from time import sleep
import pytesseract
import urllib.request
from pandas import pandas as pd
import cv2
from datetime import datetime
import requests
import schedule
import threading
import json
import math
import mysql.connector
import os


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


dda = datetime.today()
da = str(dda).split(' ')
dataa = da[0].split('-')
data = f'{dataa[2]}/{dataa[1]}/{dataa[0]}'
data_hoje = da[0]


db = mysql.connector.connect(
    user='marceloagrouser',
    password='zHXBNu99drvBzHXBNu99drvBTf0Exe3pTf0Exe3p',
    host = 'connection-agrolivre-542543.agrolivrebrasil.com',
    port = '45821',
    database='agrolivre'
)




def iniciar_driver():

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--remote-debugging-pipe')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')


    service = Service()

    driver = webdriver.Chrome(service=service, options=chrome_options)


    wait = WebDriverWait(
        driver,
        50,
        poll_frequency=5,
        ignored_exceptions=[
            NoSuchElementException,
            ElementNotVisibleException,
            ElementNotSelectableException,
        ]
    )

    return driver,wait



pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
#pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

continu = True



def login(driver):

    sleep(1)
    driver.get('https://www.agrolink.com.br/login')
    sleep(2)

    driver.execute_script('window.scrollTo(0, 310);')
    sleep(1)

    driver.find_element(By.XPATH,'/html/body/div[1]/main/div[2]/div/div/div/section[1]/div/div/form/div[1]/div[2]/input').send_keys('xetedo9314@ratedane.com')
    sleep(2)
    driver.find_element(By.XPATH,'/html/body/div[1]/main/div[2]/div/div/div/section[1]/div/div/form/div[2]/div[2]/input').send_keys('webscraper')

    driver.find_element(By.XPATH,'/html/body/div[1]/main/div[2]/div/div/div/section[1]/div/div/form/div[3]/button').click()




def busca(driver,wait, prodformat):

    match prodformat:
        case 'algodao':
            link_search = 'https://www.agrolink.com.br/cotacoes/diversos/algodao/'
        case 'arroz':
            link_search = 'https://www.agrolink.com.br/cotacoes/graos/arroz/'
        case 'amendoim':
            link_search = 'https://www.agrolink.com.br/cotacoes/diversos/amendoim/'
        case 'cafe':
            link_search = 'https://www.agrolink.com.br/cotacoes/graos/cafe/'
        case 'cana':
            link_search = 'https://www.agrolink.com.br/cotacoes/diversos/cana-de-acucar/'
        case 'feijao':
            link_search = 'https://www.agrolink.com.br/cotacoes/graos/feijao/'
        case 'milho':
            link_search = 'https://www.agrolink.com.br/cotacoes/graos/milho/'
        case 'soja':
            link_search = 'https://www.agrolink.com.br/cotacoes/graos/soja/'
        case 'sorgo':
            link_search = 'https://www.agrolink.com.br/cotacoes/graos/sorgo/'
        case 'trigo':
            link_search = 'https://www.agrolink.com.br/cotacoes/graos/trigo/'
        case 'suinos':
            link_search = 'https://www.agrolink.com.br/cotacoes/carnes/suinos/'
        case 'aves':
            link_search = 'https://www.agrolink.com.br/cotacoes/carnes/aves/'
        case 'caprinos':
            link_search = 'https://www.agrolink.com.br/cotacoes/carnes/caprinos/'
        case 'ovinos':
            link_search = 'https://www.agrolink.com.br/cotacoes/carnes/ovinos/'
        case 'beterraba':
            link_search = 'https://www.agrolink.com.br/cotacoes/hortalicas/beterraba/'
        case 'tomate':
            link_search = 'https://www.agrolink.com.br/cotacoes/hortalicas/tomate/'
        case 'pimentao':
            link_search = 'https://www.agrolink.com.br/cotacoes/hortalicas/pimentao/'
        case 'cebola':
            link_search = 'https://www.agrolink.com.br/cotacoes/diversos/cebola/'
        case 'couve':
            link_search = 'https://www.agrolink.com.br/cotacoes/hortalicas/couve/'
        case 'cenoura':
            link_search = 'https://www.agrolink.com.br/cotacoes/hortalicas/cenoura/'
        case 'boi':
            link_search = 'https://www.agrolink.com.br/cotacoes/carnes/bovinos/boi-gordo-15kg'
        case 'vaca':
            link_search = 'https://www.agrolink.com.br/cotacoes/carnes/bovinos/vaca-gorda-15kg'


    driver.get(link_search)
    sleep(1)

    driver.execute_script('window.scrollTo(0, 350);')
    sleep(5)

    try:
        dattaa = wait.until(condicao_esperada.presence_of_element_located((By.XPATH,'/html/body/div[1]/main/div/div/div/div[1]/div[1]/div/div/div/form/div[2]/div[3]/div[2]/div/div[1]/div/input'))).click()
        sleep(3)

        btn_date = wait.until(condicao_esperada.element_to_be_clickable((By.XPATH,'//th[@class="today"]'))).click()
        sleep(3)

        btn_form = wait.until(condicao_esperada.element_to_be_clickable((By.XPATH,'//*[@id="btnEnviarFiltroGeral-5231"]')))
        sleep(1)

        driver.execute_script("arguments[0].click();", btn_form)

    except:
        continu = False
        return



def scraw(driver, wait):

    itens = []
    sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    dom = etree.HTML(str(soup)) 
    
    table = (dom.xpath('//*/table/tbody'))

    products = []
    locals = []
    last_update = []

    for tbody in table:
        trs = tbody.xpath('.//tr')
        trs = trs[1:]
        for tr in trs:
            td1 = tr.xpath('.//td[1]/text()')
            td2 = tr.xpath('.//td[2]/text()')
            td4 = tr.xpath('.//td[4]/text()')

            td2 = td2[0].strip()
            if "'" in td2:
                td2 = td2.replace("'", "")
            
            up = td4[0].strip()
            up = up.split('/')
            td4 = f'{up[2]}-{up[1]}-{up[0]}'

            products.append(td1[0].strip())
            locals.append(td2)
            last_update.append(td4)


    pre = wait.until(condicao_esperada.visibility_of_all_elements_located((By.XPATH, '/html/body/div[1]/main/div/div/div/div[1]/div[4]/div/div/div/table/tbody/tr/td[3]/div')))



    precos = []

    for prev in pre:
        linkpre = prev.get_attribute('style')
        i = linkpre.strip()
        addr = i.split('"')
        linkk = addr[1]

        link2 = addr[2].split(';')
        wid = link2[2]
        widt = wid.split(' ')
        hei = link2[3]
        heigh = hei.split(' ')
        ind = link2[4]
        indices = ind.split(': ')
        indice = indices[1].split(' ')
        sta = indice[0]
        en = indice[1]

        star = sta.split('px')
        enn = en.split('px')


        if star[0] == '0':
            start = star[0]
        else:
            starr = star[0].split('-')
            start = starr[1]

        if enn[0] == '0':
            end = enn[0]
        else:
            ennn = enn[0].split('-')
            end = ennn[1]


        width = widt[2].split('p')
        height = heigh[2].split('p')

        urllib.request.urlretrieve(linkk, "./imagem.png")


        img = Image.open("imagem.png")

        ys = int(end)
        yf = int(end) + int(height[0])

        xs = int(start)
        xf  = int(start) + int(width[0])

        croped = img.crop((xs, ys, xf, yf))

        pre = pytesseract.image_to_string(croped)
        prec = pre.split('\n')
        preco = str(prec[0])

        if 'B' in preco:
            preco = preco.replace("B", "8")
        if 'O' in preco:
            preco = preco.replace("O", "0")
        if 'S' in preco:
            preco = preco.replace("S", "5")

        precos.append(str(preco))


    data = []

    for product, locale, price, ultup in  zip(products, locals, precos, last_update):
        obj = {
            'Produto': product,
            'Local': locale,
            'Preco': price,
            'Update': ultup,
            'Data': data_hoje
        }

        data.append(obj)
        

    return data



def page(driver, wait):


    next_btn = driver.find_element(By.XPATH, '//*/a[@class="btn-navigation btn-navigation-next"]')

    sleep(2)
    driver.execute_script("arguments[0].scrollIntoView();", next_btn)

    driver.execute_script("window.scrollBy(0, -100);")

    driver.execute_script("arguments[0].click();", next_btn)
    #next_btn = wait.until(condicao_esperada.presence_of_element_located((By.XPATH, '//*[@id="frmMercadoFisico-5181"]/div/a')))
    #next_btn.click()
    sleep(5)
    driver.execute_script('window.scrollTo(0, 2200);')


def post(itemarq, item):

    cursor = db.cursor()
    sql = f"INSERT INTO quotes_{itemarq} (item, state, price, date_update ,date_scraping) VALUES ('{item['Produto']}', '{item['Local']}', '{item['Preco']}', '{item['Update']}', '{item['Data']}')"
    cursor.execute(sql)
    db.commit()



def crawler(driver, wait, prodformat):
    

    busca(driver, wait, prodformat)

    if continu == True:

        driver.execute_script('window.scrollTo(0, 2000);')
        sleep(3)


        try:
            inf = driver.find_element(By.XPATH,'/html/body/div[1]/main/div/div/div/div[1]/div[4]/div/form/div/div').text
            info = str(inf)
            txt = info.split(' ')
            num = int(txt[5])
            print(num)
            pag = num / 30
            tot = math.ceil(pag)
        except:
            tot = 1



        print(F'CRAWLING... {prodformat} : {tot}')

        match tot:
            case 1:
                
                itens = scraw(driver, wait)

                for item in itens:
                    post(prodformat, item)

            case 2:
                itens = scraw(driver, wait)
                for item in itens:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)

                itens2 = scraw(driver, wait)
                for item in itens2:
                    post(prodformat, item)
                


            case 3:
                itens = scraw(driver, wait)
                for item in itens:
                    post(prodformat, item)


                sleep(1)
                page(driver, wait)
                sleep(1)
                itens2 = scraw(driver, wait)
                for item in itens2:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens3 = scraw(driver, wait)
                for item in itens3:
                    post(prodformat, item)


            case 4:
                itens = scraw(driver, wait)
                for item in itens:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                sleep(1)
                itens2 = scraw(driver, wait)
                for item in itens2:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                sleep(1)
                itens3 = scraw(driver, wait)
                for item in itens3:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens4 = scraw(driver, wait)
                for item in itens4:
                    post(prodformat, item)


            case 5:
                itens = scraw(driver, wait)
                for item in itens:
                    post(prodformat, item)


                sleep(1)
                page(driver, wait)
                sleep(1)
                itens2 = scraw(driver, wait)
                for item in itens2:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens3 = scraw(driver, wait)
                for item in itens3:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens4 = scraw(driver, wait)
                for item in itens4:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens5 = scraw(driver, wait)
                for item in itens5:
                    post(prodformat, item)

                    
            case 6:
                itens = scraw(driver, wait)
                for item in itens:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                sleep(1)
                itens2 = scraw(driver, wait)
                for item in itens2:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens3 = scraw(driver, wait)
                for item in itens2:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens4 = scraw(driver, wait)
                for item in itens4:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens5 = scraw(driver, wait)
                for item in itens5:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens6 = scraw(driver, wait)
                for item in itens6:
                    post(prodformat, item)


            case 7:
                itens = scraw(driver, wait)
                for item in itens:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                sleep(1)
                itens2 = scraw(driver, wait)
                for item in itens2:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens3 = scraw(driver, wait)
                for item in itens3:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens4 = scraw(driver, wait)
                for item in itens4:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens5 = scraw(driver, wait)
                for item in itens5:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens6 = scraw(driver, wait)
                for item in itens6:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens7 = scraw(driver, wait)
                for item in itens7:
                    post(prodformat, item)


            case 8:
                itens = scraw(driver, wait)
                for item in itens:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                sleep(1)
                itens2 = scraw(driver, wait)
                for item in itens2:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens3 = scraw(driver, wait)
                for item in itens3:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens4 = scraw(driver, wait)
                for item in itens4:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens5 = scraw(driver, wait)
                for item in itens5:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens6 = scraw(driver, wait)
                for item in itens6:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens7 = scraw(driver, wait)
                for item in itens7:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens8 = scraw(driver, wait)
                for item in itens8:
                    post(prodformat, item)


            case 9:
                itens = scraw(driver, wait)
                for item in itens:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                sleep(1)
                itens2 = scraw(driver, wait)
                for item in itens2:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens3 = scraw(driver, wait)
                for item in itens3:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens4 = scraw(driver, wait)
                for item in itens4:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens5 = scraw(driver, wait)
                for item in itens5:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens6 = scraw(driver, wait)
                for item in itens6:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens7 = scraw(driver, wait)
                for item in itens7:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens8 = scraw(driver, wait)
                for item in itens8:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens9 = scraw(driver, wait)
                for item in itens9:
                    post(prodformat, item)


            case 10:
                itens = scraw(driver, wait)
                for item in itens:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                sleep(1)
                itens2 = scraw(driver, wait)
                for item in itens2:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens3 = scraw(driver, wait)
                for item in itens3:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens4 = scraw(driver, wait)
                for item in itens4:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens5 = scraw(driver, wait)
                for item in itens5:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens6 = scraw(driver, wait)
                for item in itens6:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens7 = scraw(driver, wait)
                for item in itens7:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens8 = scraw(driver, wait)
                for item in itens8:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens9 = scraw(driver, wait)
                for item in itens9:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens10 = scraw(driver, wait)
                for item in itens10:
                    post(prodformat, item)


            case 11:
                itens = scraw(driver, wait)
                for item in itens:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                sleep(1)
                itens2 = scraw(driver, wait)
                for item in itens2:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens3 = scraw(driver, wait)
                for item in itens3:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens4 = scraw(driver, wait)
                for item in itens4:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens5 = scraw(driver, wait)
                for item in itens5:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens6 = scraw(driver, wait)
                for item in itens6:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens7 = scraw(driver, wait)
                for item in itens7:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens8 = scraw(driver, wait)
                for item in itens8:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens9 = scraw(driver, wait)
                for item in itens9:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens10 = scraw(driver, wait)
                for item in itens10:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens11 = scraw(driver, wait)
                for item in itens11:
                    post(prodformat, item)


            case 12:
                itens = scraw(driver, wait)
                for item in itens:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                sleep(1)
                itens2 = scraw(driver, wait)
                for item in itens2:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens3 = scraw(driver, wait)
                for item in itens3:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens4 = scraw(driver, wait)
                for item in itens4:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens5 = scraw(driver, wait)
                for item in itens5:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens6 = scraw(driver, wait)
                for item in itens6:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens7 = scraw(driver, wait)
                for item in itens7:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens8 = scraw(driver, wait)
                for item in itens8:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens9 = scraw(driver, wait)
                for item in itens9:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens10 = scraw(driver, wait)
                for item in itens10:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens11 = scraw(driver, wait)
                for item in itens11:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens12 = scraw(driver, wait)
                for item in itens12:
                    post(prodformat, item)


            case 13:
                itens = scraw(driver, wait)
                for item in itens:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                sleep(1)
                itens2 = scraw(driver, wait)
                for item in itens2:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens3 = scraw(driver, wait)
                for item in itens3:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens4 = scraw(driver, wait)
                for item in itens4:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens5 = scraw(driver, wait)
                for item in itens5:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens6 = scraw(driver, wait)
                for item in itens6:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens7 = scraw(driver, wait)
                for item in itens7:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens8 = scraw(driver, wait)
                for item in itens8:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens9 = scraw(driver, wait)
                for item in itens9:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens10 = scraw(driver, wait)
                for item in itens10:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens11 = scraw(driver, wait)
                for item in itens11:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens12 = scraw(driver, wait)
                for item in itens12:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens13 = scraw(driver, wait)
                for item in itens13:
                    post(prodformat, item)


            case 14:
                itens = scraw(driver, wait)
                for item in itens:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                sleep(1)
                itens2 = scraw(driver, wait)
                for item in itens2:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens3 = scraw(driver, wait)
                for item in itens3:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens4 = scraw(driver, wait)
                for item in itens4:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens5 = scraw(driver, wait)
                for item in itens5:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens6 = scraw(driver, wait)
                for item in itens6:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens7 = scraw(driver, wait)
                for item in itens7:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens8 = scraw(driver, wait)
                for item in itens8:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens9 = scraw(driver, wait)
                for item in itens9:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens10 = scraw(driver, wait)
                for item in itens10:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens11 = scraw(driver, wait)
                for item in itens11:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens12 = scraw(driver, wait)
                for item in itens12:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens14 = scraw(driver, wait)
                for item in itens14:
                    post(prodformat, item)


            case 15:
                itens = scraw(driver, wait)
                for item in itens:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                sleep(1)
                itens2 = scraw(driver, wait)
                for item in itens2:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens3 = scraw(driver, wait)
                for item in itens3:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens4 = scraw(driver, wait)
                for item in itens4:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens5 = scraw(driver, wait)
                for item in itens5:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens6 = scraw(driver, wait)
                for item in itens6:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens7 = scraw(driver, wait)
                for item in itens7:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens8 = scraw(driver, wait)
                for item in itens8:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens9 = scraw(driver, wait)
                for item in itens9:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens10 = scraw(driver, wait)
                for item in itens10:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens11 = scraw(driver, wait)
                for item in itens11:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens12 = scraw(driver, wait)
                for item in itens12:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens14 = scraw(driver, wait)
                for item in itens14:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens15 = scraw(driver, wait)
                for item in itens15:
                    post(prodformat, item)


            case 16:
                itens = scraw(driver, wait)
                for item in itens:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                sleep(1)
                itens2 = scraw(driver, wait)
                for item in itens2:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens3 = scraw(driver, wait)
                for item in itens3:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens4 = scraw(driver, wait)
                for item in itens4:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens5 = scraw(driver, wait)
                for item in itens5:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens6 = scraw(driver, wait)
                for item in itens6:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens7 = scraw(driver, wait)
                for item in itens7:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens8 = scraw(driver, wait)
                for item in itens8:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens9 = scraw(driver, wait)
                for item in itens9:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens10 = scraw(driver, wait)
                for item in itens10:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens11 = scraw(driver, wait)
                for item in itens11:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens12 = scraw(driver, wait)
                for item in itens12:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens14 = scraw(driver, wait)
                for item in itens14:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens15 = scraw(driver, wait)
                for item in itens15:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens16 = scraw(driver, wait)
                for item in itens16:
                    post(prodformat, item)


            case 17:
                itens = scraw(driver, wait)
                for item in itens:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                sleep(1)
                itens2 = scraw(driver, wait)
                for item in itens2:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens3 = scraw(driver, wait)
                for item in itens3:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens4 = scraw(driver, wait)
                for item in itens4:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens5 = scraw(driver, wait)
                for item in itens5:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens6 = scraw(driver, wait)
                for item in itens6:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens7 = scraw(driver, wait)
                for item in itens7:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens8 = scraw(driver, wait)
                for item in itens8:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens9 = scraw(driver, wait)
                for item in itens9:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens10 = scraw(driver, wait)
                for item in itens10:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens11 = scraw(driver, wait)
                for item in itens11:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens12 = scraw(driver, wait)
                for item in itens12:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens14 = scraw(driver, wait)
                for item in itens14:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens15 = scraw(driver, wait)
                for item in itens15:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens16 = scraw(driver, wait)
                for item in itens16:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens17 = scraw(driver, wait)
                for item in itens17:
                    post(prodformat, item)


            case 18:
                itens = scraw(driver, wait)
                for item in itens:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                sleep(1)
                itens2 = scraw(driver, wait)
                for item in itens2:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens3 = scraw(driver, wait)
                for item in itens3:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens4 = scraw(driver, wait)
                for item in itens4:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens5 = scraw(driver, wait)
                for item in itens5:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens6 = scraw(driver, wait)
                for item in itens6:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens7 = scraw(driver, wait)
                for item in itens7:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens8 = scraw(driver, wait)
                for item in itens8:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens9 = scraw(driver, wait)
                for item in itens9:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens10 = scraw(driver, wait)
                for item in itens10:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens11 = scraw(driver, wait)
                for item in itens11:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens12 = scraw(driver, wait)
                for item in itens12:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens14 = scraw(driver, wait)
                for item in itens14:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens15 = scraw(driver, wait)
                for item in itens15:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens16 = scraw(driver, wait)
                for item in itens16:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens17 = scraw(driver, wait)
                for item in itens17:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens18 = scraw(driver, wait)
                for item in itens18:
                    post(prodformat, item)


            case 19:
                itens = scraw(driver, wait)
                for item in itens:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)

                itens2 = scraw(driver, wait)
                for item in itens2:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)

                itens3 = scraw(driver, wait)
                for item in itens3:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)

                itens4 = scraw(driver, wait)
                for item in itens4:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)

                itens5 = scraw(driver, wait)
                for item in itens5:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)

                itens6 = scraw(driver, wait)
                for item in itens6:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)

                itens7 = scraw(driver, wait)
                for item in itens7:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)

                itens8 = scraw(driver, wait)
                for item in itens8:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)

                itens9 = scraw(driver, wait)
                for item in itens9:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
   
                itens10 = scraw(driver, wait)
                for item in itens10:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)

                itens11 = scraw(driver, wait)
                for item in itens11:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)

                itens12 = scraw(driver, wait)
                for item in itens12:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)

                itens14 = scraw(driver, wait)
                for item in itens14:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)

                itens15 = scraw(driver, wait)
                for item in itens15:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)

                itens16 = scraw(driver, wait)
                for item in itens16:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)

                itens17 = scraw(driver, wait)
                for item in itens17:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens18 = scraw(driver, wait)
                for item in itens18:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                driver.execute_script('window.scrollTo(0, 1700);')

                itens19 = scraw(driver, wait)
                for item in itens19:
                    post(prodformat, item)


            case 20:
                itens = scraw(driver, wait)
                for item in itens:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                sleep(1)
                itens2 = scraw(driver, wait)
                for item in itens2:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens3 = scraw(driver, wait)
                for item in itens3:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens4 = scraw(driver, wait)
                for item in itens4:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens5 = scraw(driver, wait)
                for item in itens5:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens6 = scraw(driver, wait)
                for item in itens6:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens7 = scraw(driver, wait)
                for item in itens7:
                    post(prodformat, item)


                sleep(1)
                page(driver, wait)
                itens8 = scraw(driver, wait)
                for item in itens8:
                    post(prodformat, item)

 
                sleep(1)
                page(driver, wait)
                itens9 = scraw(driver, wait)
                for item in itens9:
                    post(prodformat, item)


                sleep(1)
                page(driver, wait)
                itens10 = scraw(driver, wait)
                for item in itens10:
                    post(prodformat, item)


                sleep(1)
                page(driver, wait)
                itens11 = scraw(driver, wait)
                for item in itens11:
                    post(prodformat, item)


                sleep(1)
                page(driver, wait)
                itens12 = scraw(driver, wait)
                for item in itens12:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens14 = scraw(driver, wait)
                for item in itens14:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens15 = scraw(driver, wait)
                for item in itens15:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens16 = scraw(driver, wait)
                for item in itens16:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens17 = scraw(driver, wait)
                for item in itens17:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens18 = scraw(driver, wait)
                for item in itens18:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens19 = scraw(driver, wait)
                for item in itens19:
                    post(prodformat, item)

                sleep(1)
                page(driver, wait)
                itens20 = scraw(driver, wait)
                for item in itens20:
                    post(prodformat, item)




def crawlAlface():

    driver, wait = iniciar_driver()

    driver.get('https://www.noticiasagricolas.com.br/cotacoes/verduras/alface-ceasas')

    texto = driver.find_element(By.XPATH,'//*[@id="content"]/div[3]/div[3]/div[1]/div[1]/div').text
    data_cotacao = texto.split(' ')
    dia_c = data_cotacao[1]
    dia_cotacao = f'{dia_c[2]}-{dia_c[1]}-{dia_c[0]}'

    tabela1 = driver.find_element(By.XPATH,'//*[@id="content"]/div[3]/div[3]/div[1]/div[2]/table')
    html_tabela1 = tabela1.get_attribute('outerHTML')
    sleep(2)

    soup1 = BeautifulSoup(html_tabela1, 'html.parser')
    table1 = soup1.find(name='table')

    df_alface = pd.read_html( str(table1) ) [0]
    sleep(1)

    itens = []

    for i, item in enumerate(df_alface['Tipo / Unidade medida']):
        produto = df_alface.loc[i, "Tipo / Unidade medida"]
        prec = df_alface.loc[i, "Preço"]
        if prec == '***':
            preco = 0
        else:
            if len(prec) == 3:
                x = slice(1)
                y = slice(1,3)

                real = prec[x]
                cent = prec[y]
                preco = f'{real},{cent}'
            else:
                x = slice(2)
                y = slice(2,4)

                real = prec[x]
                cent = prec[y]
                preco = f'{real},{cent}'

            
        itens.append({
            "item": produto, 
            "valor": preco
            })

            
    linha1 = itens[0]
    linha2 = itens[1]
    linha3 = itens[2]
    linha4 = itens[3]
    linha5 = itens[4]
    linha6 = itens[5]
    linha7 = itens[6]
    linha8 = itens[7]
    linha9 = itens[8]

    dados= []


    estado1 = linha1['item']

    item1 = linha2['item']
    preco1 = linha2['valor']

    item2 = linha3['item']
    preco2 = linha3['valor']

    dados.append({
        "Produto": item1,
        "Estado": estado1,
        "Preco": preco1,
        "Data": data_hoje
    })

    dados.append({
        "Produto": item2,
        "Estado": estado1,
        "Preco": preco2,
        "Data": data_hoje
    })


    estado2 = linha4['item']

    item3 = linha5['item']
    preco3 = linha5['valor']

    item4 = linha6['item']
    preco4 = linha6['valor']

    dados.append({
        "Produto": item3,
        "Estado": estado2,
        "Preco": preco3,
        "Data": data_hoje
    })

    dados.append({
        "Produto": item4,
        "Estado": estado2,
        "Preco": preco4,
        "Data": data_hoje
    })


    estado3 = linha7['item']

    item5 = linha8['item']
    preco5 = linha8['valor']

    item6 = linha9['item']
    preco6 = linha9['valor']

    dados.append({
        "Produto": item6,
        "Estado": estado3,
        "Preco": preco6,
        "Data": data_hoje
    })

    dados.append({
        "Produto": item5,
        "Estado": estado3,
        "Preco": preco5,
        "Data": data_hoje
    })

    driver.close()

    for dado in dados:
        if dado['Preco'] == 's/, c':
            dado['Preco'] = 'Sem cotacao'

        data = {
            'Produto': dado["Produto"],
            'Local': dado["Estado"],
            'Preco': dado["Preco"],
            'Update': dado["Data"],
            'Data': dado["Data"]
        }


        post('alface',data)


def crawlRepolho():

    driver, wait = iniciar_driver()

    driver.get('https://www.noticiasagricolas.com.br/cotacoes/verduras/repolho-ceasas')


    tabela1 = driver.find_element(By.XPATH,'//*[@id="content"]/div[3]/div[3]/div[1]/div[2]/table')
    html_tabela1 = tabela1.get_attribute('outerHTML')
    sleep(2)

    soup1 = BeautifulSoup(html_tabela1, 'html.parser')
    table1 = soup1.find(name='table')

    df_repolho = pd.read_html( str(table1) ) [0]
    sleep(1)

    itens = []

    for i, item in enumerate(df_repolho['Tipo / Unidade medida']):
        produto = df_repolho.loc[i, "Tipo / Unidade medida"]
        prec = df_repolho.loc[i, "Preço"]
        if prec == '***':
            preco = 0
        else:
            if len(prec) == 3:
                x = slice(1)
                y = slice(1,3)

                real = prec[x]
                cent = prec[y]
                preco = f'{real},{cent}'
            else:
                x = slice(2)
                y = slice(2,4)

                real = prec[x]
                cent = prec[y]
                preco = f'{real},{cent}'

            
        itens.append({
            "item": produto, 
            "valor": preco
        })

            
    linha1 = itens[0]
    linha2 = itens[1]
    linha3 = itens[2]
    linha4 = itens[3]
    linha5 = itens[4]
    linha6 = itens[5]
    linha7 = itens[6]
    linha8 = itens[7]

    dados= []


    estado1 = linha1['item']

    item1 = linha2['item']
    preco1 = linha2['valor']

    item2 = linha3['item']
    preco2 = linha3['valor']

    dados.append({
        "Produto": item1,
        "Estado": estado1,
        "Preco": preco1,
        "Data": data_hoje
    })

    dados.append({
        "Produto": item2,
        "Estado": estado1,
        "Preco": preco2,
        "Data": data_hoje
    })


    estado2 = linha4['item']

    item3 = linha5['item']
    preco3 = linha5['valor']

    dados.append({
        "Produto": item3,
        "Estado": estado2,
        "Preco": preco3,
        "Data": data_hoje
    })


    estado3 = linha6['item']

    item4 = linha7['item']
    preco4 = linha7['valor']

    item5 = linha8['item']
    preco5 = linha8['valor']
    
    dados.append({
        "Produto": item4,
        "Estado": estado3,
        "Preco": preco4,
        "Data": data_hoje
    })

    dados.append({
        "Produto": item5,
        "Estado": estado3,
        "Preco": preco5,
        "Data": data_hoje
    })

    driver.close()

    for dado in dados:
        if dado['Preco'] == 's/, c':
            dado['Preco'] = 'Sem cotacao'

        data = {
            'Produto': dado["Produto"],
            'Local': dado["Estado"],
            'Preco': dado["Preco"],
            'Update': dado["Data"],
            'Data': dado["Data"]
        }

        post('repolho',data)

       
def scrap_preco():

    print('CRAWLER PRICES')
    codigos = [{'11,8,Todos,algodao'},{'13,5,Todos,arroz'},{'11,30,Todos,amendoim'},{'13,7,Todos,cafe'},{'11,92,Todos,cana'},{'13,46,Todos,feijao'},{'13,2,Todos,milho'},{'13,1,Todos,soja'},{'13,31,Todos,sorgo'},{'13,6,Todos,trigo'},{'10,144,Todos,suinos'},{'10,122,Todos,aves'},{'10,147,Todos,caprinos'},{'10,152,Todos,ovinos'},{'14,95,Todos,beterraba'},{'14,40,Todos,tomate'},{'14,51,Todos,pimentao'},{'11,24,Todos,cebola'},{'14,39,Todos,couve'},{'14,27,Todos,cenoura'},{'10,120,Boi Gordo 15Kg,boi'},{'10,120,Vaca Gorda 15Kg,vaca'}]

    

    driver,wait = iniciar_driver()

    login(driver)
    sleep(1)

    for cod in codigos:

        item = str(cod)
        it = item.split(',')

        grp = it[0].split("'")
        itemgrupo = grp[1]
        itemespecie = it[1]
        itemproduto = it[2]
        fmt = it[3].split("'")
        prodformat = fmt[0]
        crawler(driver,wait,prodformat)
        sleep(1)

        

    driver.close()


def send_mail():
    sender_email = "meuclash3333@gmail.com"
    sender_password = "mqzm swld bzsa hjau"
    recipient_email = "mayconclementino44@gmail.com"
    subject = "SUPORTE - DEV"
    body = "BUG APP AGROLIVRE - CRAWLER PRICES"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Send the email
    smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_server.starttls()
    smtp_server.login(sender_email, sender_password)
    smtp_server.sendmail(sender_email, recipient_email, msg.as_string())
    smtp_server.quit()




def scrapy_precos():
    try:
        scrap_preco()
        sleep(1)
        crawlAlface()
        sleep(1)
        crawlRepolho() 

    except:
        send_mail()
        


scrap_preco()

schedule.every().day.at("05:30").do(scrapy_precos)


while True:
    schedule.run_pending()
    sleep(1)