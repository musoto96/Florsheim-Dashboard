import numpy as np
import pandas as pd
import scipy
import datetime
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from pmdarima.arima import auto_arima


# Hoja de trabajo: Utilidades por artículo
ut1 = pd.read_csv('datos/bases/adm_finanzas/utilidades_por_art_2020.TXT', sep='\t', encoding='latin_1')
ut0 = pd.read_csv('datos/bases/adm_finanzas/utilidades_por_art_2019.TXT', sep='\t', encoding='latin_1')

# Utilidades
def utilidad_bruta_total(h):
   if int(h) == 1:
      ut = ut1.copy()
   elif int(h) == 0:
      ut = ut0.copy()

   utilidad_bruta = ut.loc[:, 'UTILIDAD BRUTA'].apply(lambda x: float(x.replace(',', '')))
   # ajuste presentacion div/2
   utilidad_bruta_total = f'{utilidad_bruta.sum()/2:,.0f}'
   return utilidad_bruta_total


def top3_utilidad_bruta_total(h):
   if int(h) == 1:
      ut = ut1.copy()
   elif int(h) == 0:
      ut = ut0.copy()

   ut.loc[:, '% UTILIDAD GLOBAL'] = ut['% UTILIDAD GLOBAL'].apply(lambda x: float(x.strip('%')))
   ut = ut.sort_values(by='% UTILIDAD GLOBAL')
   ut.reset_index(inplace=True, drop=True)
   ut = ut.loc[:, ['ESTILO', 'MARCA', 'COLOR', 'ACABADO', 'CONCEPTO', '% UTILIDAD GLOBAL']].tail(3).reset_index(drop=True)
   t3 = []
   for row in ut.iterrows():
      t3.append((row[1][['ESTILO', 'MARCA', 'COLOR', 'ACABADO', 'CONCEPTO']] , row[1]['% UTILIDAD GLOBAL']))
   return t3


# Ventas netas
def ventas_netas_total(h):
   if int(h) == 1:
      ut = ut1.copy()
   elif int(h) == 0:
      ut = ut0.copy()

   ventas_netas = ut.loc[:, 'VENTAS NETAS'].apply(lambda x: float(x.replace(',', '')))
   # ajuste presentacion div/2
   ventas_netas_total = f'{ventas_netas.sum()/2:,.0f}'
   return ventas_netas_total


def top3_ventas_netas_total(h):
   if int(h) == 1:
      ut = ut1.copy()
   elif int(h) == 0:
      ut = ut0.copy()

   ut.loc[:, '% VENTAS'] = ut['% VENTAS'].apply(lambda x: float(x.strip('%')))
   ut = ut.sort_values(by='% VENTAS')
   ut.reset_index(inplace=True, drop=True)
   ut = ut.loc[:, ['ESTILO', 'MARCA', 'COLOR', 'ACABADO', 'CONCEPTO', '% VENTAS']].tail(3).reset_index(drop=True)
   t3 = []
   for row in ut.iterrows():
      t3.append((row[1][['ESTILO', 'MARCA', 'COLOR', 'ACABADO', 'CONCEPTO']] , row[1]['% VENTAS']))
   return t3


# Costo
def costo_total(h):
   if int(h) == 1:
      ut = ut1.copy()
   elif int(h) == 0:
      ut = ut0.copy()

   costo = ut.loc[:, 'COSTO'].apply(lambda x: float(x.replace(',', '')))
   # ajuste presentacion div/2
   costo_total = f'{costo.sum()/2:,.0f}'
   return costo_total


# Hoja devoluciones
cardex = pd.read_csv('datos/bases/inventario/cardex_gral_19-20.TXT', sep='\t', encoding='latin_1')
cardex.loc[:, 'FECHA'] = pd.to_datetime(cardex['FECHA'])
cardex.set_index('FECHA', inplace=True, drop=True)

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



# Hoja de trabajo: Ventas, devoluciones, negados, etc., por artículo
vtas = pd.read_csv('datos/bases/adm_finanzas/ventas_acumuladas_por_articulo.TXT', sep='\t', encoding='latin_1')

