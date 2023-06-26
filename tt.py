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


data_hoje = f'{dataa[2]}/{dataa[1]}/{dataa[0]}'



option = Options()

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




urls = [
    {'arroz-https://www.agrolink.com.br/cotacoes/graos/arroz/'},
    {'algodao-https://www.agrolink.com.br/cotacoes/diversos/algodao/'},
    {'amendoim-https://www.agrolink.com.br/cotacoes/diversos/amendoim/'},
    {'cafe-https://www.agrolink.com.br/cotacoes/graos/cafe/'},
    {'cana-https://www.agrolink.com.br/cotacoes/diversos/cana-de-acucar/'},
    {'feijao-https://www.agrolink.com.br/cotacoes/graos/feijao/'},
    {'milho-https://www.agrolink.com.br/cotacoes/graos/milho/'},
    {'soja-https://www.agrolink.com.br/cotacoes/graos/soja/'},
    {'sorgo-https://www.agrolink.com.br/cotacoes/graos/sorgo/'},
    {'trigo-https://www.agrolink.com.br/cotacoes/graos/trigo/'},
    {'bovinos-https://www.agrolink.com.br/cotacoes/carnes/bovinos/'},
    {'suinos-https://www.agrolink.com.br/cotacoes/carnes/suinos/'},
    {'aves-https://www.agrolink.com.br/cotacoes/carnes/aves/'},
    {'caprinos-https://www.agrolink.com.br/cotacoes/carnes/caprinos/'},
    {'ovinos-https://www.agrolink.com.br/cotacoes/carnes/ovinos/'},
    {'beterraba-https://www.agrolink.com.br/cotacoes/hortalicas/beterraba/'},
    {'tomate-https://www.agrolink.com.br/cotacoes/hortalicas/tomate/'},
    {'pimentao-https://www.agrolink.com.br/cotacoes/hortalicas/pimentao/'},
    {'cebola-https://www.agrolink.com.br/cotacoes/diversos/cebola/'},
    {'couve-https://www.agrolink.com.br/cotacoes/hortalicas/couve/'},
    {'cenoura-https://www.agrolink.com.br/cotacoes/hortalicas/cenoura/'}
]


header = {
    'Content-Type': 'application/json'
    }

ufs = ['ac','al','am','ap','ba','ce','df','es','go','ma','mg','ms','mt','pa','pb','pe','pi','pr','rj','rn','ro','rr','rs','sc','se','sp','to']


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



def varrer(driver):

    tabela = driver.find_element(By.XPATH,'//*[@id="agks-cont-tb1"]/table')
    html_tabela = tabela.get_attribute('outerHTML')
    sleep(2)

    soup = BeautifulSoup(html_tabela, 'html.parser')
    table = soup.find(name='table')

    df_full = pd.read_html( str(table) ) [0]
    sleep(1)

    driver.execute_script('window.scrollTo(0, 1900);')
    sleep(2)

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

        pytesseract.pytesseract.tesseract_cmd = "/app/.apt/usr/bin/tesseract"

        pre = pytesseract.image_to_string(imagem)
        prec = pre.split('\n')
        preco = prec[0]
        
        precos.append(str(preco))


    dados = infos.assign(preco=precos)

    itens = []

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
        estado = estadd[0] + ')'

        prec = pre.split('   ')
        precc = prec[1].split()
        preco = precc[0]

        itens.append({
            "Produto": produto,
            "Estado": estado,
            "Preco": preco,
            "Data": data_hoje
            })
        


    return itens

def pagini(driver, link):
    driver.get(link)
    sleep(5)

    driver.execute_script('window.scrollTo(0, 430);')

    driver.find_element(By.XPATH,'//*[@id="DataInicial"]').click()
    sleep(5)

    driver.find_element(By.XPATH,'/html/body/div[5]/div[1]/table/tfoot/tr[1]/th').click()
    sleep(3)

    driver.find_element(By.XPATH,'//*[@id="btnEnviarFiltroGeral-5231"]').click()
    sleep(5)
            
    driver.execute_script('window.scrollTo(0, 1950);') 
    sleep(2)

def proxpage(driver):
    driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]').click()
    driver.execute_script('window.scrollTo(0, 1900);')






