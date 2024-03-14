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

    service = Service(executable_path='/automacao-agro/venv/bin/chromedriver')

    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--no-sandbox')


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



def login(driver):

    driver.get('https://www.agrolink.com.br/login')
    sleep(2)

    driver.execute_script('window.scrollTo(0, 310);')
    sleep(1)

    driver.find_element(By.XPATH,'/html/body/div[1]/main/div[2]/div/div/div/section[1]/div/div/form/div[1]/div[2]/input').send_keys('xetedo9314@ratedane.com')
    sleep(2)
    driver.find_element(By.XPATH,'/html/body/div[1]/main/div[2]/div/div/div/section[1]/div/div/form/div[2]/div[2]/input').send_keys('webscraper')

    driver.find_element(By.XPATH,'/html/body/div[1]/main/div[2]/div/div/div/section[1]/div/div/form/div[3]/button').click()



def busca(driver,wait, itemgrupo, itemespecie, itemproduto):

    driver.get('https://www.agrolink.com.br/cotacoes/busca')
    sleep(1)

    driver.execute_script('window.scrollTo(0, 270);')
    sleep(1)

    match itemgrupo:
        case 10:
            grupoo = 'Carnes'
        case 11:
            grupoo = 'Diversos'
        case 13:
            grupoo = 'Grãos'
        case 14:
            grupoo = 'Hortaliças'

    
    grupo = wait.until(condicao_esperada.element_to_be_clickable((By.XPATH,'//select[@id="FiltroCotacoesGrupo"]')))
    sleep(2)
    grupos = Select(grupo)
    sleep(2)
    try:
        grupos.select_by_value(itemgrupo)
        sleep(1)
    except:
        grupos.select_by_visible_text(grupoo)
        sleep(1)

    especie = wait.until(condicao_esperada.element_to_be_clickable((By.XPATH,'//select[@id="FiltroCotacoesEspecie"]')))
    sleep(2)
    especies = Select(especie)
    sleep(2)

    especiees = ''

    match itemespecie:
        case 122:
            especiees = 'Aves'
        case 120:
            especiees = 'Bovinos'
        case 147:
            especiees = 'Caprinos'
        case 152:
            especiees = 'Ovinos'
        case 144:
            especiees = 'Suínos'
        case 673:
            especies = 'Açúcar'
        case 8:
            especiees = 'Algodão'
        case 30:
            especiees = 'Amendoim'
        case 92:
            especiees = 'Cana-de-açúcar'
        case 24:
            especiees = 'Cebola'
        case 5:
            especiees = 'Arroz'
        case 7:
            especiees = 'Café'
        case 46:
            especiees = 'Feijão'
        case 2:
            especiees = 'Milho'
        case 1:
            especiees = 'Soja'
        case 31:
            especiees = 'Sorgo'
        case 6:
            especiees = 'Trigo'
        case 95:
            especiees = 'Beterraba'
        case 27:
            especiees = 'Cenoura'
        case 39:
            especiees = 'Couve'
        case 51:
            especiees = 'Pimentão'
        case 40:
            especiees = 'Tomate'
    

    try:
        especies.select_by_value(itemespecie)
        sleep(1)
    except:
        especies.select_by_visible_text(especiees)
    
    sleep(1)
    produto = wait.until(condicao_esperada.element_to_be_clickable((By.XPATH,'//select[@id="FiltroCotacoesProduto"]')))
    sleep(2)
    produtos = Select(produto)
    sleep(1)

    try:
        produtos.select_by_visible_text(itemproduto)
        sleep(1)
    except:
        busca(driver,wait, itemgrupo, itemespecie, itemproduto)

    sleep(4)

    driver.execute_script('window.scrollTo(0, 300);')
    sleep(2)
    
    dattaa = wait.until(condicao_esperada.element_to_be_clickable((By.XPATH,'//*[@id="DataInicial"]')))
    dattaa.click()
    sleep(2)
    

    try:
        wait.until(condicao_esperada.element_to_be_clickable((By.XPATH,'//th[@class="today"]'))).click()
        sleep(3)

    except:
        return


    wait.until(condicao_esperada.element_to_be_clickable((By.XPATH,'//*[@id="btnEnviarFiltroGeral-5231"]'))).click()
    sleep(1)



def scraw(driver, wait):

    itens = []
    sleep(3)

    produtos = wait.until(condicao_esperada.visibility_of_all_elements_located((By.XPATH, '//*[@id="app"]/div[1]/main/div/div/div/div[1]/div[4]/div/div/div/table/tbody/tr/td[1]')))
    produtos = produtos[1:]

    products = []
    locals = []

    for produto in produtos:
        produto_texto = produto.text
        prodd = produto_texto.split('\n')

        local = prodd[1]

        if "'" in local:
            local = local.replace("'", "")
        
        products.append(prodd[0])
        locals.append(local)

    

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

    for product, locale, price in  zip(products, locals, precos):

        data.append({
            'Produto': product,
            'Local': locale,
            'Preco': price,
            'Data': data_hoje
        })



    return data



