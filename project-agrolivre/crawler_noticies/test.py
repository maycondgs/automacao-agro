import schedule
import requests
from lxml import etree
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup
import mysql.connector
import os



dda = datetime.today()
da = str(dda).split(' ')
dataa = da[0].split('-')
data = f'{dataa[2]}/{dataa[1]}/{dataa[0]}'
data_hoje = da[0]

db = mysql.connector.connect(
    user='marceloagrouser',
    password='zHXBNu99drvBzHXBNu99drvBTf0Exe3pTf0Exe3p',
    host = 'connection-agrolivre-542543.agrolivrebrasil.com',
    port = '45821',
    database='agrolivre'
)


data = []

cursor = db.cursor()

cursor.execute("""
    CREATE TABLE quotes_repolho (
        id INT AUTO_INCREMENT PRIMARY KEY,
        item VARCHAR(255),
        state VARCHAR(255),
        price VARCHAR(255),
        date_update DATE,
        date_scraping DATE
    )
""")

print('TABELA CRIADA')