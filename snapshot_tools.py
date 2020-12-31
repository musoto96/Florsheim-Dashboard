import numpy as np
import pandas as pd
import scipy
import datetime
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from pmdarima.arima import auto_arima


# Sección 1; General


# KPI's  comparativo i.e. 2000+n+1 vs 2000+n

# Hoja de trabajo: Utilidades por artículo
ut1 = pd.read_csv('datos/bases/adm_finanzas/utilidades_por_art_2020.TXT', sep='\t', encoding='latin_1')
ut0 = pd.read_csv('datos/bases/adm_finanzas/utilidades_por_art_2019.TXT', sep='\t', encoding='latin_1')

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
   sheet = sheet.groupby(by=['ESTILO', 'MARCA', 'COLOR', 'ACABADO', 'CONCEPTO'], as_index=False)[col].sum()

   sheet = sheet.sort_values(by=col)
   sheet.reset_index(inplace=True, drop=True)

   top3 = sheet.tail(3).reset_index(drop=True)

   kpi_top3 = []
   for row in top3.iterrows():
      kpi_top3.append((row[1][['ESTILO', 'MARCA', 'COLOR', 'ACABADO', 'CONCEPTO']] , f'{row[1][col]:.2f}'))

   return kpi_top3


# Hoja devoluciones
cardex = pd.read_csv('datos/bases/inventario/cardex_gral_19-20.TXT', sep='\t', encoding='latin_1')
cardex.loc[:, 'FECHA'] = pd.to_datetime(cardex['FECHA'])
cardex.set_index('FECHA', inplace=True, drop=True)

devoluciones = cardex.copy().groupby(by='MOVIMIENTO').get_group('Entrada (Devolucion)')

# Hoja Negados
negados = pd.read_csv('datos/bases/compras/neg_19-20.TXT', sep='\t', encoding='latin_1')
negados.loc[:, 'FECHA'] = pd.to_datetime(negados['FECHA'])
negados.set_index('FECHA', inplace=True, drop=True)


def kpi_by_period(df, col, t, period):
   df = df.groupby(by=df.index.to_period(period)).get_group(pd.Period(t))
   df.reset_index(drop=True, inplace=True)
   df_total = f'{df[col].sum():,.0f}'
   return df_total


def top3_kpi_by_period_manual_calc(df, col, t, period):
   df = df.groupby(by=df.index.to_period(period)).get_group(pd.Period(t))
   df = df.groupby(by=['ESTILO', 'MARCA', 'COLOR', 'ACABADO', 'CONCEPTO']).sum()
   df = df.reset_index(drop=False)

   total = df[col].sum()

   df = df.groupby(by=['ESTILO', 'MARCA', 'COLOR', 'ACABADO', 'CONCEPTO'], as_index=False)[col].sum()
   df = df.sort_values(by=col)
   df.reset_index(inplace=True, drop=True)

   t3 = df.tail(3).reset_index(drop=True)

   top3 = []
   for row in t3.iterrows():
      top3.append((row[1][['ESTILO', 'MARCA', 'COLOR', 'ACABADO', 'CONCEPTO']] , f'{(row[1][col]*100 / total):.2f}'))

   return top3



# KPI's globales i.e. 2000+n+1 y 2000+n acumulado

# Hoja de trabajo: Ventas, devoluciones, negados, etc., por artículo
vtas = pd.read_csv('datos/bases/adm_finanzas/ventas_acumuladas_por_articulo.TXT', sep='\t', encoding='latin_1')

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
   df = df.groupby(by=['ESTILO', 'MARCA', 'COLOR', 'ACABADO', 'CONCEPTO'], as_index=False)['DÍAS EXIST'].sum()

   df = df.sort_values(by='DÍAS EXIST', ascending=False)
   df.reset_index(inplace=True, drop=True)

   t3 = df.tail(3).reset_index(drop=True)

   top3 = []
   for row in t3.iterrows():
      top3.append((row[1][['ESTILO', 'MARCA', 'COLOR', 'ACABADO', 'CONCEPTO']] , f'{row[1]["DÍAS EXIST"]:.0f}'))

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
   df = df.groupby(by=['ESTILO', 'MARCA', 'COLOR', 'ACABADO', 'CONCEPTO'], as_index=False)['DESPLAZAMIENTO %'].sum()

   df = df.sort_values(by='DESPLAZAMIENTO %', ascending=True)
   df.reset_index(inplace=True, drop=True)

   t3 = df.tail(3).reset_index(drop=True)

   top3 = []
   for row in t3.iterrows():
      top3.append((row[1][['ESTILO', 'MARCA', 'COLOR', 'ACABADO', 'CONCEPTO']] , f'{row[1]["DESPLAZAMIENTO %"]:.0f}%'))
   return top3




