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

    driver.execute_script('window.scrollTo(0, 300);')
    sleep(2)

    driver.find_element(By.XPATH,'//*[@id="DataInicial"]').click()
    sleep(2)
        
    driver.find_element(By.XPATH,'//th[@class="today"]').click()
    sleep(3)

    driver.find_element(By.XPATH,'//*[@id="btnEnviarFiltroGeral-5231"]').click()
    sleep(1)

    driver.execute_script('window.scrollTo(0, 2200);')
    sleep(2)

    try:
        #page2
        driver.find_element(By.XPATH,'//i[@class="icon-angle-right"]').click()
        sleep(1)    
        print('data atual')
    except:
        print('negative')

driver = iniciar_driver()
link = 'https://www.agrolink.com.br/cotacoes/graos/arroz/'

pagini2(driver, link)


pagini2(driver, link)
            sleep(1)
            proxpage(driver)

            try:
                #page3
                driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]').click()
                sleep(1)

                dados3 = varree2(driver)

                for item in dados3:

                    if item['Preco'] == '':
                        print(item)
                    else:

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
                        if item['Preco'] == '':
                            print(item)
                        else:

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

                            if item['Preco'] == '':
                                print(item)
                            else:

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

                                if item['Preco'] == '':
                                    print(item)
                                else:

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

                                    if item['Preco'] == '':
                                        print(item)
                                    else:

                                        st = json.dumps(item)

                                        requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}', headers=header, data=st)
                                    
                                pagini2(driver, link)
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

                                    dados8 = varree2(driver)

                                    for item in dados8:

                                        if item['Preco'] == '':
                                            print(item)
                                        else:

                                            st = json.dumps(item)

                                            requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}', headers=header, data=st)

                                    pagini2(driver, link)
                                    sleep(1)
                                    proxpage(driver)
                                    proxpage(driver)
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

                                            if item['Preco'] == '':
                                                print(item)
                                            else:

                                                st = json.dumps(item)

                                                requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}', headers=header, data=st)
                                                    
                                        pagini2(driver, link)
                                        sleep(1)
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
                                            driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]').click()
                                            sleep(1)

                                            dados10 = varree2(driver)

                                            for item in dados10:

                                                if item['Preco'] == '':
                                                    print(item)
                                                else:

                                                    st = json.dumps(item)

                                                    requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}', headers=header, data=st)

                                            pagini2(driver, link)
                                            sleep(1)
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
                                                driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]').click()
                                                sleep(1)

                                                dados11 = varree2(driver)

                                                for item in dados11:

                                                    st = json.dumps(item)

                                                    requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}', headers=header, data=st)

                                                pagini2(driver, link)
                                                sleep(1)
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
                                                    driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]').click()
                                                    sleep(1)

                                                    dados12 = varree2(driver)

                                                    for item in dados12:

                                                        st = json.dumps(item)

                                                        requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}', headers=header, data=st)
                                                                            
                                                    pagini2(driver, link)
                                                    sleep(1)
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
                                                        driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]').click()
                                                        sleep(1)

                                                        dados13 = varree2(driver)

                                                        for item in dados13:

                                                            st = json.dumps(item)

                                                            requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}', headers=header, data=st)
                                                                                    
                                                        pagini2(driver, link)
                                                        sleep(1)
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
                                                            driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]').click()
                                                            sleep(1)

                                                            dados14 = varree2(driver)

                                                            for item in dados14:

                                                                st = json.dumps(item)

                                                                requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}', headers=header, data=st)
                                                                                            
                                                            pagini2(driver, link)
                                                            sleep(1)
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
                                                                driver.find_element(By.XPATH,'//*[@id="dvPaginacao"]/ul/li/a/i[@class="icon-angle-right"]').click()
                                                                sleep(1)

                                                                dados15 = varree2(driver)

                                                                for item in dados15:

                                                                    st = json.dumps(item)

                                                                    requests.post(f'https://api-cotacoes.agrolivrebrasil.com/pos/{nome}', headers=header, data=st)
                                                                                                    
                                                                
                                                            except:
                                                                print(f'Finalizei:{nome},pag-14')
                                                                next
                                                            
                                                        except:
                                                            print(f'Finalizei:{nome},pag-13')
                                                            next

                                                    except:
                                                        print(f'Finalizei:{nome},pag-12')
                                                        next
                                                except:
                                                    print(f'Finalizei:{nome},pag-11')
                                                    next
                                                
                                            except:
                                                print(f'Finalizei:{nome},pag-10')
                                                next

                                        except:
                                            print(f'Finalizei:{nome},pag-9')
                                            next

                                    except:
                                            print(f'Finalizei:{nome},pag-8')
                                            next

                                except:
                                    print(f'Finalizei:{nome},pag-7')
                                    next

                            except:
                                print(f'Finalizei:{nome},pag-6')
                                next

                        except:
                            print(f'Finalizei:{nome},pag-5')
                            next

                    except:
                        print(f'Finalizei:{nome},pag-4')
                        next

                except:
                    print(f'Finalizei:{nome},pag-3')
                    next

            except:
                print(f'Finalizei:{nome},pag-2')
                next