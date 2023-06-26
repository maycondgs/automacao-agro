urls = [
    {'cana,https://www.agrolink.com.br/cotacoes/diversos/cana-de-acucar/'},
]

for url in urls:

    item = str(url)
    it = item.split(',')

    nom = it[0].split("'")
    nome = nom[1]

    lin = it[1].split("'")
    link = lin[0]

    print(nome, link)