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


dda = datetime.today()
da = str(dda).split(' ')
dataa = da[0].split('-')

stt = dataa[2]
ontem = int(stt) - 1
data_ontem = f'{ontem}/{dataa[1]}/{dataa[0]}'
data_hoje = f'{dataa[2]}/{dataa[1]}/{dataa[0]}'



option = Options()
def iniciar_driver():
    chrome_options = Options()

    arguments = ['--window-size=800,600',
                 '--incognito', '--disable-gpu', '--no-sandbox', '--headless', '--disable-dev-shm-usage']

    for argument in arguments:
        chrome_options.add_argument(argument)
    chrome_options.headless = True
    chrome_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1

    })
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=chrome_options)

    return driver


#INFORMACOES CAPTADAS

urls1= [
    {'boi,https://www.agrolink.com.br/cotacoes/carnes/,Bovinos,Boi Gordo 15Kg'},
    {'vaca,https://www.agrolink.com.br/cotacoes/carnes/,Bovinos,Vaca Gorda 15Kg'}
]


urls2 = [
    {'arroz,https://www.agrolink.com.br/cotacoes/graos/arroz'},
    {'algodao,https://www.agrolink.com.br/cotacoes/diversos/algodao'},
    {'amendoim,https://www.agrolink.com.br/cotacoes/diversos/amendoim'},
    {'cafe,https://www.agrolink.com.br/cotacoes/graos/cafe'},
    {'cana,https://www.agrolink.com.br/cotacoes/diversos/cana-de-acucar'},
    {'feijao,https://www.agrolink.com.br/cotacoes/graos/feijao'},
    {'milho,https://www.agrolink.com.br/cotacoes/graos/milho'},
    {'soja,https://www.agrolink.com.br/cotacoes/graos/soja'},
    {'sorgo,https://www.agrolink.com.br/cotacoes/graos/sorgo'},
    {'trigo,https://www.agrolink.com.br/cotacoes/graos/trigo'},
    {'suinos,https://www.agrolink.com.br/cotacoes/carnes/suinos'},
    {'aves,https://www.agrolink.com.br/cotacoes/carnes/aves'},
    {'caprinos,https://www.agrolink.com.br/cotacoes/carnes/caprinos'},
    {'ovinos,https://www.agrolink.com.br/cotacoes/carnes/ovinos'},
    {'beterraba,https://www.agrolink.com.br/cotacoes/hortalicas/beterraba'},
    {'tomate,https://www.agrolink.com.br/cotacoes/hortalicas/tomate'},
    {'pimentao,https://www.agrolink.com.br/cotacoes/hortalicas/pimentao'},
    {'cebola,https://www.agrolink.com.br/cotacoes/diversos/cebola'},
    {'couve,https://www.agrolink.com.br/cotacoes/hortalicas/couve'},
    {'cenoura,https://www.agrolink.com.br/cotacoes/hortalicas/cenoura'},
]


#DADOS PARA O BOT ABAIXO

header = {
    'Content-Type': 'application/json'
    }

ufs = ['AC','AL','AM','AP','BA','CE','DF','ES','GO','MA','MG','MS','MT','PA','PB','PE','PI',
    'PR','RJ','RN','RO','RR','RS','SC','SE','SP','TO']

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


pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


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

                requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/mes/{itemrq}', headers=header, data=payl)
                    


def varre(driver, uf, link, tipo1, tipo2):

    itens = []

    driver.get(link)

    driver.execute_script('window.scrollTo(0, 50);')
    sleep(2)

    el = driver.find_element(By.XPATH,'//*[@id="FiltroCotacoesEspecie"]')
    els = Select(el)
    sleep(2)

    els.select_by_visible_text(tipo1)
    sleep(1)

    ti = driver.find_element(By.XPATH,'//*[@id="FiltroCotacoesProduto"]')
    tipos = Select(ti)
    sleep(2)

    tipos.select_by_visible_text(tipo2)
    sleep(1)

    est = driver.find_element(By.XPATH,'//*[@id="FiltroGeoEstado"]')
    estados = Select(est)
    sleep(2)

    estados.select_by_visible_text(uf)
    sleep(1)

    driver.find_element(By.XPATH,'//*[@id="DataInicial"]').click()
    sleep(2)
        
    try:
        driver.find_element(By.XPATH,'/html/body/div[5]/div[1]/table/tfoot/tr[1]/th').click()
        sleep(3)

    except:
        return



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
        
    except:
        next

    return itens

