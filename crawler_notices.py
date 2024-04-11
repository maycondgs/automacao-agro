import schedule
import requests
from lxml import etree
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup
import mysql.connector
import os

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

dda = datetime.today()
da = str(dda).split(' ')
dataa = da[0].split('-')
data = f'{dataa[2]}/{dataa[1]}/{dataa[0]}'
data_hoje = da[0]



db = mysql.connector.connect(
    user='root',
    password='63d08ecd4c92b34acf3b',
    host = '5.161.188.61',
    port = '7129',
    database='agrolivre'
)



dda = datetime.today()
da = str(dda).split(' ')
dataa = da[0].split('-')
date_now_format = f'{dataa[2]}/{dataa[1]}/{dataa[0]}'
date_now = da[0]


def crawlNoticiasAgricolas(cursor):
    
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
        if "'" in titu:
            titu = titu.replace("'", "")
        
        novos.append([titu, lnk, hora, datafim, referencia, referencia])

    
    sql = f"SELECT * FROM notices_agricolas"

    cursor.execute(sql)
    ext = cursor.fetchall()

    linksat = []
    for it in ext:
        linksat.append(it[2])
    
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

            sql = f"INSERT INTO notices_agricolas (title, link, time_publication, date_publication, referency, category) VALUES ('{payl['Titulo']}', '{payl['Link']}', '{payl['Hora']}', '{payl['Data']}', '{payl['Referencia']}', '{payl['Categoria']}')"
            cursor.execute(sql)
            db.commit()


def crawlNoticiasAgrolink(cursor):
        
    novos = []   

    links = ['https://www.agrolink.com.br/noticias/categoria/agricultura/lista','https://www.agrolink.com.br/noticias/categoria/pecuaria/lista', 'https://www.agrolink.com.br/noticias/categoria/economia/lista','https://www.agrolink.com.br/noticias/categoria/politica/lista', 'https://www.agrolink.com.br/noticias/categoria/tecnologia/lista']

    for link in links:
        lnnk = link.split('/')
        categoria = lnnk[5]
        referencia = 'agrolink'
        
        page = requests.get(link)

        soup = BeautifulSoup(page.content, 'html.parser')

        dom = etree.HTML(str(soup))


        links2 = (dom.xpath('/html/body/div[1]/main/div/div/div/div[1]/section/div/ul/li/article/div/div[2]/a[1]/@href'))
        titulo = (dom.xpath('/html/body/div[1]/main/div/div/div/div[1]/section/div/ul/li/article/div/div[2]/a[1]/h4/text()'))
        datt = (dom.xpath('/html/body/div[1]/main/div/div/div/div[1]/section/div/ul/li/article/div/div[2]/a[2]/text()'))

        lnks2 = []
        data = []
        hora = []
        

        for da in datt:
            dattt = da.split(' ')
            datt = str(dattt[2]).split('/')
            data.append(f'{datt[2]}-{datt[1]}-{datt[0]}')
            hora.append(dattt[3].strip())

        for lnk in links2:
            lnks2.append(f'https://www.agrolink.com.br{lnk}')



        for titu, link, data, hora in zip(titulo, lnks2, data, hora):
            if "'" in titu:
                titu = titu.replace("'", "")

            novos.append([titu, link, hora, data, referencia, categoria])

        
        
    sql = f"SELECT * FROM notices_agrolink"

    cursor.execute(sql)
    ext = cursor.fetchall()

    linksat = []
    for it in ext:
        linksat.append(it[2])
        
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

            sql = f"INSERT INTO notices_agrolink (title, link, time_publication, date_publication, referency, category) VALUES ('{payl['Titulo']}', '{payl['Link']}', '{payl['Hora']}', '{payl['Data']}', '{payl['Referencia']}', '{payl['Categoria']}')"
            cursor.execute(sql)
            db.commit()
            

def crawlNoticiasCanalRural(cursor): 
            
    novos =[]

    referencia = 'Canal Rural'

    page = requests.get('https://www.canalrural.com.br/ultimas-noticias/')
    
    soup = BeautifulSoup(page.content, 'html.parser')
    dom = etree.HTML(str(soup))

    links = (dom.xpath('/html/body/main/div[2]/div/div[1]/div/article/a/@href'))

    for link in links:
        page1 = requests.get(link)
    
        soup1 = BeautifulSoup(page1.content, 'html.parser')
        dom1 = etree.HTML(str(soup1))

        titu = (dom1.xpath('/html/body/main/section[1]/div/div[1]/div/h1/text()'))
        titulo = titu[0].strip()

        categ = (dom1.xpath('/html/body/main/section[1]/div/div[1]/div/p/text()'))
        categoria = categ[0].strip()


        dat = (dom1.xpath('/html/body/main/section[1]/div/div[2]/div[2]/time/text()'))
        datt = dat[1].split('\n')
        dattt = datt[1].split()

        dattn = dattt[0].strip()
        datan = dattn.split('/')
        data = f'{datan[2]}-{datan[1]}-{datan[0]}'
        hora = f'{dattt[1]}:00'

        if "'" in titulo:
            titulo = titulo.replace("'", "")

        novo = [titulo, link, hora, data, referencia, categoria]

        novos.append(novo)
    
    
    sql = f"SELECT * FROM notices_canal_rural"

    cursor.execute(sql)
    ext = cursor.fetchall()

    linksat = []
    for it in ext:
        linksat.append(it[2])
    
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

            sql = f"INSERT INTO notices_canal_rural (title, link, time_publication, date_publication, referency, category) VALUES ('{payl['Titulo']}', '{payl['Link']}', '{payl['Hora']}', '{payl['Data']}', '{payl['Referencia']}', '{payl['Categoria']}')"
            cursor.execute(sql)
            db.commit()
            


def crawlerNoticias():
    cursor = db.cursor()
    crawlNoticiasAgricolas(cursor)
    crawlNoticiasAgrolink(cursor)
    crawlNoticiasCanalRural(cursor)


def send_mail():
    sender_email = "meuclash3333@gmail.com"
    sender_password = "mqzm swld bzsa hjau"
    recipient_email = "mayconclementino44@gmail.com"
    subject = "SUPORTE - DEV"
    body = "BUG APP AGROLIVRE - CRAWLER NOTICES"

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




def crawler():
    try:
        crawlerNoticias()
    except:
        send_mail()

schedule.every(1).minutes.do(crawler)

while True:
    schedule.run_pending()
    sleep(1)