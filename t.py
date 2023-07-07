vaca = [
    {'vaca,https://www.agrolink.com.br/cotacoes/carnes/bovinos/vaca-gorda-15kg'}
]

for url in vaca:

        item = str(url)
        it = item.split(',')

        nom = it[0].split("'")
        nome = nom[1]

        lin = it[1].split("'")
        link = lin[0]

        print(link)