# Días existencia
def dexistencia_total():
   existencia = vtas.copy()
   dexistencia = vtas.loc[:, 'DÍAS EXIST'].dropna().apply(lambda x: float(x.replace(',', '')))
   dexistencia_total = f'{dexistencia.mean():.0f}'
   return dexistencia_total


def top3_dexistencia_total(categoria='ESTILO'):
   df = vtas.copy()
   df = df.dropna(subset=['DÍAS EXIST'])
   df.loc[:, 'DÍAS EXIST'] = df['DÍAS EXIST'].apply(lambda x: float(x.replace(',', '')))
   df = df.sort_values(by='DÍAS EXIST', ascending=False)
   df.reset_index(inplace=True, drop=True)
   df = df.loc[:, ['ESTILO', 'MARCA', 'COLOR', 'ACABADO', 'CONCEPTO', 'DÍAS EXIST']].dropna().tail(3).reset_index(drop=True)
   t3 = []
   for row in df.iterrows():
      t3.append((row[1][['ESTILO', 'MARCA', 'COLOR', 'ACABADO', 'CONCEPTO']] , f'{row[1]["DÍAS EXIST"]:.0f}'))
   return t3


# Desplazamiento
def desplazamiento_total():
   desp = vtas.copy()
   desp = desp.loc[:, 'DESPLAZAMIENTO %'].dropna().apply(lambda x: float(x.replace('%', '')))
   desp_total = f'{desp.mean():.2f}%'
   return desp_total


def top3_desplazamiento_total(categoria='ESTILO'):
   df = vtas.copy()
   df.loc[:, 'DESPLAZAMIENTO %'] = df['DESPLAZAMIENTO %'].dropna().apply(lambda x: float(x.replace('%', '')))
   df = df.sort_values(by='DESPLAZAMIENTO %', ascending=True)
   df.dropna(subset=['DESPLAZAMIENTO %'], inplace=True)
   df.reset_index(inplace=True, drop=True)
   df = df.loc[:, ['ESTILO', 'MARCA', 'COLOR', 'ACABADO', 'CONCEPTO', 'DESPLAZAMIENTO %']].dropna().tail(3).reset_index(drop=True)
   t3 = []
   for row in df.iterrows():
      t3.append((row[1][['ESTILO', 'MARCA', 'COLOR', 'ACABADO', 'CONCEPTO']] , f'{row[1]["DESPLAZAMIENTO %"]:.0f}%'))
   return t3



# Hoja de trabajo: Ventas de articulo por fecha
zbase = pd.read_csv('datos/bases/transformadas/fs_zapato.csv', engine='python', encoding='utf-8')
zbase['fecha'] = pd.to_datetime(zbase['fecha'])
# Tirar supuestas devoluciones; Número de artículos comprados en 0
zbase.drop(zbase[zbase['ARTÍCULO ARTS'] == 0].index, inplace=True)


def time_series_ventas(f0=2020, period='D'):
   df = zbase.copy()

   # Quitar hora y minuto y solo dejar fecha
   df.loc[:, 'fecha'] = df['fecha'].dt.date

   df = df.groupby('año').get_group(f0)
   # Monto de ventas
   mventas = pd.crosstab(index=df['fecha'], columns='ARTÍCULO SUBTOTAL',
                    values=df['ARTÍCULO SUBTOTAL'], aggfunc=np.sum)
   # Llenar con 0 días vacios
   x = pd.date_range(start=min(mventas.index), end=max(mventas.index))
   mventas = mventas.reindex(x).fillna(0)

   # Agrupar por preiodo de teimpo
   g = mventas.groupby(by=mventas.index.to_period(period))
   mventas = g.sum()
   mventas.index = mventas.index.to_timestamp()

   return mventas


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


