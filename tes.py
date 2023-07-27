codigos = [{'13,5,Todos,arroz'},{'11,8,Todos,algodao'},{'11,30,Todos,amendoim'},{'11,92,Todos,cana'},{'13,46,Todos,feijao'},{'13,2,Todos,milho'},{'13,1,Todos,soja'},{'13,31,Todos,sorgo'},{'10,144,Todos,suinos'},{'10,122,Todos,aves'},{'10,147,Todos,caprinos'},
    {'10,152,Todos,ovinos'},{'14,95,Todos,beterraba'},{'14,40,Todos,tomate'},{'14,51,Todos,pimentao'},{'11,24,Todos,cebola'},{'14,39,Todos,couve'},{'14,27,Todos,cenoura'},{'10,120,Boi Gordo 15Kg,boi'},{'10,120,Vaca Gorda 15Kg,vaca'}]
 
itemgrupo = '13'
itemespecie = '1'
itemproduto = 'Todos'
prodformat = 'soja'


for cod in codigos:

    item = str(cod)
    it = item.split(',')

    grp = it[0].split("'")
    itemgrupo = grp[1]
    itemespecie = it[1]
    itemproduto = it[2]
    fmt = it[3].split("'")
    prodformat = fmt[0]

    print(itemgrupo,itemespecie,itemproduto,prodformat)