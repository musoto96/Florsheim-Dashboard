import numpy as np
import pandas as pd
import scipy
import datetime
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from pmdarima.arima import auto_arima
import importlib

rf = importlib.import_module('refactor')

# Sección 1; General


# KPI's  comparativo i.e. 2000+n+1 vs 2000+n

# Hoja de trabajo: Utilidades por artículo
ut1 = pd.read_csv('datos/bases/adm_finanzas/utilidades_por_art_2020.TXT', sep='\t', encoding='latin_1')
ut1 = rf.refactor_all(ut1, col_concepto='CONCEPTO', col_color='COLOR', col_estilo='ESTILO')

ut0 = pd.read_csv('datos/bases/adm_finanzas/utilidades_por_art_2019.TXT', sep='\t', encoding='latin_1')
ut0 = rf.refactor_all(ut0, col_concepto='CONCEPTO', col_color='COLOR', col_estilo='ESTILO')

def kpi_by_sheet(col, x, prec=0, pct=False):
   if int(x) == 1:
      sheet = ut1.copy()
   elif int(x) == 0:
      sheet = ut0.copy()

   kpi = sheet.loc[:, col].apply(lambda x: float(x.replace(',', '')))

   if pct == True:
      kpi = f'{kpi.sum():,.0f}%'  # Porcentaje falta de implementar presición
   else:
      kpi = f'{kpi.sum():,.0f}'

   return kpi


def top3_kpi_by_sheet_precalculated(col, x):
   if int(x) == 1:
      sheet = ut1.copy()
   elif int(x) == 0:
      sheet = ut0.copy()

   sheet.loc[:, col] = sheet[col].apply(lambda x: float(x.strip('%')))
   sheet = sheet.groupby(by=['ESTILO', 'MARCA', 'color', 'ACABADO', 'concepto'], as_index=False)[col].sum()

   sheet = sheet.sort_values(by=col)
   sheet.reset_index(inplace=True, drop=True)

   top3 = sheet.tail(3).reset_index(drop=True)

   kpi_top3 = []
   for row in top3.iterrows():
      kpi_top3.append((row[1][['ESTILO', 'MARCA', 'color', 'ACABADO', 'concepto']] , f'{row[1][col]:.2f}'))

   return kpi_top3


# Hoja devoluciones
cardex = pd.read_csv('datos/bases/inventario/cardex_gral_19-20.TXT', sep='\t', encoding='latin_1')
cardex = rf.refactor_all(cardex, col_concepto='CONCEPTO', col_color='COLOR', col_estilo='ESTILO')

cardex.loc[:, 'FECHA'] = pd.to_datetime(cardex['FECHA'])
cardex.set_index('FECHA', inplace=True, drop=True)

devoluciones = cardex.copy().groupby(by='MOVIMIENTO').get_group('Entrada (Devolucion)')

# Hoja Negados
negados = pd.read_csv('datos/bases/compras/neg_19-20.TXT', sep='\t', encoding='latin_1')
negados = rf.refactor_all(negados, col_concepto='CONCEPTO', col_color='COLOR', col_estilo='ESTILO')

negados.loc[:, 'FECHA'] = pd.to_datetime(negados['FECHA'])
negados.set_index('FECHA', inplace=True, drop=True)


def kpi_by_period(df, col, t, period):
   df = df.groupby(by=df.index.to_period(period)).get_group(pd.Period(t))
   df.reset_index(drop=True, inplace=True)
   df_total = f'{df[col].sum():,.0f}'
   return df_total


def top3_kpi_by_period_manual_calc(df, col, t, period):
   df = df.groupby(by=df.index.to_period(period)).get_group(pd.Period(t))
   df = df.groupby(by=['ESTILO', 'MARCA', 'color', 'ACABADO', 'concepto']).sum()
   df = df.reset_index(drop=False)

   total = df[col].sum()

   df = df.groupby(by=['ESTILO', 'MARCA', 'color', 'ACABADO', 'concepto'], as_index=False)[col].sum()
   df = df.sort_values(by=col)
   df.reset_index(inplace=True, drop=True)

   t3 = df.tail(3).reset_index(drop=True)

   top3 = []
   for row in t3.iterrows():
      top3.append((row[1][['ESTILO', 'MARCA', 'color', 'ACABADO', 'concepto']] , f'{(row[1][col]*100 / total):.2f}'))

   return top3



