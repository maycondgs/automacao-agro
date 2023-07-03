from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from datetime import datetime
from lxml import etree
import pytesseract
import cv2
import json
import requests

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


dda = datetime.today()
da = str(dda).split(' ')
dataa = da[0].split('-')

data_hoje = f'{dataa[2]}/{dataa[1]}/{dataa[0]}'


def iniciar_driver():
    chrome_options = Options()
    arguments = ['--lang=pt-BR', '--window-size=800,600', '--incognito']
    for argument in arguments:
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1,

    })
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=chrome_options)

    return driver


ufs = ['MT']


driver = iniciar_driver()

def login():

    driver.get('https://www.agrolink.com.br/login')
    sleep(2)

    driver.execute_script('window.scrollTo(0, 310);')
    sleep(1)

    driver.find_element(By.XPATH,'/html/body/div[1]/section/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/div/form[1]/div/div[1]/input').send_keys('xetedo9314@ratedane.com')
    sleep(2)
    driver.find_element(By.XPATH,'/html/body/div[1]/section/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/div/form[1]/div/div[2]/input').send_keys('webscraper')

    driver.find_element(By.XPATH,'/html/body/div[1]/section/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/div/form[1]/div/div[3]/button').click()

    
login()
sleep(1)

itens = []

for uf in ufs:

    driver.get('https://www.agrolink.com.br/cotacoes/carnes/bovinos/boi-gordo-15kg/')

    driver.execute_script('window.scrollTo(0, 310);')
    sleep(2)

    est = driver.find_element(By.XPATH,'//*[@id="FiltroGeoEstado"]')
    estados = Select(est)

    estados.select_by_visible_text(uf)
    sleep(1)

    driver.find_element(By.XPATH,'//*[@id="btnEnviarFiltroGeral-5231"]').click()
    sleep(1)

    driver.execute_script('window.scrollTo(0, 1900);')

    try:
        tabela = driver.find_element(By.XPATH,'//*[@id="agks-cont-tb1"]/table')
        html_tabela = tabela.get_attribute('outerHTML')
        sleep(2)

        soup = BeautifulSoup(html_tabela, 'html.parser')
        table = soup.find(name='table')

        df_full = pd.read_html( str(table) ) [0]
        sleep(1)

        infos = df_full.drop(['PREÇO', 'Última Atualização', 'Freq', 'Gráfico'], axis='columns')

        pre = driver.find_elements(By.XPATH,'//*[@id="agks-cont-tb1"]/table/tbody/tr/td[3]/div')
        sleep(2)

        links = []
        widths = []
        heights = []
        starts = []
        ends = []

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

            links.append(linkk)
            widths.append(width[0])
            heights.append(height[0])
            starts.append(start)
            ends.append(end)


        for i in range(len(links)):

            driver.get(links[i])
            sleep(2)

            image = driver.find_element(By.XPATH,'/html/body/img')
            sleep(2)

            with open('imagem.png', 'wb') as f:
                f.write(image.screenshot_as_png)


            img = cv2.imread("imagem.png")

            ys = int(ends[i])
            yf = int(ends[i]) + int(heights[i])

            xs = int(starts[i])
            xf  = int(starts[i]) + int(widths[i])



            croped = img[ys:yf, xs:xf]

            cv2.imwrite('tag.png', croped)

            imagem = cv2.imread("tag.png")

            pre = pytesseract.image_to_string(imagem)
            prec = pre.split('\n')
            preco = prec[0]
            
            precos.append(str(preco))


        dados = infos.assign(preco=precos)


        for i, preco in enumerate(dados['preco']):
            prod = dados.loc[i, "Produto"]
            esta = dados.loc[i, "LOCAL"]
            pr = dados.loc[i, "preco"]

            prod = str(prod)
            esta = str(esta)
            pre = str(pr)

            produ = prod.split('   ')
            produt = produ[1].split('Kg')
            produto = produt[0] + 'kg'

            estad = esta.split('   ')
            estadd = estad[1].split(')')
            estadoo = estadd[0] + ')'

            if "'" in estadoo:
                estado = estadoo.replace("'", "")
            else:
                estado = estadoo
            

            prec = pre.split('   ')
            precc = prec[1].split()
            preco = precc[0]



            itens.append({
                "Produto": produto,
                "Estado": estado,
                "Preco": preco,
                "Data": data_hoje
            })

        for item in itens:
            print(item)

        
    except:
        next