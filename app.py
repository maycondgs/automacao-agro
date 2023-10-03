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
import math
import mysql.connector
import os



dda = datetime.today()
da = str(dda).split(' ')
dataa = da[0].split('-')
data = f'{dataa[2]}/{dataa[1]}/{dataa[0]}'
data_hoje = da[0]

db = mysql.connector.connect(
    user='agrouser',
    password='agropass_TC7EeT2DaheojULHMvxa',
    host = 'connection-agrolivre-542543.agrolivrebrasil.com',
    port = '45821',
    database='agrolivre'
)


def iniciar_driver():
    chrome_options = Options()
    arguments = ['--lang=pt-BR', '--start-maximized', '--incognito', '--headless']
    for argument in arguments:
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1,

    })
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

header = {
    'Content-Type': 'application/json'
    }

ufs = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT','PA',
    'PB','PE','PI', 'PR','RJ','RN','RO','RR','RS','SC','SE','SP','TO']


tipos_algodao = ['/algodao-em-caroco-15kg','/algodao-em-pluma-15kg']
tipos_arroz = ['/arroz-em-casca-irrigado-sc-60kg', '/arroz-em-casca-longo-fino-sc-60kg', '/arroz-em-casca-sc-60kg', '/arroz-irrigado-em-casca-sc-50kg', '/arroz-sequeiro-cultivar-primavera-sc-60kg','/arroz-sequeiro-tipo-1-sc-60kg']
tipos_amendoim = ['/amendoim-com-casca-1kg', '/amendoim-com-casca-sc-25kg', '/amendoim-sc-10kg']
tipos_cafe = ['/cafe-arabica-bebida-dura-tipo-6-safra-nova-sc-60kg', '/cafe-arabica-despolpado-sc-60kg', '/cafe-arabica-duro-sc-60kg', '/cafe-arabica-rio-sc-60kg', '/cafe-arabica-tipo-6-bebida-dura-sc-60kg','/cafe-arabica-tipo-6-duro-sc-60kg', '/cafe-arabica-tipo-6-sc-60kg', '/cafe-arabica-tipo-7-sc-60kg', '/cafe-beneficiado-cereja-descascado-sc-60kg', '/cafe-beneficiado-sc-60kg', '/cafe-beneficiado-tipo-6-duro-sc-60kg', '/cafe-conillon-sc-60kg', '/cafe-conilon-tipo-7-sc-60kg', '/cafe-conilon-tipo-7-8-sc-60kg','/cafe-conilon-tipo-8-sc-60kg']
tipos_cana = ['/cana-de-acucar-1ton']
tipos_feijao = ['/feijao-carioca-extra-safra-nova-sc-60kg', '/feijao-carioca-sc-60kg', '/feijao-carioquinha-30kg', '/feijao-carioquinha-sc-60kg', '/feijao-caupi-sc-60kg', '/feijao-cores-sc-60kg', '/feijao-de-corda-caupi-sc-60kg', '/feijao-manteiga-30kg', '/feijao-preto-30kg','/feijao-preto-sc-60kg', '/feijao-vermelho-30kg', '/feijao-vermelho-safra-sc-60kg']
tipos_milho = ['/milho-50kg', '/milho-seco-sc-25kg', '/milho-seco-sc-60kg']
tipos_soja = ['/soja-em-grao-sc-60kg', '/soja-s--royalts-sc-60kg']
tipos_sorgo = ['/sorgo-sc-60kg']
tipos_trigo = ['/trigo-em-grao-nacional-sc-60kg', '/trigo-granel-1ton']
tipos_bovinos = ['/bezerra-12-meses-1cab', '/bezerro-12-meses-1cab','/bezerro-1cab', '/boi-gordo-15kg', '/boi-gordo-castrado-15kg', '/boi-gordo-inteiro-15kg', '/boi-gordo-kg-vivo-1kg', '/boi-magro-1cab', '/boi-magro-30-meses-1cab', '/garrote-1-a-2-anos-1cab', '/garrote-18-meses-1cab', '/novilha-1-a-2-anos-1cab', '/novilha-gorda-15kg', '/vaca-boiadeira-1cab', '/vaca-gorda-15kg', '/vaca-gorda-kg-vivo-1kg']
tipos_suinos = ['/leitao-----22-kg--1kg', '/suino-1kg', '/suino-tipo-carne-15kg']
tipos_aves = ['/frango-1kg']
tipos_caprinos = ['/caprino-adulto-15kg']
tipos_ovinos = ['/cordeiro-kg-vivo-1kg', '/ovino-15kg']
tipos_beterraba = ['/beterraba-comum-sc-20kg', '/beterraba-extra-cx-23kg']
tipos_tomate = ['/tomate-1kg', '/tomate-20kg', '/tomate-longa-vida-23kg', '/tomate-longa-vida-cx-23kg', '/tomate-mesa-cx-22kg']
tipos_pimentao = ['/pimentao-verde-1kg']
tipos_cebola = ['/cebola-nacional-sc-20kg','/cebola-pera-classe-3-a-5-sc-20kg', '/cebola-vermelha--crioula--produtor-1kg', '/cebola-vermelha--crioula--tipo-2-beneficiador-sc-20kg', '/cebola-vermelha--crioula--tipo-3-atacado-sc-20kg', '/cebola-vermelha--crioula--tipo-3-beneficiador-sc-20kg', '/cebola-vermelha--crioula--tipo-4-beneficiador-sc-20kg', '/cebola-vermelha-argentina-tipo-3-beneficiador-sc-20kg', '/cebola-vermelha-tipo-3-atacado-sc-20kg']
tipos_couve = ['/couve-flor-1dz']
tipos_cenoura = ['/cenoura-comum-cx-23-kg-cx-23kg', '/cenoura-cx-20kg', '/cenoura-extra-cx-19kg', '/cenoura-verao-a---atacado-cx-20kg', '/cenoura-verao-a-lavada-beneficiador-cx-20kg', '/cenoura-verao-aaa---beneficiador-cx-20kg', '/cenoura-verao-g---atacado-cx-20kg', '/cenoura-verao-g-lavada---beneficiador-cx-20kg', '/cenoura-verao-suja---produtor-cx-20kg']





