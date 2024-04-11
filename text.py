links = ['algodao,https://www.agrolink.com.br/cotacoes/diversos/algodao/', 'arroz,https://www.agrolink.com.br/cotacoes/graos/arroz/', 'amendoim,https://www.agrolink.com.br/cotacoes/diversos/amendoim/', 'cafe,https://www.agrolink.com.br/cotacoes/graos/cafe/', 'cana,https://www.agrolink.com.br/cotacoes/diversos/cana-de-acucar/', 'feijao,https://www.agrolink.com.br/cotacoes/graos/feijao/' ,'milho,https://www.agrolink.com.br/cotacoes/graos/milho/', 'soja,https://www.agrolink.com.br/cotacoes/graos/soja/', 'sorgo,https://www.agrolink.com.br/cotacoes/graos/sorgo/', 'trigo,https://www.agrolink.com.br/cotacoes/graos/trigo/', 'suinos,https://www.agrolink.com.br/cotacoes/carnes/suinos/' ,'aves,https://www.agrolink.com.br/cotacoes/carnes/aves/', 'caprinos,https://www.agrolink.com.br/cotacoes/carnes/caprinos/', 'ovinos,https://www.agrolink.com.br/cotacoes/carnes/ovinos/', 'beterraba,https://www.agrolink.com.br/cotacoes/hortalicas/beterraba/', 'tomate,https://www.agrolink.com.br/cotacoes/hortalicas/tomate/', 'pimentao,https://www.agrolink.com.br/cotacoes/hortalicas/pimentao/', 'cebola,https://www.agrolink.com.br/cotacoes/diversos/cebola/', 'couve,https://www.agrolink.com.br/cotacoes/hortalicas/couve/', 'cenoura,https://www.agrolink.com.br/cotacoes/hortalicas/cenoura/', 'boi,https://www.agrolink.com.br/cotacoes/carnes/bovinos/boi-gordo-15kg', 'vaca,https://www.agrolink.com.br/cotacoes/carnes/bovinos/vaca-gorda-15kg']

for link in links:

    l = link.split(',')
    prodformat = l[0]
    link = l[1]
    print(prodformat)