# Series de tiempo

# Hoja de trabajo: Ventas de articulo por fecha
zbase = pd.read_csv('datos/bases/transformadas/fs_zapato.csv', engine='python', encoding='utf-8')
zbase['fecha'] = pd.to_datetime(zbase['fecha'])
zbase.set_index('fecha', inplace=True, drop=True)
# Tirar supuestas devoluciones; Número de artículos comprados en 0
zbase.drop(zbase[zbase['ARTÍCULO ARTS'] == 0].index, inplace=True)


def time_series(df, date_col, n_col, col=None, group=None, f0=2020, period='Y', ts_period='D'):
   df = df.copy()
   df = df.groupby(by=df.index.to_period(period)).get_group(pd.Period(f0))

   # Quitar hora y minuto y solo dejar fecha
   df.reset_index(drop=False, inplace=True)
   df.loc[:, date_col] = df[date_col].dt.date

   # Agrupar por categoría
   if col != None and group != None:
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
ventas_df_D = time_series(df=zbase, date_col='fecha', n_col='ARTÍCULO SUBTOTAL', f0=2020, period='Y', ts_period='D')
ventas_args_D = ts_autoarima(ventas_df_D, 'D')
# W
ventas_df_W = time_series(df=zbase, date_col='fecha', n_col='ARTÍCULO SUBTOTAL', f0=2020, period='Y', ts_period='W')
ventas_args_W = ts_autoarima(ventas_df_W, 'W')
# M
ventas_df_M = time_series(df=zbase, date_col='fecha', n_col='ARTÍCULO SUBTOTAL', f0=2020, period='Y', ts_period='M')
ventas_args_M = ts_autoarima(ventas_df_M, 'M')

## Devoluciones
# D
devs_df_D = time_series(df=devoluciones, date_col='FECHA', n_col='ARTS.', f0=2020, period='Y', ts_period='D')
devs_args_D = ts_autoarima(devs_df_D, 'D')
# W
devs_df_W = time_series(df=devoluciones ,date_col='FECHA', n_col='ARTS.', f0=2020, period='Y', ts_period='W')
devs_args_W = ts_autoarima(devs_df_W, 'W')
# M
devs_df_M = time_series(df=devoluciones, date_col='FECHA', n_col='ARTS.', f0=2020, period='Y', ts_period='M')
devs_args_M = ts_autoarima(devs_df_M, 'M')

## Negados
# D
negs_df_D = time_series(df=negados, date_col='FECHA', n_col='ARTS', f0=2020, period='Y', ts_period='D')
negs_args_D = ts_autoarima(negs_df_D, 'D')
# W
negs_df_W = time_series(df=negados, date_col='FECHA', n_col='ARTS', f0=2020, period='Y', ts_period='W')
negs_args_W = ts_autoarima(negs_df_W, 'W')
# M
negs_df_M = time_series(df=negados, date_col='FECHA', n_col='ARTS', f0=2020, period='Y', ts_period='M')
negs_args_M = ts_autoarima(negs_df_M, 'M')



# Sección 2; Detallado


def revenue_bubble_plot(col):
   df = ut1.copy()
   df.loc[:, '% UTILIDAD GLOBAL'] = df['% UTILIDAD GLOBAL'].apply(lambda x: float(x.replace('%','')) / 100)

   cats = ['ESTILO', 'TIENDA', 'COLOR', 'ACABADO', 'CONCEPTO']

   if col == 'modelo':
      col = 'ESTILO'
      hover_data = [i for i in cats if i != col]
      utilidad = df.groupby(by=cats, as_index=False)['% UTILIDAD GLOBAL'].sum()
   else:
      hover_data = []
      utilidad = df.groupby(by=col, as_index=False)['% UTILIDAD GLOBAL'].sum()
      
   size = utilidad.loc[:, '% UTILIDAD GLOBAL'].apply(lambda x: x if x > 0 else 0.0)

   fig = px.scatter(utilidad, x='% UTILIDAD GLOBAL', y=np.arange(0, len(utilidad)), 
         size=size, hover_name=col, hover_data=hover_data, 
         labels={'x': '% Utilidad Global', 'y': ''})

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
   fig.update_yaxes(visible=False)
   fig.update_xaxes(tickformat='.1%')

   return fig