def login(driver):

    driver.get('https://www.agrolink.com.br/login')
    sleep(2)

    driver.execute_script('window.scrollTo(0, 310);')
    sleep(1)

    driver.find_element(By.XPATH,'/html/body/div[1]/section/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/div/form[1]/div/div[1]/input').send_keys('xetedo9314@ratedane.com')
    sleep(2)
    driver.find_element(By.XPATH,'/html/body/div[1]/section/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/div/form[1]/div/div[2]/input').send_keys('webscraper')

    driver.find_element(By.XPATH,'/html/body/div[1]/section/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/div/form[1]/div/div[3]/button').click()


def scrap(tipo, itemrq):

    for uf in ufs:
        link = f'https://www.agrolink.com.br/cotacoes/historico/{uf}{tipo}'
        page = requests.get(link,headers=header)

        soup = BeautifulSoup(page.content, 'html.parser')

        dom = etree.HTML(str(soup))

        data = (dom.xpath('//*[@id="content"]/div/div/div[3]/div[1]/div[5]/div[1]/table/tbody/tr/td[1]/text()'))
        estadual = (dom.xpath('//*[@id="content"]/div/div/div[3]/div[1]/div[5]/div[1]/table/tbody/tr/td[2]/text()'))
        nacional = (dom.xpath('//*[@id="content"]/div/div/div[3]/div[1]/div[5]/div[1]/table/tbody/tr/td[3]/text()'))
            
        estado = uf
        nom = tipo.split('/')
        nome = nom[1]
        
        dados = []

        for dat, estadua, naciona in zip(data, estadual, nacional):

            dados.append({"Item": nome,"Estado": estado,"Data": dat,"Estadual": estadua,"Nacional": naciona})

        bd = requests.get(f'https://api-cotacoes.agrolivrebrasil.com/mes/{itemrq}')

        tb = json.loads(bd.content)

        itens = []

        for dado in dados:
            item = dado['Item']
            estado = dado['Estado']
            data = dado['Data']
            estadual = dado['Estadual']
            nacional = dado['Nacional']

            itens.append([item, estado, data, estadual, nacional])


        for novo in itens:
            if novo not in tb:
                payl = {
                    "Item": novo[0],
                    "Estado": novo[1],
                    "Data": novo[2],
                    "Estadual": novo[3],
                    "Nacional": novo[4],
                }

                print(payl)

                st = json.dumps(payl)

                requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/mes/{itemrq}', headers=header, data=st)
                
                    

