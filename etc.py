import numpy as np
import pandas as pd
import scipy
import datetime
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from pmdarima.arima import auto_arima

# Hoja devoluciones
cardex = pd.read_csv('datos/bases/inventario/cardex_gral_19-20.TXT', sep='\t', encoding='latin_1')
cardex.loc[:, 'FECHA'] = pd.to_datetime(cardex['FECHA'])
cardex.set_index('FECHA', inplace=True, drop=True)
print(cardex.columns)
print(cardex.head(10))

# Devoluciones
def devoluciones_total(t, period):
   devs = cardex.copy()
   devs = devs.groupby(by=devs.index.to_period(period)).get_group(pd.Period(t))
   devs = devs.groupby(by='MOVIMIENTO').get_group('Entrada (Devolucion)')
   devs.reset_index(drop=True, inplace=True)
   devs_total = f'{devs["ARTS."].sum():,.0f}'
   return devs_total


def top3_devoluciones_total(t, period):
   devs = cardex.copy()
   devs = devs.groupby(by=devs.index.to_period(period)).get_group(pd.Period(t))
   devs = devs.groupby(by='MOVIMIENTO').get_group('Entrada (Devolucion)')[['ESTILO', 'MARCA', 'COLOR', 'ACABADO', 'CONCEPTO', 'ARTS.']]
   devs = devs.groupby(by=['ESTILO', 'MARCA', 'COLOR', 'ACABADO', 'CONCEPTO']).sum()
   devs = devs.reset_index(drop=False)
   devs = devs.sort_values(by='ARTS.')
   devs.reset_index(inplace=True, drop=True)
   total = devs['ARTS.'].sum()
   devs = devs.loc[:, ['ESTILO', 'MARCA', 'COLOR', 'ACABADO', 'CONCEPTO', 'ARTS.']].tail(3).reset_index(drop=True)

   t3 = []
   for row in devs.iterrows():
      t3.append((row[1][['ESTILO', 'MARCA', 'COLOR', 'ACABADO', 'CONCEPTO']] , row[1]['ARTS.']*100 / total))
   return t3


# Hoja Negados
negados = pd.read_csv('datos/bases/compras/neg_19-20.TXT', sep='\t', encoding='latin_1')
negados.loc[:, 'FECHA'] = pd.to_datetime(negados['FECHA'])
negados.set_index('FECHA', inplace=True, drop=True)

# Negados
def negados_total(t, period):
   negs = negados.copy()
   negs = negs.groupby(by=negs.index.to_period(period)).get_group(pd.Period(t))
   negs.reset_index(drop=True, inplace=True)
   negs_total = f'{negs["ARTS"].sum():,.0f}'
   return negs_total


def top3_negados_total(t, period):
   negs = negados.copy()
   negs = negs.groupby(by=negs.index.to_period(period)).get_group(pd.Period(t))
   negs = negs.groupby(by=['ESTILO', 'MARCA', 'COLOR', 'ACABADO', 'CONCEPTO']).sum()
   negs = negs.reset_index(drop=False)
   negs = negs.sort_values(by='ARTS')
   negs.reset_index(inplace=True, drop=True)
   total = negs['ARTS'].sum()
   negs = negs.loc[:, ['ESTILO', 'MARCA', 'COLOR', 'ACABADO', 'CONCEPTO', 'ARTS']].tail(3).reset_index(drop=True)

   t3 = []
   for row in negs.iterrows():
      t3.append((row[1][['ESTILO', 'MARCA', 'COLOR', 'ACABADO', 'CONCEPTO']] , row[1]['ARTS']*100 / total))
   return t3




def time_series(df, date_col, n_col, col=None, group=None, f0=2020, period='Y', ts_period='D'):
   df = df.copy()
   df = df.groupby(by=df.index.to_period(period)).get_group(pd.Period(f0))

   # Quitar hora y minuto y solo dejar fecha
   df.reset_index(drop=False, inplace=True)
   df.loc[:, date_col] = df[date_col].dt.date

   # Agrupar por categoría
   if col != None and group != None:
      print('grouped')
      df = df.groupby(by=col).get_group(group)

   # Número de devoluciones
   ndf = pd.crosstab(index=df[date_col], columns=n_col,
                    values=df[n_col], aggfunc=np.sum)
   # Llenar con 0 días vacios
   x = pd.date_range(start=min(ndf.index), end=max(ndf.index))
   ndf = ndf.reindex(x).fillna(0)

   # Agrupar por preiodo de teimpo
   g = ndf.groupby(by=ndf.index.to_period(ts_period))
   ndf = g.sum()
   ndf.index = ndf.index.to_timestamp()
   return ndf


print(cardex.groupby(by='ACABADO').groups.keys())
print(time_series(df=cardex, date_col='FECHA', n_col='ARTS.', col='ACABADO', group='100% PIEL', f0=2020, period='Y', ts_period='D'))
