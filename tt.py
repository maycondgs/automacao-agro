import requests
import json
from lxml import etree
from bs4 import BeautifulSoup

header = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

referencia = 'Canal Rural'
dados = []

page = requests.get('https://www.canalrural.com.br/noticias/',headers=header)

soup = BeautifulSoup(page.content, 'html.parser')

dom = etree.HTML(str(soup))

links = (dom.xpath('//*[@class="info"]/h2/a/@href'))
titulos = (dom.xpath('//*[@class="info"]/h2/a/text()'))
datt = (dom.xpath('//div[@class="data-hora"]/text()'))
data = []
hora = []

for datta in datt:
    dattta = datta.strip()
    dat = str(dattta).split(' às ')
    ddat = str(dat[0]).split('/')
    dda = f'{ddat[2]}-{ddat[1]}-{ddat[0]}'
    data.append(dda)
    hor = str(f'{dat[1]}:00')
    horr = hor.replace('h',':')
    hora.append(horr)

for link,tit,data,hora in zip(links, titulos, data, hora):
    dados.append([tit, link, hora, data, referencia, referencia])


bd = requests.get('https://api-cotacoes.agrolivrebrasil.com/noticias/canalrural')

tb = json.loads(bd.content)

ext = []

for it in tb:
    ctd = it[0]
    ext.append(ctd)

for novo in dados:
    if novo[0] in ext:

        print(novo[1])