def busca(driver,wait, itemgrupo, itemespecie, itemproduto):

    driver.get('https://www.agrolink.com.br/cotacoes/busca')
    sleep(1)

    driver.execute_script('window.scrollTo(0, 230);')
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

    driver.execute_script('window.scrollTo(0, 320);')
    
    dattaa = wait.until(condicao_esperada.element_to_be_clickable((By.XPATH,'//*[@id="DataInicial"]')))
    dattaa.click()
    sleep(2)
    

    try:
        driver.find_element(By.XPATH,'//th[@class="today"]').click()
        sleep(3)

    except:
        return


    wait.until(condicao_esperada.element_to_be_clickable((By.XPATH,'//*[@id="btnEnviarFiltroGeral-5231"]'))).click()
    sleep(1)


def page(driver):
    driver.execute_script('window.scrollTo(0, 1000);')
    sleep(2)
    numli = driver.find_elements(By.XPATH,'//*[@id="dvPaginacao"]/ul/li')
    num = len(numli)
    print(num)
    match num:
        case 2:
            driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li[2]/a').click()
            sleep(1)
        case 3:
            driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li[3]/a').click()
            sleep(1)
        case 4:
            driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li[4]/a').click()
            sleep(1)
        case 5:
            driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li[5]/a').click()
            sleep(1)
        case 6:
            driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li[6]/a').click()
            sleep(1)

def scraw(driver, wait):

    itens = []

    tabela = driver.find_element(By.XPATH,'//*[@id="agks-cont-tb1"]/table')
    html_tabela = tabela.get_attribute('outerHTML')
    sleep(2)

    soup = BeautifulSoup(html_tabela, 'html.parser')
    table = soup.find(name='table')

    df_full = pd.read_html( str(table) ) [0]
    sleep(1)

    infos = df_full.drop(['PREÇO', 'Última Atualização', 'Freq', 'Gráfico'], axis='columns')

    pre = driver.find_elements(By.XPATH,'//*[@id="agks-cont-tb1"]/table/tbody/tr/td[3]')
    sleep(2)

    precos = []

    print(len(pre))
    for prev in pre:
        if prev.find_element(By.TAG_NAME, 'div'):
    
            linkpre = prev.find_element(By.TAG_NAME, 'div').get_attribute('style')
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

            driver.execute_script(f"window.open('{linkk}', '_blank')")
            sleep(1)
            driver.switch_to.window(driver.window_handles[1])
            sleep(2)
            image = wait.until(condicao_esperada.presence_of_element_located((By.XPATH,'/html/body/img')))
            sleep(1)

            with open('imagem.png', 'wb') as f:
                f.write(image.screenshot_as_png)

            sleep(1)
            driver.close()

            driver.switch_to.window(driver.window_handles[0])

            img = cv2.imread("imagem.png")

            ys = int(end)
            yf = int(end) + int(height[0])

            xs = int(start)
            xf  = int(start) + int(width[0])


            croped = img[ys:yf, xs:xf]

            cv2.imwrite('tag.png', croped)

            imagem = cv2.imread("tag.png")

            pre = pytesseract.image_to_string(imagem)
            prec = pre.split('\n')
            preco = prec[0]
            precos.append(str(preco))

        else:
            preco = prev.text
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
        produt = produ[1].split('\n')

        estad = esta.split('   ')
        estadd = estad[1].split(')')
        estadoo = estadd[0] + ')'

        if "'" in estadoo:
            estado = estadoo.replace("'", "")
        else:
            estado = estadoo


        if estadoo in produt[0]:
            producto = produt[0].split(estadoo)
            produto = producto[0]
        else:
            produto = produt[0]
            if 'Kg ' in produto:
                proto = produto.split('Kg ')
                produto = proto[0] + 'Kg'


        prec = pre.split('   ')
        precc = prec[1].split()

        if ',' in precc[0]:
            preco = precc[0]
        else:
            pr = precc[0]
            v = len(pr)
            if v == 2:
                preco = f'{pr[0]}{pr[1]},00'
            elif v == 3:
                preco = f'{pr[0]},{pr[1]}{pr[2]}'
            elif v == 4:
                preco = f'{pr[0]}{pr[1]},{pr[2]}{pr[3]}'

        itens.append({
            "Produto": produto,
            "Estado": estado,
            "Preco": preco,
            "Data": data_hoje
        })
            


    return itens


