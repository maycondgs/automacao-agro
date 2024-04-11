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


cursor = db.cursor()




query = """
INSERT INTO notices_canal_rural (title, link, time_publication, date_publication, referency, category)) VALUES ('Boi de papel: Fraude milionária envolve gado fantasma', 'https://www.canalrural.com.br/pecuaria/boi/boi-de-papel-fraude-milionaria-envolve-gado-fantasma/', '20:26:00', '2024-03-07', 'Canal Rural', 'OPERAÇÃO')
"""

cursor.execute(query)

cursor.commit()
cursor.close()

print('CRIADA')