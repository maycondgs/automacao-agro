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


dda = datetime.today()
da = str(dda).split(' ')
dataa = da[0].split('-')

stt = dataa[2]
ontem = int(stt) - 1
data_ontem = f'{ontem}/{dataa[1]}/{dataa[0]}'
data_hoje = f'{dataa[2]}/{dataa[1]}/{dataa[0]}'


ufs1 = ['PB','PE','PI','PR','RJ','RN','RO','RR','RS','SC','SE','SP','TO']
ufs2 = ['AC','AL','AM','AP','BA','CE','DF','ES','GO','MA','MG','MS','MT','PA',]

urls = [
    {'boi,https://www.agrolink.com.br/cotacoes/carnes/,Bovinos,Boi Gordo 15Kg'},
    {'vaca,https://www.agrolink.com.br/cotacoes/carnes/,Bovinos,Vaca Gorda 15Kg'}
]

def proxpage(driver):
    driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]').click()
    sleep(1)
    driver.execute_script('window.scrollTo(0, 1900);')
    sleep(1)



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

    for url in urls:

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



        for uf in ufs1:

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

        for uf in ufs2:

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


crawlAgro1()