def post(itemarq, item):

    cursor = db.cursor()
    sql = f"INSERT INTO {itemarq} (nome, estado, preco, data) VALUES ('{item['Produto']}', '{item['Estado']}', '{item['Preco']}', '{item['Data']}')"
    cursor.execute(sql)
    db.commit()


def crawler(driver,wait,itemgrupo,itemespecie,itemproduto,prodformat):
    
    busca(driver,wait, itemgrupo, itemespecie, itemproduto)

    driver.execute_script('window.scrollTo(0, 2200);')

    try:
        inf = driver.find_element(By.XPATH,'//*/div/div[2]/small/i').text
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
            page(driver)
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
            page(driver)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)


        case 4:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            sleep(1)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)


        case 5:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)


            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

                
        case 6:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            itens3 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens6 = scraw(driver, wait)
            for item in itens6:
                post(prodformat, item)


        case 7:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens6 = scraw(driver, wait)
            for item in itens6:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens7 = scraw(driver, wait)
            for item in itens7:
                post(prodformat, item)


        case 8:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens6 = scraw(driver, wait)
            for item in itens6:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens7 = scraw(driver, wait)
            for item in itens7:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens8 = scraw(driver, wait)
            for item in itens8:
                post(prodformat, item)


        case 9:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens6 = scraw(driver, wait)
            for item in itens6:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens7 = scraw(driver, wait)
            for item in itens7:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens8 = scraw(driver, wait)
            for item in itens8:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens9 = scraw(driver, wait)
            for item in itens9:
                post(prodformat, item)


        case 10:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens6 = scraw(driver, wait)
            for item in itens6:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens7 = scraw(driver, wait)
            for item in itens7:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens8 = scraw(driver, wait)
            for item in itens8:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens9 = scraw(driver, wait)
            for item in itens9:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens10 = scraw(driver, wait)
            for item in itens10:
                post(prodformat, item)


        case 11:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens6 = scraw(driver, wait)
            for item in itens6:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens7 = scraw(driver, wait)
            for item in itens7:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens8 = scraw(driver, wait)
            for item in itens8:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens9 = scraw(driver, wait)
            for item in itens9:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens10 = scraw(driver, wait)
            for item in itens10:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens11 = scraw(driver, wait)
            for item in itens11:
                post(prodformat, item)


        case 12:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens6 = scraw(driver, wait)
            for item in itens6:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens7 = scraw(driver, wait)
            for item in itens7:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens8 = scraw(driver, wait)
            for item in itens8:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens9 = scraw(driver, wait)
            for item in itens9:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens10 = scraw(driver, wait)
            for item in itens10:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens11 = scraw(driver, wait)
            for item in itens11:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens12 = scraw(driver, wait)
            for item in itens12:
                post(prodformat, item)


        case 13:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens6 = scraw(driver, wait)
            for item in itens6:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens7 = scraw(driver, wait)
            for item in itens7:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens8 = scraw(driver, wait)
            for item in itens8:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens9 = scraw(driver, wait)
            for item in itens9:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens10 = scraw(driver, wait)
            for item in itens10:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens11 = scraw(driver, wait)
            for item in itens11:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens12 = scraw(driver, wait)
            for item in itens12:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens13 = scraw(driver, wait)
            for item in itens13:
                post(prodformat, item)


        case 14:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens6 = scraw(driver, wait)
            for item in itens6:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens7 = scraw(driver, wait)
            for item in itens7:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens8 = scraw(driver, wait)
            for item in itens8:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens9 = scraw(driver, wait)
            for item in itens9:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens10 = scraw(driver, wait)
            for item in itens10:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens11 = scraw(driver, wait)
            for item in itens11:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens12 = scraw(driver, wait)
            for item in itens12:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens14 = scraw(driver, wait)
            for item in itens14:
                post(prodformat, item)


        case 15:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens6 = scraw(driver, wait)
            for item in itens6:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens7 = scraw(driver, wait)
            for item in itens7:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens8 = scraw(driver, wait)
            for item in itens8:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens9 = scraw(driver, wait)
            for item in itens9:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens10 = scraw(driver, wait)
            for item in itens10:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens11 = scraw(driver, wait)
            for item in itens11:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens12 = scraw(driver, wait)
            for item in itens12:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens14 = scraw(driver, wait)
            for item in itens14:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens15 = scraw(driver, wait)
            for item in itens15:
                post(prodformat, item)


        case 16:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens6 = scraw(driver, wait)
            for item in itens6:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens7 = scraw(driver, wait)
            for item in itens7:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens8 = scraw(driver, wait)
            for item in itens8:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens9 = scraw(driver, wait)
            for item in itens9:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens10 = scraw(driver, wait)
            for item in itens10:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens11 = scraw(driver, wait)
            for item in itens11:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens12 = scraw(driver, wait)
            for item in itens12:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens14 = scraw(driver, wait)
            for item in itens14:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens15 = scraw(driver, wait)
            for item in itens15:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens16 = scraw(driver, wait)
            for item in itens16:
                post(prodformat, item)


        case 17:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens6 = scraw(driver, wait)
            for item in itens6:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens7 = scraw(driver, wait)
            for item in itens7:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens8 = scraw(driver, wait)
            for item in itens8:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens9 = scraw(driver, wait)
            for item in itens9:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens10 = scraw(driver, wait)
            for item in itens10:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens11 = scraw(driver, wait)
            for item in itens11:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens12 = scraw(driver, wait)
            for item in itens12:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens14 = scraw(driver, wait)
            for item in itens14:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens15 = scraw(driver, wait)
            for item in itens15:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens16 = scraw(driver, wait)
            for item in itens16:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens17 = scraw(driver, wait)
            for item in itens17:
                post(prodformat, item)


        case 18:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens6 = scraw(driver, wait)
            for item in itens6:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens7 = scraw(driver, wait)
            for item in itens7:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens8 = scraw(driver, wait)
            for item in itens8:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens9 = scraw(driver, wait)
            for item in itens9:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens10 = scraw(driver, wait)
            for item in itens10:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens11 = scraw(driver, wait)
            for item in itens11:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens12 = scraw(driver, wait)
            for item in itens12:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens14 = scraw(driver, wait)
            for item in itens14:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens15 = scraw(driver, wait)
            for item in itens15:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens16 = scraw(driver, wait)
            for item in itens16:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens17 = scraw(driver, wait)
            for item in itens17:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens18 = scraw(driver, wait)
            for item in itens18:
                post(prodformat, item)


        case 19:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens6 = scraw(driver, wait)
            for item in itens6:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens7 = scraw(driver, wait)
            for item in itens7:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens8 = scraw(driver, wait)
            for item in itens8:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens9 = scraw(driver, wait)
            for item in itens9:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens10 = scraw(driver, wait)
            for item in itens10:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens11 = scraw(driver, wait)
            for item in itens11:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens12 = scraw(driver, wait)
            for item in itens12:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens14 = scraw(driver, wait)
            for item in itens14:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens15 = scraw(driver, wait)
            for item in itens15:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens16 = scraw(driver, wait)
            for item in itens16:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens17 = scraw(driver, wait)
            for item in itens17:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens18 = scraw(driver, wait)
            for item in itens18:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens19 = scraw(driver, wait)
            for item in itens19:
                post(prodformat, item)


        case 20:
            itens = scraw(driver, wait)
            for item in itens:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            sleep(1)
            itens2 = scraw(driver, wait)
            for item in itens2:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            itens3 = scraw(driver, wait)
            for item in itens3:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            itens4 = scraw(driver, wait)
            for item in itens4:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens5 = scraw(driver, wait)
            for item in itens5:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens6 = scraw(driver, wait)
            for item in itens6:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens7 = scraw(driver, wait)
            for item in itens7:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens8 = scraw(driver, wait)
            for item in itens8:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens9 = scraw(driver, wait)
            for item in itens9:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens10 = scraw(driver, wait)
            for item in itens10:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens11 = scraw(driver, wait)
            for item in itens11:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens12 = scraw(driver, wait)
            for item in itens12:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens14 = scraw(driver, wait)
            for item in itens14:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens15 = scraw(driver, wait)
            for item in itens15:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens16 = scraw(driver, wait)
            for item in itens16:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens17 = scraw(driver, wait)
            for item in itens17:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens18 = scraw(driver, wait)
            for item in itens18:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens19 = scraw(driver, wait)
            for item in itens19:
                post(prodformat, item)

            busca(driver,wait, itemgrupo, itemespecie, itemproduto)
            sleep(1)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            page(driver)
            itens20 = scraw(driver, wait)
            for item in itens20:
                post(prodformat, item)



       
