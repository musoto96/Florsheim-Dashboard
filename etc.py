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
print(cardex)

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

def time_series_devs(f0=2020, period='Y', ts_period='D'):
   devs = cardex.copy()
   devs = devs.groupby(by=devs.index.to_period(period)).get_group(pd.Period(f0))
   devs = devs.groupby(by='MOVIMIENTO').get_group('Entrada (Devolucion)')

   # Quitar hora y minuto y solo dejar fecha
   devs.reset_index(drop=False, inplace=True)
   devs.loc[:, 'FECHA'] = devs['FECHA'].dt.date

   # Número de devoluciones
   ndevs = pd.crosstab(index=devs['FECHA'], columns='ARTS.',
                    values=devs['ARTS.'], aggfunc=np.sum)
   # Llenar con 0 días vacios
   x = pd.date_range(start=min(ndevs.index), end=max(ndevs.index))
   ndevs = ndevs.reindex(x).fillna(0)

   # Agrupar por preiodo de teimpo
   g = ndevs.groupby(by=ndevs.index.to_period(ts_period))
   ndevs = g.sum()
   ndevs.index = ndevs.index.to_timestamp()
   return ndevs


print(time_series_devs())

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


def time_series_devs(f0=2020, period='Y', ts_period='D'):
   devs = negados.copy()
   devs = devs.groupby(by=devs.index.to_period(period)).get_group(pd.Period(f0))

   # Quitar hora y minuto y solo dejar fecha
   devs.reset_index(drop=False, inplace=True)
   devs.loc[:, 'FECHA'] = devs['FECHA'].dt.date

   # Número de devoluciones
   ndevs = pd.crosstab(index=devs['FECHA'], columns='ARTS',
                    values=devs['ARTS'], aggfunc=np.sum)
   # Llenar con 0 días vacios
   x = pd.date_range(start=min(ndevs.index), end=max(ndevs.index))
   ndevs = ndevs.reindex(x).fillna(0)

   # Agrupar por preiodo de teimpo
   g = ndevs.groupby(by=ndevs.index.to_period(ts_period))
   ndevs = g.sum()
   ndevs.index = ndevs.index.to_timestamp()
   return ndevs


