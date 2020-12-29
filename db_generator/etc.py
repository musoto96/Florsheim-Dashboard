import numpy as np
import pandas as pd


# Codigo FL0000X pares únicos.
accesorio = pd.read_csv('datos/bases/fs_zapato.csv', engine='python')
zapato = pd.read_csv('datos/bases/fs_accesorio.csv', engine='python')

#vbase = base.iloc[:, [9, -3]].groupby('NOTA DE VENTA NOTA')


print('\n\n\n\n\n')
print('################################# ZAPATO ##############################')
print(len(zapato))
print('\n\n\n\n\n')

for i in zapato:
    print(zapato[i].value_counts(), '\n')

print('\n\n\n\n\n')
print('################################# ACCESORIO ##############################')
print(len(accesorio))
print('\n\n\n\n\n')

for i in accesorio:
    print(accesorio[i].value_counts(), '\n')

