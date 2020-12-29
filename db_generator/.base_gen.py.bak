import numpy as np
import pandas as pd


# Codigo FL0000X pares únicos.
# Lectura de datos
base = pd.read_csv('../datos/bases/adm_finanzas/ventas_19-20.TXT', sep='\t', engine='python', encoding='latin_1')

# Transformacion y separación fecha/hora
base.iloc[:, 3] = pd.to_datetime(base.iloc[:, 3], format='%d/%m/%Y %H:%M')
base.insert(loc=0, column='fecha', value=base['NOTA DE VENTA FECHA'])
base.drop(columns=['NOTA DE VENTA FECHA'], inplace=True)
base.insert(loc=1, column='año', value=base['fecha'].dt.year)
base.insert(loc=2, column='mes', value=base['fecha'].dt.month)
base.insert(loc=3, column='ndia', value=base['fecha'].dt.day)
base.insert(loc=4, column='dia', value=base['fecha'].dt.day_name())
base.insert(loc=5, column='sndia', value=base['fecha'].dt.weekday)
base.sort_values(by=['fecha'], inplace=True)

# Revisión de fechas faltantes
fechas_unicas = pd.Index(data=base.loc[:, 'fecha'].dt.date[base['fecha'].duplicated(keep='first').apply(lambda x: not x)])

# Tiempo en operación
t_op = pd.Index(data=pd.date_range(start=min(base['fecha']), end=max(base['fecha']), freq='D').date)

# Faltantes
faltantes = t_op.difference(fechas_unicas)
faltantes = pd.DataFrame({'fecha': faltantes.to_series()}).reset_index(drop=True)
base = base.append(faltantes, ignore_index=True).sort_values(by='fecha').reset_index(drop=True)

# exploracion
'''
for i in base:
    print(base[i].describe())
    print('\n\n')
'''
base.drop(columns=['NOTA DE VENTA CAJA', 'ARTÍCULO MARCA'], inplace=True)
base['NOTA DE VENTA TOTAL'] = base['NOTA DE VENTA TOTAL'].apply(lambda x: x.replace(',','') if type(x) != float else np.nan)
base['ARTÍCULO TALLA'] = base['ARTÍCULO TALLA'].astype(str)

# aplicador
def like(x, d):
    for key, vals in d.items():
        for val in vals: 
            try: 
                if val in x.lower(): 
                    return key 
            except AttributeError:
                return np.nan
    return x


# variables numéricas de 0 -> nan
num_vars = ['ARTÍCULO PRECIO', 'ARTÍCULO IMPORTE', 'ARTÍCULO SUBTOTAL', 'FORMA DE PAGO IMPORTE']
for i in num_vars: 
    base[i].replace(0, np.nan, inplace=True)


# ARTÍCULO CONCEPTO
con = {
        'vestir': ['vestir', 'trabajo'], 
        'casual/vestir': ['casual', 'botas', 'bota'], 
        'confort': ['confort'], 
        'sport': ['sport', 'urbano'], 
        'consumibles': ['producto', 'crema', 'cera', 'limpiador', 'reavivador', 'renovador', 'avivador', 'dilatador', 'jabon', 'jabón', 'cepillo', 'esponja'], 
        'accesorios': ['cinturon', 'cinturón', 'calcetin', 'calcetín', 'cartera', 'mochila']
    }
cat = {
        'zapato': ['vestir', 'casual', 'confort', 'urbano', 'botas', 'bota', 'botin', 'sport', 'trabajo'], 
        'accesorio': ['accesorios', 'consumibles'], 
    }

base.insert(loc=base.columns.get_loc('ARTÍCULO CONCEPTO')+1, 
        column='concepto', value=base['ARTÍCULO CONCEPTO'].apply(like, args=(con, )))
base.insert(loc=base.columns.get_loc('ARTÍCULO CONCEPTO'), 
        column='categoria', value=base['concepto'].apply(like, args=(cat, )))
base.drop(columns=['ARTÍCULO CONCEPTO'], inplace=True)

## base por categoria
base_cat = base.groupby(by='categoria')

## zapato 
zbase = base_cat.get_group('zapato').copy()
zbase.drop(columns=['categoria'], inplace=True)
## accesorio 
abase = base_cat.get_group('accesorio').copy()
abase.drop(columns=['categoria'], inplace=True)