def scrap_preco():

    codigos = [{'11,8,Todos,algodao'},{'13,5,Todos,arroz'},{'11,30,Todos,amendoim'},{'13,7,Todos,cafe'},{'11,92,Todos,cana'},{'13,46,Todos,feijao'},{'13,2,Todos,milho'},{'13,1,Todos,soja'},{'13,31,Todos,sorgo'},{'13,6,Todos,trigo'},{'10,144,Todos,suinos'},{'10,122,Todos,aves'},{'10,147,Todos,caprinos'},
    {'10,152,Todos,ovinos'},{'14,95,Todos,beterraba'},{'14,40,Todos,tomate'},{'14,51,Todos,pimentao'},{'11,24,Todos,cebola'},{'14,39,Todos,couve'},{'14,27,Todos,cenoura'},{'10,120,Boi Gordo 15Kg,boi'},{'10,120,Vaca Gorda 15Kg,vaca'}]


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
        print(dado)
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
        print(dado)
        post('repolho',dado)




def crawlNoticiasAgricolas():
    
    referencia = 'agricolas'

    page = requests.get('https://www.noticiasagricolas.com.br/noticias/agronegocio/')
    sleep(2)
    
    soup = BeautifulSoup(page.content, 'html.parser')
    dom = etree.HTML(str(soup))

    links = (dom.xpath('//*[@id="content"]/div[2]/ul[1]/li/a/@href'))
    datanoticia = (dom.xpath('//*[@id="content"]/div[2]/h3[1]/text()'))
    data_noticia = datanoticia[0].split('/')
    dia = str(data_noticia[0])
    mes = str(data_noticia[1])
    ano = str(data_noticia[2])
    datafim = f'{ano}-{mes}-{dia}'
    titulo = (dom.xpath('//*[@id="content"]/div[2]/ul[1]/li/a/div/h2/text()'))
    dat = (dom.xpath('//*[@id="content"]/div[2]/ul[1]/li/a/span/text()'))
    horas = []

    for datt in dat:
        hora = f'{datt}:00'

        horas.append(hora)

    novos = []

    for titu, link, hora in zip(titulo, links, horas):     
        lnk = f'https://www.noticiasagricolas.com.br{link}'
        novos.append([titu, lnk, hora, datafim, referencia, referencia])
    

    cursor = db.cursor()
    sql = f"SELECT * FROM noticias_agricolas"

    cursor.execute(sql)
    ext = cursor.fetchall()
    cursor.close()
    linksat = []
    for it in ext:
        linksat.append(it[1])
    
    for novo in novos:
        if novo[1] not in linksat:
            payl = {
                "Titulo": novo[0],
                "Link": novo[1],
                "Hora": novo[2],
                "Data": novo[3],
                "Referencia": novo[4],
                "Categoria" : novo[5]
            }
            print(f'Noticia: {payl}')
            cursord = db.cursor()
            sql = f"INSERT INTO noticias_agricolas (Titulo, Link, Hora, Data, Referencia, Categoria) VALUES ('{payl['Titulo']}', '{payl['Link']}', '{payl['Hora']}', '{payl['Data']}', '{payl['Referencia']}', '{payl['Categoria']}')"
            cursord.execute(sql)
            db.commit()
            cursord.close()

    db.close()

    