def time_series_negs(f0=2020, period='Y', ts_period='D'):
   negs = negados.copy()
   negs = negs.groupby(by=negs.index.to_period(period)).get_group(pd.Period(f0))

   # Quitar hora y minuto y solo dejar fecha
   negs.reset_index(drop=False, inplace=True)
   negs.loc[:, 'FECHA'] = negs['FECHA'].dt.date

   # Número de negados
   nnegs = pd.crosstab(index=negs['FECHA'], columns='ARTS',
                    values=negs['ARTS'], aggfunc=np.sum)
   # Llenar con 0 días vacios
   x = pd.date_range(start=min(nnegs.index), end=max(nnegs.index))
   nnegs = nnegs.reindex(x).fillna(0)

   # Agrupar por preiodo de teimpo
   g = nnegs.groupby(by=nnegs.index.to_period(ts_period))
   nnegs = g.sum()
   nnegs.index = nnegs.index.to_timestamp()
   return nnegs


def ts_autoarima(df, period='D', n_pred=30):
   # Multiplos de tiempo
   if period == 'W':
      weeks, days = n_pred, 0
   elif period == 'M':
      weeks, days =  0, n_pred*30
   else:
      weeks, days = 0, n_pred

   max_x = max(df.index)+datetime.timedelta(weeks=weeks, days=days)
   min_x = max(df.index)

   xp = pd.period_range(start=min_x, end=max_x, freq=period)
   xp = xp[:n_pred].to_timestamp()

   model = auto_arima(df)
   y_hat, conf = model.predict(n_periods=n_pred, index=xp, return_conf_int=True)
   pred = pd.DataFrame({'y_hat': y_hat, 'inf': conf[:, 0], 'sup': conf[:, 1]}, index=xp)

   y_fit , conf_fit = model.predict_in_sample(start=1, end=len(df.index), return_conf_int=True)
   ajuste = pd.DataFrame({'y_hat': y_fit, 'inf': conf_fit[:, 0], 'sup': conf_fit[:, 1]}, index=df.index)

   # Nuevo indice para agregar primer dato
   pred = pred.append(ajuste.iloc[-1, :])
   pred.sort_index(inplace=True)

   # Resetear indices para grafica
   pred.reset_index(inplace=True, drop=False)
   pred.rename(columns={'index': 'fecha'}, inplace=True)
   ajuste.reset_index(inplace=True, drop=False)
   ajuste.rename(columns={'index': 'fecha'}, inplace=True)
   df.reset_index(inplace=True)
   df.rename(columns={'index': 'fecha', df.columns[1]: 'y'}, inplace=True)

   return df, pred, ajuste