def varree(driver):

    itens = []

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
    

    return itens

def pagini(driver, uf, link, tipo1, tipo2):
    driver.get(link)

    driver.execute_script('window.scrollTo(0, 50);')
    sleep(2)

    el = driver.find_element(By.XPATH,'//*[@id="FiltroCotacoesEspecie"]')
    els = Select(el)
    sleep(2)

    els.select_by_visible_text(tipo1)
    sleep(1)

    ti = driver.find_element(By.XPATH,'//*[@id="FiltroCotacoesProduto"]')
    tipos = Select(ti)
    sleep(2)

    tipos.select_by_visible_text(tipo2)
    sleep(1)

    est = driver.find_element(By.XPATH,'//*[@id="FiltroGeoEstado"]')
    estados = Select(est)
    sleep(2)

    estados.select_by_visible_text(uf)
    sleep(1)

    driver.find_element(By.XPATH,'//*[@id="DataInicial"]').click()
    sleep(2)
        
    driver.find_element(By.XPATH,'/html/body/div[5]/div[1]/table/tfoot/tr[1]/th').click()
    sleep(3)

    driver.find_element(By.XPATH,'//*[@id="btnEnviarFiltroGeral-5231"]').click()
    sleep(1)

    driver.execute_script('window.scrollTo(0, 1900);')


def crawlAgro1():

    driver = iniciar_driver()

    login(driver)
    sleep(1)

    for url in urls1:

        item = str(url)
        it = item.split(',')

        nom = it[0].split("'")
        nome = nom[1]

        lin = it[1].split("'")
        link = lin[0]

        tip1 = it[2].split("'")
        tipo1 = tip1[0]

        tip2 = it[3].split("'")
        tipo2 = tip2[0]



        for uf in ufs:

            print(f'Varrendo: {nome} no {uf}')

            dados = varre(driver, uf, link, tipo1, tipo2)

            for item in dados:

                st = json.dumps(item)

                requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}', headers=header, data=st)

            pagini(driver, uf, link, tipo1, tipo2)
            sleep(1)

            try:
                #page2
                driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]').click()
                sleep(1)

                dados2 = varree(driver)

                for item in dados2:

                    st = json.dumps(item)

                    requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}', headers=header, data=st)

                pagini(driver, uf, link, tipo1, tipo2)
                sleep(1)
                proxpage(driver)

                try:
                    #page3
                    driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]').click()
                    sleep(1)

                    dados3 = varree(driver)

                    for item in dados3:

                        st = json.dumps(item)

                        requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}', headers=header, data=st)

                    pagini(driver, uf, link, tipo1, tipo2)
                    sleep(1)
                    proxpage(driver)
                    proxpage(driver)

                    try:
                        #page4
                        driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]').click()
                        sleep(1)

                        dados4 = varree(driver)

                        for item in dados4:

                            st = json.dumps(item)

                            requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}', headers=header, data=st)

                        pagini(driver, uf, link, tipo1, tipo2)
                        sleep(1)
                        proxpage(driver)
                        proxpage(driver)
                        proxpage(driver)

                        try:
                            #page5
                            driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]').click()
                            sleep(1)

                            dados5 = varree(driver)

                            for item in dados5:

                                st = json.dumps(item)

                                requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}', headers=header, data=st)

                            pagini(driver, uf, link, tipo1, tipo2)
                            sleep(1)
                            proxpage(driver)
                            proxpage(driver)
                            proxpage(driver)
                            proxpage(driver)

                            try:
                                #page6
                                driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]').click()
                                sleep(1)

                                dados6 = varree(driver)

                                for item in dados6:

                                    st = json.dumps(item)

                                    requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}', headers=header, data=st)

                                pagini(driver, uf, link, tipo1, tipo2)
                                sleep(1)
                                proxpage(driver)
                                proxpage(driver)
                                proxpage(driver)
                                proxpage(driver)
                                proxpage(driver)

                                try:
                                    #page7
                                    driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]').click()
                                    sleep(1)

                                    dados7 = varree(driver)

                                    for item in dados7:

                                        st = json.dumps(item)

                                        requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}', headers=header, data=st)
                                    
                                    pagini(driver, uf, link, tipo1, tipo2)
                                    sleep(1)
                                    proxpage(driver)
                                    proxpage(driver)
                                    proxpage(driver)
                                    proxpage(driver)
                                    proxpage(driver)
                                    proxpage(driver)

                                    try:
                                        #page8
                                        driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]').click()
                                        sleep(1)

                                        dados8 = varree(driver)

                                        for item in dados8:

                                            st = json.dumps(item)

                                            requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}', headers=header, data=st)

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
            
            print(f'Finalizei:{uf}')




