estaddd = "Figueirópolis D'Oeste (MT)"
spl = '"'

nn = estaddd.count("'")

if nn >= 1: 
    estado = estaddd.replace("'", "")
    
else:
    estado = estaddd

print(estado)

    
