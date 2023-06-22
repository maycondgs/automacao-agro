from datetime import datetime

dda = datetime.today()
da = str(dda).split(' ')
data = da[0].split('-')
dia = data[2]

print(dia)