def varre2(driver, link):

    itens = []

    driver.get(link)

    driver.execute_script('window.scrollTo(0, 290);')
    sleep(2)

    driver.find_element(By.XPATH,'//*[@id="DataInicial"]').click()
    sleep(2)
        
    try:
        driver.find_element(By.XPATH,'/html/body/div[5]/div[1]/table/tfoot/tr[1]/th').click()
        sleep(3)

    except:
        return


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
        
    except:
        next

    return itens

def varree2(driver):

    itens = []

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
    

    return itens

def pagini2(driver, link):
    driver.get(link)

    driver.execute_script('window.scrollTo(0, 290);')
    sleep(2)

    driver.find_element(By.XPATH,'//*[@id="DataInicial"]').click()
    sleep(2)
        
    driver.find_element(By.XPATH,'/html/body/div[5]/div[1]/table/tfoot/tr[1]/th').click()
    sleep(3)

    driver.find_element(By.XPATH,'//*[@id="btnEnviarFiltroGeral-5231"]').click()
    sleep(1)

    driver.execute_script('window.scrollTo(0, 1900);')


def crawlAgro2():

    driver = iniciar_driver()

    login(driver)
    sleep(1)


    for url in urls2:

        item = str(url)
        it = item.split(',')

        nom = it[0].split("'")
        nome = nom[1]

        lin = it[1].split("'")
        link = lin[0]


        print(f'Varrendo: {nome}')

        dados = varre2(driver, link)

        for item in dados:

            st = json.dumps(item)

            requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}', headers=header, data=st)

        pagini2(driver, link)
        sleep(1)

        try:
            #page2
            driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]').click()
            sleep(1)

            dados2 = varree2(driver)

            for item in dados2:

                st = json.dumps(item)

                requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}', headers=header, data=st)

            pagini2(driver, link)
            sleep(1)
            proxpage(driver)

            try:
                #page3
                driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]').click()
                sleep(1)

                dados3 = varree2(driver)

                for item in dados3:

                    st = json.dumps(item)

                    requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}', headers=header, data=st)

                pagini2(driver, link)
                sleep(1)
                proxpage(driver)
                proxpage(driver)

                try:
                    #page4
                    driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]').click()
                    sleep(1)

                    dados4 = varree2(driver)

                    for item in dados4:

                        st = json.dumps(item)

                        requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}', headers=header, data=st)

                    pagini2(driver, link)
                    sleep(1)
                    proxpage(driver)
                    proxpage(driver)
                    proxpage(driver)

                    try:
                        #page5
                        driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]').click()
                        sleep(1)

                        dados5 = varree2(driver)

                        for item in dados5:

                            st = json.dumps(item)

                            requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}', headers=header, data=st)

                        pagini2(driver, link)
                        sleep(1)
                        proxpage(driver)
                        proxpage(driver)
                        proxpage(driver)
                        proxpage(driver)

                        try:
                            #page6
                            driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]').click()
                            sleep(1)

                            dados6 = varree2(driver)

                            for item in dados6:

                                st = json.dumps(item)

                                requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}', headers=header, data=st)

                            pagini2(driver, link)
                            sleep(1)
                            proxpage(driver)
                            proxpage(driver)
                            proxpage(driver)
                            proxpage(driver)
                            proxpage(driver)

                            try:
                                #page7
                                driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]').click()
                                sleep(1)

                                dados7 = varree2(driver)

                                for item in dados7:

                                    st = json.dumps(item)

                                    requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}', headers=header, data=st)
                
                                pagini2(driver, link)
                                sleep(1)
                                proxpage(driver)
                                proxpage(driver)
                                proxpage(driver)
                                proxpage(driver)
                                proxpage(driver)
                                try:
                                    #page8
                                    driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]').click()
                                    sleep(1)

                                    dados8 = varree2(driver)

                                    for item in dados8:

                                        st = json.dumps(item)

                                        requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}', headers=header, data=st)
                                    
                                    pagini2(driver, link)
                                    sleep(1)
                                    proxpage(driver)
                                    proxpage(driver)
                                    proxpage(driver)
                                    proxpage(driver)
                                    proxpage(driver)

                                    try:
                                        #page9
                                        driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]').click()
                                        sleep(1)

                                        dados9 = varree2(driver)

                                        for item in dados9:

                                            st = json.dumps(item)

                                            requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}', headers=header, data=st)
                        
                                        pagini2(driver, link)
                                        sleep(1)
                                        proxpage(driver)
                                        proxpage(driver)
                                        proxpage(driver)
                                        proxpage(driver)
                                        proxpage(driver)

                                        try:
                                            #page10
                                            driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]').click()
                                            sleep(1)

                                            dados10 = varree2(driver)

                                            for item in dados10:

                                                st = json.dumps(item)

                                                requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}', headers=header, data=st)

                                            pagini2(driver, link)
                                            sleep(1)
                                            proxpage(driver)
                                            proxpage(driver)
                                            proxpage(driver)
                                            proxpage(driver)
                                            proxpage(driver)

                                            try:
                                                #page11
                                                driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]').click()
                                                sleep(1)

                                                dados11 = varree2(driver)

                                                for item in dados11:

                                                    st = json.dumps(item)

                                                    requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}', headers=header, data=st)
                                

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
            
        print(f'Finalizei:{nome}')



