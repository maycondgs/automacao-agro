from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
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

    
dda = datetime.today()
da = str(dda).split(' ')
dataa = da[0].split('-')

header = {
    'Content-Type': 'application/json'
    }



links = ['https://www.agrolink.com.br/noticias/categoria/agricultura/lista','https://www.agrolink.com.br/noticias/categoria/pecuaria/lista', 'https://www.agrolink.com.br/noticias/categoria/economia/lista','https://www.agrolink.com.br/noticias/categoria/politica/lista', 'https://www.agrolink.com.br/noticias/categoria/tecnologia/lista',]


for link in links:
    lnnk = link.split('/')
    categoria = lnnk[5]
    referencia = 'agrolink'
        
    page = requests.get(link)

    soup = BeautifulSoup(page.content, 'html.parser')

    dom = etree.HTML(str(soup))


    links2 = (dom.xpath('//*[@id="content"]/div/div/div[3]/div[1]/div[2]/div/div[1]/div[2]/div[1]/h3/a/@href'))
    titulo = (dom.xpath('//*[@id="content"]/div/div/div[3]/div[1]/div[2]/div/div[1]/div[2]/div[1]/h3/a/text()'))
    datt = (dom.xpath('//*[@id="content"]/div/div/div[3]/div[1]/div[2]/div/div[1]/div[2]/div[2]/ul/li[2]/small/text()'))

    lnks2 = []
    data = []
    hora = []
        

    for da in datt:
        dattt = da.split(' ')
        data.append(dattt[0])
        hora.append(dattt[1])

    for lnk in links2:
        lnks2.append(f'https://www.agrolink.com.br{lnk}')

    novos = []

    for titu, link, data, hora in zip(titulo, lnks2, data, hora):     
        novos.append([titu, link, hora, data, referencia, categoria])

    bd = requests.get(f'https://api-cotacoes.agrolivrebrasil.com/noticias/agrolink/{categoria}')

    tb = json.loads(bd.content)

    for novo in novos:
        if novo not in tb:
            payl = {
                "Titulo": novo[0],
                "Link": novo[1],
                "Hora": novo[2],
                "Data": novo[3],
                "Referencia": novo[4],
                "Categoria" : novo[5]
            }

            st = json.dumps(payl)
            
            requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/noticias/agrolink', headers=header, data=st)