# KPI's globales i.e. 2000+n+1 y 2000+n acumulado

# Hoja de trabajo: Ventas, devoluciones, negados, etc., por artículo
vtas = pd.read_csv('datos/bases/adm_finanzas/ventas_acumuladas_por_articulo.TXT', sep='\t', encoding='latin_1')
vtas = rf.refactor_all(vtas, col_concepto='CONCEPTO', col_color='COLOR', col_estilo='ESTILO')

# Días existencia
def dexistencia_total():
   existencia = vtas.copy()
   dexistencia = vtas.loc[:, 'DÍAS EXIST'].dropna().apply(lambda x: float(x.replace(',', '')))
   dexistencia_total = f'{dexistencia.mean():.0f}'
   return dexistencia_total


def top3_dexistencia_total():
   df = vtas.copy()
   df = df.dropna(subset=['DÍAS EXIST'])
   df.loc[:, 'DÍAS EXIST'] = df['DÍAS EXIST'].apply(lambda x: float(x.replace(',', '')))
   df = df.groupby(by=['ESTILO', 'MARCA', 'color', 'ACABADO', 'concepto'], as_index=False)['DÍAS EXIST'].sum()

   df = df.sort_values(by='DÍAS EXIST', ascending=False)
   df.reset_index(inplace=True, drop=True)

   t3 = df.tail(3).reset_index(drop=True)

   top3 = []
   for row in t3.iterrows():
      top3.append((row[1][['ESTILO', 'MARCA', 'color', 'ACABADO', 'concepto']] , f'{row[1]["DÍAS EXIST"]:.0f}'))

   return top3


# Desplazamiento
def desplazamiento_total():
   desp = vtas.copy()
   desp = desp.loc[:, 'DESPLAZAMIENTO %'].dropna().apply(lambda x: float(x.replace('%', '')))
   desp_total = f'{desp.mean():.2f}%'
   return desp_total


def top3_desplazamiento_total():
   df = vtas.copy()
   df.loc[:, 'DESPLAZAMIENTO %'] = df['DESPLAZAMIENTO %'].dropna().apply(lambda x: float(x.replace('%', '')))
   df.dropna(subset=['DESPLAZAMIENTO %'], inplace=True)
   df = df.groupby(by=['ESTILO', 'MARCA', 'color', 'ACABADO', 'concepto'], as_index=False)['DESPLAZAMIENTO %'].sum()

   df = df.sort_values(by='DESPLAZAMIENTO %', ascending=True)
   df.reset_index(inplace=True, drop=True)

   t3 = df.tail(3).reset_index(drop=True)

   top3 = []
   for row in t3.iterrows():
      top3.append((row[1][['ESTILO', 'MARCA', 'color', 'ACABADO', 'concepto']] , f'{row[1]["DESPLAZAMIENTO %"]:.0f}%'))
   return top3




# Series de tiempo

# Hoja de trabajo: Ventas de articulo por fecha
#zbase = pd.read_csv('datos/bases/transformadas/fs_zapato.csv', engine='python', encoding='utf-8')
base = pd.read_csv('datos/bases/adm_finanzas/ventas_19-20.TXT', sep='\t', engine='python', encoding='latin_1')

# variables numéricas de 0 -> nan
num_vars = ['ARTÍCULO PRECIO', 'ARTÍCULO IMPORTE', 'ARTÍCULO SUBTOTAL', 'FORMA DE PAGO IMPORTE']
for i in num_vars: 
   base.loc[:, i].replace(0, np.nan, inplace=True)

base = rf.refactor_all(base, col_concepto='ARTÍCULO CONCEPTO', col_color='ARTÍCULO COLOR', col_estilo='ARTÍCULO ESTILO')

base.loc[:, 'NOTA DE VENTA FECHA'] = pd.to_datetime(base['NOTA DE VENTA FECHA'])
base.set_index('NOTA DE VENTA FECHA', inplace=True, drop=True)
# Tirar supuestas devoluciones; Número de artículos comprados en 0
base.drop(base[base['ARTÍCULO ARTS'] == 0].index, inplace=True)


def time_series(date_col, n_col, df=base, group=None, value=None, f0=2020, period='Y', ts_period='D'):
   df = df.copy()
   df = df.groupby(by=df.index.to_period(period)).get_group(pd.Period(f0))

   # Quitar hora y minuto y solo dejar fecha
   df.reset_index(drop=False, inplace=True)
   df.loc[:, date_col] = df[date_col].dt.date
   
   # Agrupar por categoría
   if group != None and value != None:
      df = df.groupby(by=group).get_group(value)
      df.reset_index(drop=True, inplace=True)

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