def crawlAlface(driver):
    driver.get('https://www.noticiasagricolas.com.br/cotacoes/verduras/alface-ceasas')

    texto = driver.find_element(By.XPATH,'//*[@id="content"]/div[3]/div[3]/div[1]/div[1]/div').text
    data_cotacao = texto.split(' ')
    dia_cotacao = data_cotacao[1]

    if dia_cotacao == data_ontem:

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
                preco = int(prec)

            
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

        for dado in dados:
            st = json.dumps(dado)

            requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/alface',headers=header, data=st)

    else:
        next


def crawlRepolho(driver):

    print('repolho')
    driver.get('https://www.noticiasagricolas.com.br/cotacoes/verduras/repolho-ceasas')

    texto = driver.find_element(By.XPATH,'//*[@id="content"]/div[3]/div[3]/div[1]/div[1]/div').text
    data_cotacao = texto.split(' ')
    dia_cotacao = data_cotacao[1]


    if dia_cotacao == data_ontem:
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
                preco = int(prec)

            
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


        estado3 = linha7['item']

        item4 = linha6['item']
        preco4 = linha6['valor']

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

        for dado in dados:
            st = json.dumps(dado)

            requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/repolho',headers=header, data=st)
    else:
        next



def proxpage(driver):
    driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]').click()
    sleep(1)
    driver.execute_script('window.scrollTo(0, 1900);')
    sleep(1)