def page(driver, wait):
    driver.execute_script('window.scrollTo(0, 1250);')
    sleep(5)
    next_btn = wait.until(condicao_esperada.element_to_be_clickable((By.XPATH, '//*[@class="btn-navigation btn-navigation-next"]'))).click()



def post(itemarq, item):

    cursor = db.cursor()
    sql = f"INSERT INTO quotes_{itemarq} (name, state, price, date_publication) VALUES ('{item['Produto']}', '{item['Local']}', '{item['Preco']}', '{item['Data']}')"
    cursor.execute(sql)
    db.commit()


def crawler(driver,wait,itemgrupo,itemespecie,itemproduto,prodformat):
    
    busca(driver,wait, itemgrupo, itemespecie, itemproduto)

    driver.execute_script('window.scrollTo(0, 2200);')

    try:
        inf = driver.find_element(By.XPATH,'/html/body/div[1]/main/div/div/div/div[1]/div[4]/div/form/div/div').text
        info = str(inf)

        txt = info.split(' ')
        num = int(txt[5])
        pag = num / 30
        tot = math.ceil(pag)
    except:
        tot = 1

    match tot:
        case 1:
            itens = scraw(driver, wait)

            for item in itens:
                post(prodformat, item)

        case 2:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver, wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)
            


        case 3:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)


            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)


        case 4:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            sleep(1)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)


        case 5:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)


            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

                
        case 6:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            itens3 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens6 = scraw(driver, wait)
            for item in itens6:
                post(prodformat, item)


        case 7:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens6 = scraw(driver, wait)
            for item in itens6:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens7 = scraw(driver, wait)
            for item in itens7:
                post(prodformat, item)


        case 8:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens6 = scraw(driver, wait)
            for item in itens6:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens7 = scraw(driver, wait)
            for item in itens7:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens8 = scraw(driver, wait)
            for item in itens8:
                post(prodformat, item)


        case 9:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens6 = scraw(driver, wait)
            for item in itens6:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens7 = scraw(driver, wait)
            for item in itens7:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens8 = scraw(driver, wait)
            for item in itens8:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens9 = scraw(driver, wait)
            for item in itens9:
                post(prodformat, item)


        case 10:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens6 = scraw(driver, wait)
            for item in itens6:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens7 = scraw(driver, wait)
            for item in itens7:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens8 = scraw(driver, wait)
            for item in itens8:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens9 = scraw(driver, wait)
            for item in itens9:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens10 = scraw(driver, wait)
            for item in itens10:
                post(prodformat, item)


        case 11:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens6 = scraw(driver, wait)
            for item in itens6:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens7 = scraw(driver, wait)
            for item in itens7:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens8 = scraw(driver, wait)
            for item in itens8:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens9 = scraw(driver, wait)
            for item in itens9:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens10 = scraw(driver, wait)
            for item in itens10:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens11 = scraw(driver, wait)
            for item in itens11:
                post(prodformat, item)


        case 12:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens6 = scraw(driver, wait)
            for item in itens6:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens7 = scraw(driver, wait)
            for item in itens7:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens8 = scraw(driver, wait)
            for item in itens8:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens9 = scraw(driver, wait)
            for item in itens9:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens10 = scraw(driver, wait)
            for item in itens10:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens11 = scraw(driver, wait)
            for item in itens11:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens12 = scraw(driver, wait)
            for item in itens12:
                post(prodformat, item)


        case 13:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens6 = scraw(driver, wait)
            for item in itens6:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens7 = scraw(driver, wait)
            for item in itens7:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens8 = scraw(driver, wait)
            for item in itens8:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens9 = scraw(driver, wait)
            for item in itens9:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens10 = scraw(driver, wait)
            for item in itens10:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens11 = scraw(driver, wait)
            for item in itens11:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens12 = scraw(driver, wait)
            for item in itens12:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens13 = scraw(driver, wait)
            for item in itens13:
                post(prodformat, item)


        case 14:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens6 = scraw(driver, wait)
            for item in itens6:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens7 = scraw(driver, wait)
            for item in itens7:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens8 = scraw(driver, wait)
            for item in itens8:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens9 = scraw(driver, wait)
            for item in itens9:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens10 = scraw(driver, wait)
            for item in itens10:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens11 = scraw(driver, wait)
            for item in itens11:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens12 = scraw(driver, wait)
            for item in itens12:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens14 = scraw(driver, wait)
            for item in itens14:
                post(prodformat, item)


        case 15:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens6 = scraw(driver, wait)
            for item in itens6:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens7 = scraw(driver, wait)
            for item in itens7:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens8 = scraw(driver, wait)
            for item in itens8:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens9 = scraw(driver, wait)
            for item in itens9:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens10 = scraw(driver, wait)
            for item in itens10:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens11 = scraw(driver, wait)
            for item in itens11:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens12 = scraw(driver, wait)
            for item in itens12:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens14 = scraw(driver, wait)
            for item in itens14:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens15 = scraw(driver, wait)
            for item in itens15:
                post(prodformat, item)


        case 16:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens6 = scraw(driver, wait)
            for item in itens6:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens7 = scraw(driver, wait)
            for item in itens7:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens8 = scraw(driver, wait)
            for item in itens8:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens9 = scraw(driver, wait)
            for item in itens9:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens10 = scraw(driver, wait)
            for item in itens10:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens11 = scraw(driver, wait)
            for item in itens11:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens12 = scraw(driver, wait)
            for item in itens12:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens14 = scraw(driver, wait)
            for item in itens14:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens15 = scraw(driver, wait)
            for item in itens15:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens16 = scraw(driver, wait)
            for item in itens16:
                post(prodformat, item)


        case 17:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens6 = scraw(driver, wait)
            for item in itens6:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens7 = scraw(driver, wait)
            for item in itens7:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens8 = scraw(driver, wait)
            for item in itens8:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens9 = scraw(driver, wait)
            for item in itens9:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens10 = scraw(driver, wait)
            for item in itens10:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens11 = scraw(driver, wait)
            for item in itens11:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens12 = scraw(driver, wait)
            for item in itens12:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens14 = scraw(driver, wait)
            for item in itens14:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens15 = scraw(driver, wait)
            for item in itens15:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens16 = scraw(driver, wait)
            for item in itens16:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens17 = scraw(driver, wait)
            for item in itens17:
                post(prodformat, item)


        case 18:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens6 = scraw(driver, wait)
            for item in itens6:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens7 = scraw(driver, wait)
            for item in itens7:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens8 = scraw(driver, wait)
            for item in itens8:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens9 = scraw(driver, wait)
            for item in itens9:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens10 = scraw(driver, wait)
            for item in itens10:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens11 = scraw(driver, wait)
            for item in itens11:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens12 = scraw(driver, wait)
            for item in itens12:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens14 = scraw(driver, wait)
            for item in itens14:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens15 = scraw(driver, wait)
            for item in itens15:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens16 = scraw(driver, wait)
            for item in itens16:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens17 = scraw(driver, wait)
            for item in itens17:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens18 = scraw(driver, wait)
            for item in itens18:
                post(prodformat, item)


        case 19:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens6 = scraw(driver, wait)
            for item in itens6:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens7 = scraw(driver, wait)
            for item in itens7:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens8 = scraw(driver, wait)
            for item in itens8:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens9 = scraw(driver, wait)
            for item in itens9:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens10 = scraw(driver, wait)
            for item in itens10:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens11 = scraw(driver, wait)
            for item in itens11:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens12 = scraw(driver, wait)
            for item in itens12:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens14 = scraw(driver, wait)
            for item in itens14:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens15 = scraw(driver, wait)
            for item in itens15:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens16 = scraw(driver, wait)
            for item in itens16:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens17 = scraw(driver, wait)
            for item in itens17:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens18 = scraw(driver, wait)
            for item in itens18:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens19 = scraw(driver, wait)
            for item in itens19:
                post(prodformat, item)


        case 20:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens6 = scraw(driver, wait)
            for item in itens6:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens7 = scraw(driver, wait)
            for item in itens7:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens8 = scraw(driver, wait)
            for item in itens8:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens9 = scraw(driver, wait)
            for item in itens9:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens10 = scraw(driver, wait)
            for item in itens10:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens11 = scraw(driver, wait)
            for item in itens11:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens12 = scraw(driver, wait)
            for item in itens12:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens14 = scraw(driver, wait)
            for item in itens14:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens15 = scraw(driver, wait)
            for item in itens15:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens16 = scraw(driver, wait)
            for item in itens16:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens17 = scraw(driver, wait)
            for item in itens17:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens18 = scraw(driver, wait)
            for item in itens18:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            itens19 = scraw(driver, wait)
            for item in itens19:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
            page(driver, wait)
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
        post('alface',dado)


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
        post('repolho',dado)


       
def scrap_preco():

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
        print(f"Scraping : {prodformat}")
        crawler(driver,wait,itemgrupo,itemespecie,itemproduto,prodformat)
        sleep(1)

        

    driver.close()




def scrapy_precos():
   
    print('CRAWLER PRECOS')
    scrap_preco()
    sleep(1)
    crawlAlface()
    sleep(1)
    crawlRepolho() 

    




scrapy_precos()

#schedule.every().day.at("06:30").do(scrapy_precos)


#while True:
#    schedule.run_pending()
#    sleep(1)