def time_series_plot(df, verb, watermark=False, watermark_text1='', watermark_text2=''):
   fig = go.Figure()

   fig.add_trace(go.Scatter(mode='lines', fill='tozeroy', x=df['fecha'], y=df['y'], 
      line={'color': 'mediumorchid'}, name='', 
      hovertemplate='Fecha: %{x}<br><b>'+f'{verb}:'+'</b> %{y:$,.2f}'))

   fig.update_xaxes(rangeslider_visible=False, 
         fixedrange=False, 
         rangeselector=dict(
            buttons=list([
               dict(count=1, label="1m", step="month", stepmode="backward"),
               dict(count=6, label="6m", step="month", stepmode="backward"),
               dict(count=1, label="1 Año", step="year", stepmode="backward"),
               dict(count=1, label="Total", step="all", stepmode="todate")
               ])
            ), 
         showline=False, linecolor='lightgrey', linewidth=1, mirror=True)
   fig.update_yaxes(showline=False, fixedrange=False, linecolor='lightgrey', linewidth=1, mirror=True)

   fig.update_layout(
         yaxis_range=[0, df['y'].max()*1.5], 
         hovermode='closest', 
         hoverlabel={'font_size': 9}, 
         margin=dict(t=0, b=0, l=0, r=0),
         plot_bgcolor='white',
         paper_bgcolor = 'white',
         title_font_size = 20,
         title_font_color = 'grey', 
         showlegend=False, 
         font_size = 9)

   if watermark == True:
      fig.add_annotation(text='Venta Semanal<br>'+f'{watermark_text1.title()}: {watermark_text2.title()}', xref='paper', yref='paper', x=0.5, y=0.5)
      fig.update_layout(annotations=[{'showarrow': False, 'opacity': 0.2, 'font_size': 40}])

   return fig


def ts_autoarima(df, period='D', n_pred=30, m=1):
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

   model = auto_arima(df, m=m)
   y_hat, conf = model.predict(n_periods=n_pred, index=xp, return_conf_int=True, alpha=0.2)
   pred = pd.DataFrame({'y_hat': y_hat, 'inf': conf[:, 0], 'sup': conf[:, 1]}, index=xp)

   y_fit , conf_fit = model.predict_in_sample(start=1, end=len(df.index), return_conf_int=True, alpha=0.2)
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
def time_series_plot_autoarima(df, pred, ajuste, verb, suf='$', n=7):
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
      hovertemplate='Fecha: %{x}<br><b>'+f'{verb}:'+'</b> '+f'{suf}'+'%{y:,.2f}'))
   # Ajustados
   fig.add_trace(go.Scatter(mode='lines', x=ajuste['fecha'], y=ajuste['y_hat'], 
      line={'color': 'violet'}, name='', 
      hovertemplate='Fecha: %{x}<br><b>Esperado:</b> '+f'{suf}'+'%{y:,.2f}'))
   # Intervalo inferior ajuste
   fig.add_trace(go.Scatter(mode='lines', x=ajuste['fecha'], y=ajuste['inf'], 
      fill=None, line={'width': 0, 'color': 'thistle'}, name='', 
      hovertemplate='Fecha: %{x}<br><b>Límite Inferior:</b> '+f'{suf}'+'%{y:,.2f}'))
   # Intervalo superior ajuste
   fig.add_trace(go.Scatter(mode='lines', x=ajuste['fecha'], y=ajuste['sup'], 
      fill='tonexty', line={'width': 0, 'color': 'thistle'}, name='', 
      hovertemplate='Fecha: %{x}<br><b>Límite Superior:</b> '+f'{suf}'+'%{y:,.2f}'))
   # Prediccion
   fig.add_trace(go.Scatter(mode='markers', x=pred['fecha'], y=pred['y_hat'], 
      line={'color': 'violet'}, name='', 
      hovertemplate='Fecha: %{x}<br><b>Pronóstico:</b> '+f'{suf}'+'%{y:,.2f}'))
   # Intervalo inferior
   fig.add_trace(go.Scatter(mode='lines', x=pred['fecha'], y=pred['inf'], 
      fill=None, line={'width': 0, 'color': 'violet'}, name='', 
      hovertemplate='Fecha: %{x}<br><b>Límite Inferior:</b> '+f'{suf}'+'%{y:,.2f}'))
   # Intervalo superior
   fig.add_trace(go.Scatter(mode='lines', x=pred['fecha'], y=pred['sup'], 
      fill='tonexty', line={'width': 0, 'color': 'violet'}, name='', 
      hovertemplate='Fecha: %{x}<br><b>Límite Superior:</b> '+f'{suf}'+'%{y:,.2f}'))

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
ventas_df_D = time_series(df=base, date_col='NOTA DE VENTA FECHA', n_col='ARTÍCULO SUBTOTAL', f0=2020, period='Y', ts_period='D')
ventas_args_D = ts_autoarima(ventas_df_D, 'D', m=7)
# W
ventas_df_W = time_series(df=base, date_col='NOTA DE VENTA FECHA', n_col='ARTÍCULO SUBTOTAL', f0=2020, period='Y', ts_period='W')
ventas_args_W = ts_autoarima(ventas_df_W, 'W', m=4)
# M
ventas_df_M = time_series(df=base, date_col='NOTA DE VENTA FECHA', n_col='ARTÍCULO SUBTOTAL', f0=2020, period='Y', ts_period='M')
ventas_args_M = ts_autoarima(ventas_df_M, 'M', m=3)

