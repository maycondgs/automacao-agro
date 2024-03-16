import json
import requests
import schedule
import threading 
from lxml import etree
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup
import mysql.connector

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


db = mysql.connector.connect(
    user='marceloagrouser',
    password='zHXBNu99drvBzHXBNu99drvBTf0Exe3pTf0Exe3p',
    host = 'connection-agrolivre-542543.agrolivrebrasil.com',
    port = '45821',
    database='agrolivre'
)




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



ufs = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS','MT',
    'PA','PB','PE','PI', 'PR','RJ','RN','RO','RR','RS','SC','SE','SP','TO']


header = {
    'Content-Type': 'application/json'
}


def scrap(tipo, itemrq):

    itemcontent = tipo.split('/')
    itemcontent = itemcontent[1]

    for uf in ufs:
        link = f'https://www.agrolink.com.br/cotacoes/historico/{uf}{tipo}'
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


            cursor = db.cursor()
                    
            sql = f"SELECT * FROM quotes_month_{itemrq} WHERE type == {itemcontent}"

            cursor.execute(sql)
            ext = cursor.fetchall()

            datessat = []
            for it in ext:
                datessat.append(it[3])
            
            for novo in dados:
                if novo[2] not in datessat:

                    post(itemrq, novo)




def post(itemarq, item):
    cursor = db.cursor()
    sql = f"INSERT INTO quotes_month_{itemarq} (type, state, date, local, national) VALUES ('{item['Item']}', '{item['Estado']}', '{item['Data']}', '{item['Estadual']}', '{item['Nacional']}')"
    cursor.execute(sql)
    db.commit()


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


def send_mail():
    sender_email = "meuclash3333@gmail.com"
    sender_password = "mqzm swld bzsa hjau"
    recipient_email = "mayconclementino44@gmail.com"
    subject = "Python"
    body = "ERRO NA APLICACAO AGROLIVRE"

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


def scraping():
    try:
        scrapy_tabela()
    except:
        send_mail()
    


schedule.every().monday.do(scraping)


while True:
    schedule.run_pending()
    sleep(1)