# Serie de tiempo y pronostico
def ts_plot_table(df, pred, ajuste, verb, n=7):
   pred = pred[:n]

   # Tabla
   pred_tab = pred[['fecha', 'y_hat']].iloc[1:, :]
   pred_tab.loc[:, 'y_hat'] = pred_tab['y_hat'].round(2)
   pred_tab.loc[:, 'fecha'] = pd.to_datetime(pred_tab['fecha']).dt.date
   pred_tab.rename(columns={'fecha': 'Fecha', 'y_hat': 'Pronóstico'}, inplace=True)
   tab = dbc.Table.from_dataframe(pred_tab, striped=True, bordered=True, hover=True)

   # Gráfico
   fig = go.Figure()
   # Reales
   fig.add_trace(go.Scatter(mode='markers', x=df['fecha'], y=df['y'], 
      line={'color': 'royalblue'}, name='', 
      hovertemplate='Fecha: %{x}<br><b>'+f'{verb}:'+'</b> %{y:$,.2f}'))
   # Ajustados
   fig.add_trace(go.Scatter(mode='lines', x=ajuste['fecha'], y=ajuste['y_hat'], 
      line={'color': 'violet'}, name='', 
      hovertemplate='Fecha: %{x}<br><b>Esperado:</b> %{y:$,.2f}'))
   # Intervalo inferior ajuste
   fig.add_trace(go.Scatter(mode='lines', x=ajuste['fecha'], y=ajuste['inf'], 
      fill=None, line={'width': 0, 'color': 'thistle'}, name='', 
      hovertemplate='Fecha: %{x}<br><b>Límite Inferior:</b> %{y:$,.2f}'))
   # Intervalo superior ajuste
   fig.add_trace(go.Scatter(mode='lines', x=ajuste['fecha'], y=ajuste['sup'], 
      fill='tonexty', line={'width': 0, 'color': 'thistle'}, name='', 
      hovertemplate='Fecha: %{x}<br><b>Límite Superior:</b> %{y:$,.2f}'))
   # Prediccion
   fig.add_trace(go.Scatter(mode='markers', x=pred['fecha'], y=pred['y_hat'], 
      line={'color': 'violet'}, name='', 
      hovertemplate='Fecha: %{x}<br><b>Pronóstico:</b> %{y:$,.2f}'))
   # Intervalo inferior
   fig.add_trace(go.Scatter(mode='lines', x=pred['fecha'], y=pred['inf'], 
      fill=None, line={'width': 0, 'color': 'violet'}, name='', 
      hovertemplate='Fecha: %{x}<br><b>Límite Inferior:</b> %{y:$,.2f}'))
   # Intervalo superior
   fig.add_trace(go.Scatter(mode='lines', x=pred['fecha'], y=pred['sup'], 
      fill='tonexty', line={'width': 0, 'color': 'violet'}, name='', 
      hovertemplate='Fecha: %{x}<br><b>Límite Superior:</b> %{y:$,.2f}'))

   fig.update_xaxes(rangeslider_visible=True, 
         range=[df.iloc[-5, df.columns.get_loc('fecha')], max(pred['fecha'])+datetime.timedelta(days=1)], fixedrange=False, 
         rangeselector=dict(
            buttons=list([
               dict(count=1, label="1m", step="month", stepmode="backward"),
               dict(count=6, label="6m", step="month", stepmode="backward"),
               dict(count=1, label="1 Año", step="year", stepmode="backward"),
               dict(count=1, label="Total", step="all", stepmode="todate")
               ])
            ), 
         showline=False, linecolor='lightgrey', linewidth=1, mirror=True)
   fig.update_yaxes(showline=False, linecolor='lightgrey', linewidth=1, mirror=True)

   fig.update_layout(
         hovermode='closest', 
         hoverlabel={'font_size': 9}, 
         margin=dict(t=0, b=0, l=0, r=0),
         plot_bgcolor='white',
         paper_bgcolor = 'white',
         title_font_size = 20,
         title_font_color = 'grey', 
         showlegend=False, 
         font_size = 9)
   return tab, fig


# Para hacer los modelos desde antes y mantenerlos en RAM
## Ventas
# D
ventas_df_D = time_series_ventas(2020, 'D')
ventas_args_D = ts_autoarima(ventas_df_D, 'D')
# W
ventas_df_W = time_series_ventas(2020, 'W')
ventas_args_W = ts_autoarima(ventas_df_W, 'W')
# M
ventas_df_M = time_series_ventas(2020, 'M')
ventas_args_M = ts_autoarima(ventas_df_M, 'M')

## Devoluciones
# D
devs_df_D = time_series_devs(2020, 'Y', 'D')
devs_args_D = ts_autoarima(devs_df_D, 'D')
# W
devs_df_W = time_series_devs(2020, 'Y', 'W')
devs_args_W = ts_autoarima(devs_df_W, 'W')
# M
devs_df_M = time_series_devs(2020, 'Y', 'M')
devs_args_M = ts_autoarima(devs_df_M, 'M')

## Negados
# D
negs_df_D = time_series_negs(2020, 'Y', 'D')
negs_args_D = ts_autoarima(negs_df_D, 'D')
# W
negs_df_W = time_series_negs(2020, 'Y', 'W')
negs_args_W = ts_autoarima(negs_df_W, 'W')
# M
negs_df_M = time_series_negs(2020, 'Y', 'M')
negs_args_M = ts_autoarima(negs_df_M, 'M')