def crawlNoticiasAgrolink():
        
    links = ['https://www.agrolink.com.br/noticias/categoria/agricultura/lista','https://www.agrolink.com.br/noticias/categoria/pecuaria/lista', 'https://www.agrolink.com.br/noticias/categoria/economia/lista','https://www.agrolink.com.br/noticias/categoria/politica/lista', 'https://www.agrolink.com.br/noticias/categoria/tecnologia/lista']

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
            datt = str(dattt[0]).split('/')
            data.append(f'{datt[2]}-{datt[1]}-{datt[0]}')
            hora.append(dattt[1])

        for lnk in links2:
            lnks2.append(f'https://www.agrolink.com.br{lnk}')

        novos = []

        for titu, link, data, hora in zip(titulo, lnks2, data, hora):     
            novos.append([titu, link, hora, data, referencia, categoria])

        cursorl = db.cursor()
        sql = f"SELECT * FROM noticias_agrolink"

        cursorl.execute(sql)
        ext = cursorl.fetchall()
        cursorl.close()

        linksat = []
        for it in ext:
            linksat.append(it[1])

        for novo in novos:
            if novo[1] not in linksat:
                payl = {
                    "Titulo": novo[0],
                    "Link": novo[1],
                    "Hora": novo[2],
                    "Data": novo[3],
                    "Referencia": novo[4],
                    "Categoria" : novo[5]
                }
                print(f'Noticia: {payl}')
                cursorld = db.cursor()
                sql = f"INSERT INTO noticias_agrolink (Titulo, Link, Hora, Data, Referencia, Categoria) VALUES ('{payl['Titulo']}', '{payl['Link']}', '{payl['Hora']}', '{payl['Data']}', '{payl['Referencia']}', '{payl['Categoria']}')"
                cursorld.execute(sql)
                db.commit()
                cursorld.close()
        
    
    db.close()
                