## Devoluciones
# D
devs_df_D = time_series(df=devoluciones, date_col='FECHA', n_col='ARTS.', f0=2020, period='Y', ts_period='D')
devs_args_D = ts_autoarima(devs_df_D, 'D', m=7)
# W
devs_df_W = time_series(df=devoluciones ,date_col='FECHA', n_col='ARTS.', f0=2020, period='Y', ts_period='W')
devs_args_W = ts_autoarima(devs_df_W, 'W', m=4)
# M
devs_df_M = time_series(df=devoluciones, date_col='FECHA', n_col='ARTS.', f0=2020, period='Y', ts_period='M')
devs_args_M = ts_autoarima(devs_df_M, 'M', m=1)

## Negados
# D
negs_df_D = time_series(df=negados, date_col='FECHA', n_col='ARTS', f0=2020, period='Y', ts_period='D')
negs_args_D = ts_autoarima(negs_df_D, 'D', m=7)
# W
negs_df_W = time_series(df=negados, date_col='FECHA', n_col='ARTS', f0=2020, period='Y', ts_period='W')
negs_args_W = ts_autoarima(negs_df_W, 'W', m=4)
# M
negs_df_M = time_series(df=negados, date_col='FECHA', n_col='ARTS', f0=2020, period='Y', ts_period='M')
negs_args_M = ts_autoarima(negs_df_M, 'M', m=1)



# Sección 2; Detallado


def revenue_bubble_plot(col):
   select = col
   df = ut1.copy()
   df.loc[:, '% UTILIDAD GLOBAL'] = df['% UTILIDAD GLOBAL'].apply(lambda x: float(x.replace('%','')) / 100)

   utilidad = df.groupby(by=col, as_index=False)['% UTILIDAD GLOBAL'].sum()
   size = utilidad.loc[:, '% UTILIDAD GLOBAL'].apply(lambda x: x if x > 0 else 0.0)

   fig = px.scatter(utilidad, x='% UTILIDAD GLOBAL', y=np.arange(0, len(utilidad)), 
         size=size, text=col, labels={'x': '% Utilidad Global', 'y': ''})

   fig.update_layout(
         xaxis_range=[0-0.25*utilidad['% UTILIDAD GLOBAL'].max(), 
            utilidad['% UTILIDAD GLOBAL'].max()*1.25], 
         yaxis_range=[0-0.25*len(utilidad), len(utilidad)*1.25], 
         hovermode='closest', 
         hoverlabel={'font_size': 9}, 
         margin=dict(t=0, b=0, l=0, r=0),
         plot_bgcolor='white',
         paper_bgcolor = 'white',
         title_font_size = 20,
         title_font_color = 'grey', 
         showlegend=False, 
         font_size = 9)
   fig.update_yaxes(visible=False,)
   fig.update_xaxes(tickformat='.1%')
   fig.update_traces(textposition='top center', 
         hovertemplate='<extra></extra><b>' + f'{col.title()}' +'</b><br>Selección: %{text}' + '<br>Utilidad Global: %{x}')

   return fig