## zapato
# ARTÍCULO COLOR
color = {
        'negro': ['negro'], 
        'café/chocolate': ['cafe', 'café', 'chocolate'], 
        'café/cognac': ['cognac', 'cafe claro', 'café claro'], 
        'café/tan': ['tan'], 
        'arena': ['arena', 'miel', 'almendra'], 
        'azul marino': ['azul', 'azul marino'], 
        'gris': ['gris'],
        'vino/burgundy': ['vino', 'burgundy'], 
        'blanco': ['blanco'], 
        np.nan: ['sin color']
        }
tono = {
        'oscuro': ['negro', 'chocolate', 'vino', 'azul marino'], 
        'mediano': ['café', 'cafe', 'azul', 'cognac'], 
        'claro': ['café claro', 'cafe claro', 'tan', 'arena', 'miel', 'almendra', 'veige', 'gris', 'blanco'], 
        np.nan: ['sin color']
        }

# ARTÍCULO ACABADO
material = {
        'piel': ['piel', 'gamuza', 'cerdo', 'ternera', 'ternero', 'becerro', 'venado', 'ante buck', 'ante nobuck', 'charol'], 
        'tela': ['algodon', 'nylon', 'sintetico', 'lona']
        }

# zapato color / tono
zbase.insert(loc=zbase.columns.get_loc('ARTÍCULO COLOR')+1, column='color', value=zbase['ARTÍCULO COLOR'].apply(like, args=(color, )))
zbase.insert(loc=zbase.columns.get_loc('color')+2, column='tono', value=zbase['ARTÍCULO COLOR'].apply(like, args=(tono, )))
zbase.drop(columns=['ARTÍCULO COLOR'], inplace=True)
zbase['ARTÍCULO ACABADO'].replace('100% NYLON', 'VENADO', inplace=True)
#zbase.insert(loc=zbase.columns.get_loc('ARTÍCULO ACABADO')+1, column='acabado', value=zbase['ARTÍCULO ACABADO'].apply(like, args=(material,)))

# zapato artículo estilo -> nacional / internacional
def orig(x):
    if str(x).startswith('F'):
        return 'nacional'
    elif len(str(x).split('-')[0]) == 5:
        return 'internacional'


zbase.insert(loc=zbase.columns.get_loc('ARTÍCULO ESTILO')+1, 
        column='origen', value=zbase['ARTÍCULO ESTILO'].map(orig, na_action='ignore'))

## Base final
base.to_csv('../datos/bases/transformadas/fs_master.csv', index=False)


zbase['fecha'] = pd.to_datetime(zbase['fecha'])
#### Fechas faltantes por base
fechas_unicas = pd.Index(data=zbase.loc[:, 'fecha'].dt.date[zbase['fecha'].duplicated(keep='first').apply(lambda x: not x)])
# Tiempo en operación
t_op = pd.Index(data=pd.date_range(start=min(zbase['fecha']), end=max(zbase['fecha']), freq='D').date)

# Faltantes
faltantes = t_op.difference(fechas_unicas)
faltantes = pd.DataFrame({'fecha': faltantes.to_series()}).reset_index(drop=True)

zbase = zbase.append(faltantes, ignore_index=True).sort_values(by='fecha').reset_index(drop=True)

zbase.loc[:, 'fecha'] = pd.to_datetime(zbase['fecha'])
zbase['año'] = zbase['fecha'].dt.year
zbase['mes'] = zbase['fecha'].dt.month
zbase['ndia'] = zbase['fecha'].dt.day
zbase['dia'] = zbase['fecha'].dt.day_name()
zbase['sndia'] = zbase['fecha'].dt.weekday


## Bases por categoria
zbase.to_csv('../datos/bases/transformadas/fs_zapato.csv', index=False)
abase.to_csv('../datos/bases/transformadas/fs_accesorio.csv', index=False)


## Bases por venta
#print(np.mean(base.groupby(by='NOTA DE VENTA NOTA')['ARTÍCULO CONCEPTO'].describe()))
#print(base[base['NOTA DE VENTA NOTA']==2950])
#print(base[base['NOTA DE VENTA NOTA']==2950].columns)
#base.groupby(by='NOTA DE VENTA NOTA').apply(sumI#

# Zapatos multicolor
## la mayoria son de un solo color coñac, cafe, negro, etc

# Talla uni == unitalla ? único;
## unitalla, productos, celcetines, carteras, etc

# personas registradas en clientes
## Se deberían estar registrando clientes

# código de columna ARTÍCULO ESTILO
## Filtrar por proveedor

#001 negro 002 conag 5-3 importado
#001 negro 002 conag empieza con F letras y num nacionales

