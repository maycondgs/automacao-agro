from datetime import datetime

dda = datetime.today()
da = str(dda).split(' ')
dataa = da[0].split('-')
data = f'{dataa[2]}/{dataa[1]}/{dataa[0]}'
data_hoje = da[0]

print(data_hoje)