def crawlNoticiasCanalRural(): 
            
    referencia = 'Canal Rural'

    page = requests.get('https://www.canalrural.com.br/ultimas-noticias/')
    
    soup = BeautifulSoup(page.content, 'html.parser')
    dom = etree.HTML(str(soup))

    links = (dom.xpath('/html/body/main/div[2]/div/div[1]/div/article/a/@href'))

    for link in links:
        page1 = requests.get(link)
    
        soup1 = BeautifulSoup(page1.content, 'html.parser')
        dom1 = etree.HTML(str(soup1))


        titu = (dom1.xpath('/html/body/main/section[1]/div/div[1]/strong/h1/text()'))
        titul = titu[0].split('\n')
        titulo = titul[1]
        dat = (dom1.xpath('/html/body/main/section[1]/div/div[2]/div[2]/time[1]/text()'))
        datt = dat[1].split('\n')
        dattt = datt[1].split()
        
        dattn = dattt[0].strip()
        datan = dattn.split('/')
        data = f'{datan[2]}-{datan[1]}-{datan[0]}'
        hora = f'{dattt[1]}:00'
    
        novo = [titulo, link, hora, data, referencia, referencia]

        cursorr = db.cursor()
        sql = "SELECT * FROM noticias_canal_rural"

        cursorr.execute(sql)
        ext = cursorr.fetchall()
        cursorr.close()

        linksat = []
        for it in ext:
            linksat.append(it[1])
        
        if novo[1] not in linksat:
            payl = {
                "Titulo": novo[0],
                "Link": novo[1],
                "Hora": novo[2],
                "Data": novo[3],
                "Referencia": novo[4],
                "Categoria" : novo[5]
            }
            print(f'Noticia: {payl}')
            cursorrd = db.cursor()
            sql = f"INSERT INTO noticias_canal_rural (Titulo, Link, Hora, Data, Referencia, Categoria) VALUES ('{payl['Titulo']}', '{payl['Link']}', '{payl['Hora']}', '{payl['Data']}', '{payl['Referencia']}', '{payl['Categoria']}')"
            cursorrd.execute(sql)
            db.commit()
            cursorrd.close()

            
    db.close()   