def scrapy_agro():

    driver = iniciar_driver()

    driver.get('https://www.agrolink.com.br/login')
    sleep(2)

    driver.execute_script('window.scrollTo(0, 310);')
    sleep(1)

    driver.find_element(By.XPATH,'/html/body/div[1]/section/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/div/form[1]/div/div[1]/input').send_keys('xetedo9314@ratedane.com')
    sleep(2)
    driver.find_element(By.XPATH,'/html/body/div[1]/section/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/div/form[1]/div/div[2]/input').send_keys('webscraper')

    driver.find_element(By.XPATH,'/html/body/div[1]/section/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/div/form[1]/div/div[3]/button').click()

    
    for url in urls:

        item = str(url)
        it = item.split('-')

        nom = it[0].split("'")
        nome = nom[1]

        lin = it[1].split("'")
        link = lin[0]


        driver.get(link)
        sleep(7)

        driver.execute_script('window.scrollTo(0, 450);')
        sleep(1)
        driver.find_element(By.XPATH,'//*[@id="DataInicial"]').click()
        sleep(7)

        try:
            driver.find_element(By.XPATH,'/html/body/div[5]/div[1]/table/tfoot/tr[1]/th').click()
            sleep(3)

            driver.find_element(By.XPATH,'//*[@id="btnEnviarFiltroGeral-5231"]').click()
            sleep(5)
                
            driver.execute_script('window.scrollTo(0, 1950);') 
            sleep(2)
        except:
            break
        
        dados = varrer(driver)

        sleep(1)

        for dado in dados:
            st = json.dumps(dado)

            requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}',headers=header, data=st)

        pagini(driver, link)

        try:
            #page2
            driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]')
            proxpage(driver)

            dados2 = varrer(driver)
            sleep(1)

            for dado in dados2:
                st = json.dumps(dado)

                requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}',headers=header, data=st)

            pagini(driver, link)
            proxpage(driver)
            try:
                #page3
                driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]')
                proxpage(driver)

                dados3 = varrer(driver)
                sleep(1)

                for dado in dados3:
                    st = json.dumps(dado)

                    requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}',headers=header, data=st)

                pagini(driver, link)
                proxpage(driver)
                proxpage(driver)
                try:
                    #page4
                    driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]')
                    proxpage(driver)

                    dados4 = varrer(driver)
                    sleep(1)

                    for dado in dados4:
                        st = json.dumps(dado)

                        requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}',headers=header, data=st)

                    pagini(driver, link)
                    proxpage(driver)
                    proxpage(driver)
                    proxpage(driver)
                    try:
                        #page5
                        driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]')
                        proxpage(driver)

                        dados5 = varrer(driver)
                        sleep(1)

                        for dado in dados5:
                            st = json.dumps(dado)

                            requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}',headers=header, data=st)

                        pagini(driver, link)
                        proxpage(driver)
                        proxpage(driver)
                        proxpage(driver)
                        proxpage(driver)
                        try:
                            #page6
                            driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]')
                            proxpage(driver)

                            dados6 = varrer(driver)
                            sleep(1)

                            for dado in dados6:
                                st = json.dumps(dado)

                                requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}',headers=header, data=st)

                            pagini(driver, link)
                            proxpage(driver)
                            proxpage(driver)
                            proxpage(driver)
                            proxpage(driver)
                            proxpage(driver)
                            try:
                                #page7
                                driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]')
                                proxpage(driver)

                                dados7 = varrer(driver)
                                sleep(1)

                                for dado in dados7:
                                    st = json.dumps(dado)

                                    requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}',headers=header, data=st)

                                pagini(driver, link)
                                proxpage(driver)
                                proxpage(driver)
                                proxpage(driver)
                                proxpage(driver)
                                proxpage(driver)
                                proxpage(driver)
                                try:
                                    #page8
                                    driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]')
                                    proxpage(driver)

                                    dados8 = varrer(driver)
                                    sleep(1)

                                    for dado in dados8:
                                        st = json.dumps(dado)

                                        requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}',headers=header, data=st)

                                    pagini(driver, link)
                                    proxpage(driver)
                                    proxpage(driver)
                                    proxpage(driver)
                                    proxpage(driver)
                                    proxpage(driver)
                                    proxpage(driver)
                                    proxpage(driver)
                                    try:
                                        #page9
                                        driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]')
                                        proxpage(driver)

                                        dados9 = varrer(driver)
                                        sleep(1)

                                        for dado in dados9:
                                            st = json.dumps(dado)

                                            requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}',headers=header, data=st)

                                        pagini(driver, link)
                                        proxpage(driver)
                                        proxpage(driver)
                                        proxpage(driver)
                                        proxpage(driver)
                                        proxpage(driver)
                                        proxpage(driver)
                                        proxpage(driver)
                                        proxpage(driver)
                                        try:
                                            #page10
                                            driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]')
                                            proxpage(driver)

                                            dados10 = varrer(driver)
                                            sleep(1)

                                            for dado in dados10:
                                                st = json.dumps(dado)

                                                requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}',headers=header, data=st)

                                            pagini(driver, link)
                                            proxpage(driver)
                                            proxpage(driver)
                                            proxpage(driver)
                                            proxpage(driver)
                                            proxpage(driver)
                                            proxpage(driver)
                                            proxpage(driver)
                                            proxpage(driver)
                                            proxpage(driver)
                                            try:
                                                #page11
                                                driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]')
                                                proxpage(driver)

                                                dados11 = varrer(driver)
                                                sleep(1)

                                                for dado in dados11:
                                                    st = json.dumps(dado)

                                                    requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}',headers=header, data=st)

                                                pagini(driver, link)
                                                proxpage(driver)
                                                proxpage(driver)
                                                proxpage(driver)
                                                proxpage(driver)
                                                proxpage(driver)
                                                proxpage(driver)
                                                proxpage(driver)
                                                proxpage(driver)
                                                proxpage(driver)
                                                proxpage(driver)
                                                try:
                                                    #page12
                                                    driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]')
                                                    proxpage(driver)

                                                    dados12 = varrer(driver)
                                                    sleep(1)

                                                    for dado in dados12:
                                                        st = json.dumps(dado)

                                                        requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}',headers=header, data=st)

                                                    pagini(driver, link)
                                                    proxpage(driver)
                                                    proxpage(driver)
                                                    proxpage(driver)
                                                    proxpage(driver)
                                                    proxpage(driver)
                                                    proxpage(driver)
                                                    proxpage(driver)
                                                    proxpage(driver)
                                                    proxpage(driver)
                                                    proxpage(driver)
                                                    proxpage(driver)
                                                    try:
                                                        #page13
                                                        driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]')
                                                        proxpage(driver)

                                                        dados13 = varrer(driver)
                                                        sleep(1)

                                                        for dado in dados13:
                                                            st = json.dumps(dado)

                                                            requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}',headers=header, data=st)

                                                        pagini(driver, link)
                                                        proxpage(driver)
                                                        proxpage(driver)
                                                        proxpage(driver)
                                                        proxpage(driver)
                                                        proxpage(driver)
                                                        proxpage(driver)
                                                        proxpage(driver)
                                                        proxpage(driver)
                                                        proxpage(driver)
                                                        proxpage(driver)
                                                        proxpage(driver)
                                                        proxpage(driver)
                                                        try:
                                                            #page14
                                                            driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]')
                                                            proxpage(driver)

                                                            dados14 = varrer(driver)
                                                            sleep(1)

                                                            for dado in dados14:
                                                                st = json.dumps(dado)

                                                                requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}',headers=header, data=st)

                                                            pagini(driver, link)
                                                            proxpage(driver)
                                                            proxpage(driver)
                                                            proxpage(driver)
                                                            proxpage(driver)
                                                            proxpage(driver)
                                                            proxpage(driver)
                                                            proxpage(driver)
                                                            proxpage(driver)
                                                            proxpage(driver)
                                                            proxpage(driver)
                                                            proxpage(driver)
                                                            proxpage(driver)
                                                            proxpage(driver)
                                                            try:
                                                                #page15
                                                                driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]')
                                                                proxpage(driver)

                                                                dados15 = varrer(driver)
                                                                sleep(1)

                                                                for dado in dados15:
                                                                    st = json.dumps(dado)

                                                                    requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}',headers=header, data=st)

                                                                pagini(driver, link)
                                                                proxpage(driver)
                                                                proxpage(driver)
                                                                proxpage(driver)
                                                                proxpage(driver)
                                                                proxpage(driver)
                                                                proxpage(driver)
                                                                proxpage(driver)
                                                                proxpage(driver)
                                                                proxpage(driver)
                                                                proxpage(driver)
                                                                proxpage(driver)
                                                                proxpage(driver)
                                                                proxpage(driver)
                                                                proxpage(driver)
                                                                try:
                                                                    #page16
                                                                    driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]')
                                                                    proxpage(driver)

                                                                    dados16 = varrer(driver)
                                                                    sleep(1)

                                                                    for dado in dados16:
                                                                        st = json.dumps(dado)

                                                                        requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}',headers=header, data=st)

                                                                    pagini(driver, link)
                                                                    proxpage(driver)
                                                                    proxpage(driver)
                                                                    proxpage(driver)
                                                                    proxpage(driver)
                                                                    proxpage(driver)
                                                                    proxpage(driver)
                                                                    proxpage(driver)
                                                                    proxpage(driver)
                                                                    proxpage(driver)
                                                                    proxpage(driver)
                                                                    proxpage(driver)
                                                                    proxpage(driver)
                                                                    proxpage(driver)
                                                                    proxpage(driver)
                                                                    proxpage(driver)
                                                                    try:
                                                                        #page17
                                                                        driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]')
                                                                        proxpage(driver)

                                                                        dados17 = varrer(driver)
                                                                        sleep(1)

                                                                        for dado in dados17:
                                                                            st = json.dumps(dado)

                                                                            requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}',headers=header, data=st)
                                                                            
                                                                        
                                                                    except:
                                                                        next
                                                                except:
                                                                    next
                                                            except:
                                                                next
                                                        except:
                                                            next
                                                    except:
                                                        next
                                                except:
                                                    next
                                            except:
                                                next
                                        except:
                                            next
                                    except:
                                        next
                                except:
                                    next
                            except:
                                next
                        except:
                            next
                    except:
                        next

                except:
                    next
            except:
                next
        except:
            next
    







scrapy_agro()