def crawlNoticiasAgricolas():
    
    referencia = 'agricolas'

    driver = iniciar_driver()

    driver.get('https://www.noticiasagricolas.com.br/noticias/agronegocio/')
    sleep(2)

    dia_cotacao = driver.find_element(By.XPATH,'//*[@id="content"]/div[2]/h3[1]').text


    if dia_cotacao == data_hoje:

        itens = driver.find_elements(By.XPATH,'//*[@id="content"]/div[2]/ul[1]/li')

        dados = []

        for item in itens:
            link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
            hora = item.find_element(By.TAG_NAME, 'span').text
            titulo = item.find_element(By.TAG_NAME, 'h2').text

            dados.append([titulo, link, hora, data_hoje, referencia, referencia])

        bd = requests.get('https://api-cotacoes.agrolivrebrasil.com/noticias/agricolas')

        tb = json.loads(bd.content)

        
        for novo in dados:
           if novo not in tb:
                payl = {
                    "Titulo": novo[0],
                    "Link": novo[1],
                    "Hora": novo[2],
                    "Data": novo[3],
                    "Referencia": novo[4],
                    "Categoria": novo[5]
                }

                st = json.dumps(payl)
                
                requests.post('https://api-cotacoes.agrolivrebrasil.com/pos/noticias/agricolas', headers=header, data=st)

def crawlNoticiasAgrolink():
        
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
            
                requests.post('https://api-cotacoes.agrolivrebrasil.com/pos/noticias/agrolink', headers=header, data=st)
    
def crawlNoticiasCanalRural():
      
    referencia = 'Canal Rural'

    page = requests.get('https://www.canalrural.com.br/noticias')

    soup = BeautifulSoup(page.content, 'html.parser')

    dom = etree.HTML(str(soup))

    titulo = (dom.xpath('//*[@id="mobile"]/div/div[2]/div/div/div/div/div/div[1]/div/div/div/div/div[2]/h2/a/text()'))
    link = (dom.xpath('//*[@id="mobile"]/div/div[2]/div/div/div/div/div/div[1]/div/div/div/div/div[2]/h2/a/@href'))
    dat = (dom.xpath('//*[@id="mobile"]/div/div[2]/div/div/div/div/div/div[1]/div/div/div[5]/div/div[2]/div/text()'))
    data = []
    hora = []

    for dat in dat:
        datt = str(dat).split(' às ')
        horraa = datt[1]
        horaa = horraa.split('h')
        datta = datt[0].split('\n')
        minuto = horaa[1].split('\n')

        data.append(datta[1])
        hora.append(f'{horaa[0]}:{minuto[0]}')

    novos = []
    
    for titulo, link, data, hora in zip(titulo, link, data, hora):
        novos.append([titulo, link, hora, data, referencia, referencia])
        

    bd = requests.get('https://api-cotacoes.agrolivrebrasil.com/noticias/canalrural')

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
            
                requests.post('https://api-cotacoes.agrolivrebrasil.com/pos/noticias/canalrural', headers=header, data=st)
         



def scrapy_tabela():

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
    crawlAgro1()
    crawlAgro2()
    crawlAlface()
    crawlRepolho()


def run_threaded(job):
    job_thread = threading.Thread(target=job)
    job_thread.start()

schedule.every().monday.do(run_threaded, scrapy_tabela)
schedule.every().day.at("02:00").do(run_threaded, scrapy_precos)
schedule.every().day.at("09:10").do(run_threaded, scrapy_precos)
schedule.every(1).minutes.do(run_threaded, scrapy_noticias)



while 1:
    schedule.run_pending()
    sleep(1)
