import json
import schedule
import requests
from lxml import etree
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup




tipos_algodao = ['/algodao-em-caroco-1ton','/algodao-em-pluma-15kg']

ufs = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS','MT',
    'PA','PB','PE','PI', 'PR','RJ','RN','RO','RR','RS','SC','SE','SP','TO']


header = {
    'Content-Type': 'application/json'
}


def scrap(tipo, itemrq):

    for uf in ufs:
        link = f'https://www.agrolink.com.br/cotacoes/historico/{uf}/{tipo}'
        page = requests.get(link,headers=header)

        soup = BeautifulSoup(page.content, 'html.parser')

        dom = etree.HTML(str(soup))

        data = (dom.xpath('/html/body/div[1]/main/div/div/div/div[1]/div[5]/div/div/div/table/tbody/tr/th/text()'))
        estadual = (dom.xpath('/html/body/div[1]/main/div/div/div/div[1]/div[5]/div/div/div/table/tbody/tr/td[1]/text()'))
        nacional = (dom.xpath('/html/body/div[1]/main/div/div/div/div[1]/div[5]/div/div/div/table/tbody/tr/td[2]/text()'))
        
        
        if data != []:

            estado = uf
            nom = tipo.split('/')
            nome = nom[1]
            
            dados = []

            for dat, estadua, naciona in zip(data, estadual, nacional):

                dados.append({"Item": nome,"Estado": estado,"Data": dat,"Estadual": estadua,"Nacional": naciona})



            itens = []

            for dado in dados:
                item = dado['Item']
                estado = dado['Estado']
                data = dado['Data']
                estadual = dado['Estadual']
                nacional = dado['Nacional']

                itens.append([item, estado, data, estadual, nacional])
                print([item, estado, data, estadual, nacional])




            



for tipo in tipos_algodao:

    itemrq = 'algodao'
    scrap(tipo, itemrq)