def scrapy_tabela():
    print('SCRAPING TABELA')

    for tipo in tipos_arroz:

        itemrq = 'arroz'
        scrap(tipo, itemrq)

    for tipo in tipos_algodao:

        itemrq = 'algodao'
        scrap(tipo, itemrq)

    for tipo in tipos_amendoim:

        itemrq = 'amendoim'
        scrap(tipo, itemrq)

    for tipo in tipos_cafe:

        itemrq = 'cafe'
        scrap(tipo, itemrq)

    for tipo in tipos_cana:

        itemrq = 'cana'
        scrap(tipo, itemrq)

    for tipo in tipos_feijao:

        itemrq = 'feijao'
        scrap(tipo, itemrq)

    for tipo in tipos_milho:

        itemrq = 'milho'
        scrap(tipo, itemrq)

    for tipo in tipos_soja:

        itemrq = 'soja'
        scrap(tipo, itemrq)

    for tipo in tipos_sorgo:

        itemrq = 'sorgo'
        scrap(tipo, itemrq)

    for tipo in tipos_trigo:

        itemrq = 'trigo'
        scrap(tipo, itemrq)

    for tipo in tipos_bovinos:

        itemrq = 'bovinos'
        scrap(tipo, itemrq)

    for tipo in tipos_suinos:

        itemrq = 'suinos'
        scrap(tipo, itemrq)

    for tipo in tipos_aves:

        itemrq = 'aves'
        scrap(tipo, itemrq)

    for tipo in tipos_caprinos:

        itemrq = 'caprinos'
        scrap(tipo, itemrq)

    for tipo in tipos_ovinos:

        itemrq = 'ovinos'
        scrap(tipo, itemrq)

    for tipo in tipos_beterraba:

        itemrq = 'beterraba'
        scrap(tipo, itemrq)

    for tipo in tipos_tomate:

        itemrq = 'tomate'
        scrap(tipo, itemrq)

    for tipo in tipos_pimentao:

        itemrq = 'pimentao'
        scrap(tipo, itemrq)

    for tipo in tipos_cebola:

        itemrq = 'cebola'
        scrap(tipo, itemrq)

    for tipo in tipos_couve:

        itemrq = 'couve'
        scrap(tipo, itemrq)

    for tipo in tipos_cenoura:

        itemrq = 'cenoura'
        scrap(tipo, itemrq)        

def scrapy_noticias():
    crawlNoticiasAgricolas()
    crawlNoticiasAgrolink()
    crawlNoticiasCanalRural()   



def scrapy_precos():
    scrap_preco()
    sleep(1)
    crawlAlface()
    sleep(1)
    crawlRepolho() 





def run(job):
    threaded = threading.Thread(target=job)
    threaded.start()




schedule.every(1).minute.do(run, scrapy_noticias)
schedule.every().day.at("04:30").do(run, scrapy_precos)
schedule.every().monday.do(run, scrapy_tabela)






while 1:
    schedule.run_pending()
    sleep(1)
