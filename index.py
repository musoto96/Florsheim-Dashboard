import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import importlib


# Servidor
host, port = importlib.import_module(name='config').config

navbar = importlib.import_module(name='navbar')
snapshot = importlib.import_module(name='snapshot')
st = importlib.import_module(name='snapshot_tools')

app = dash.Dash(__name__, title='Florsheim', meta_tags=[{'name': 'viewport', 'content': 'height=device-height'}])
nav = navbar.Navbar()

# Desplegador de paginas
@app.callback(Output('page', 'children'), 
      [Input('url', 'pathname')])
def page(pathname):
   return snapshot.layout()


# Snapshot; General

# Etiqueta de número de periodos a pronosticar en pestaña general
@app.callback([Output('ts_nforecast-label', 'children')], 
      [Input('ts_nforecast', 'value')])
def update_ts_label(n):
   return [n]

# Serie de tiempo y ARIMA
@app.callback([Output('ts_table', 'children'), Output('ts_plot', 'figure')], 
      [Input('ts', 'value'), Input('ts_period', 'value'), Input('ts_nforecast', 'value')])
def update_timeseries(ts, period, n):
   ## Ventas
   ventas_tab_D, ventas_fig_D = st.time_series_plot_autoarima(n=n, verb='Ventas', *st.ventas_args_D)
   ventas_tab_W, ventas_fig_W = st.time_series_plot_autoarima(n=n, verb='Ventas', *st.ventas_args_W)
   ventas_tab_M, ventas_fig_M = st.time_series_plot_autoarima(n=n, verb='Ventas', *st.ventas_args_M)

   ## Devoluciones
   devs_tab_D, devs_fig_D = st.time_series_plot_autoarima(n=n, verb='Devoluciones', suf='', *st.devs_args_D)
   devs_tab_W, devs_fig_W = st.time_series_plot_autoarima(n=n, verb='Devoluciones', suf='', *st.devs_args_W)
   devs_tab_M, devs_fig_M = st.time_series_plot_autoarima(n=n, verb='Devoluciones', suf='', *st.devs_args_M)

   ## Negados
   negs_tab_D, negs_fig_D = st.time_series_plot_autoarima(n=n, verb='Negados', suf='', *st.negs_args_D)
   negs_tab_W, negs_fig_W = st.time_series_plot_autoarima(n=n, verb='Negados', suf='', *st.negs_args_W)
   negs_tab_M, negs_fig_M = st.time_series_plot_autoarima(n=n, verb='Negados', suf='', *st.negs_args_M)

   if ts == 'ventas':
      if period == 'D':
         return [ventas_tab_D, ventas_fig_D]
      elif period == 'W':
         return [ventas_tab_W, ventas_fig_W]
      else:
         return [ventas_tab_M, ventas_fig_M]
   elif ts == 'devoluciones':
      if period == 'D':
         return [devs_tab_D, devs_fig_D]
      elif period == 'W':
         return [devs_tab_W, devs_fig_W]
      else:
         return [devs_tab_M, devs_fig_M]
   else:
      if period == 'D':
         return [negs_tab_D, negs_fig_D]
      elif period == 'W':
         return [negs_tab_W, negs_fig_W]
      else:
         return [negs_tab_M, negs_fig_M]



# Snapshot; Detallado
@app.callback([Output('revenue_plot', 'figure'), 
   Output('revenue_search', 'children')], 
      [Input('revenue_dropdown', 'value')])
def update_revenue_bubble_plot(col):
   if col == 'ESTILO':
      group = 'ARTÍCULO ESTILO'
   elif col == 'TIENDA':
      group = 'NOTA DE VENTA TIENDA'
   elif col == 'ACABADO':
      group = 'ARTÍCULO ACABADO'
   else:
      group = col

   options = st.base.loc[:, group].dropna().unique()
   search_bar = snapshot.revenue_search_bar(options)

   fig = st.revenue_bubble_plot(col)
   return [fig, search_bar]


# Serie de tiempo de selección
@app.callback([Output('ts_plot_selection', 'figure')], 
      [Input('revenue_dropdown', 'value'), 
         Input('revenue_plot', 'hoverData'), 
         Input('revenue_dd_search', 'value')])
def selection_time_series(col, hover_data, search):
   if col == 'ESTILO':
      group = 'ARTÍCULO ESTILO'
   elif col == 'TIENDA':
      group = 'NOTA DE VENTA TIENDA'
   elif col == 'ACABADO':
      group = 'ARTÍCULO ACABADO'
   else:
      group = col

   value = hover_data['points'][0]['text']

   if search != '':
      s = st.time_series(group=group, value=search, date_col='NOTA DE VENTA FECHA', 
            n_col='ARTÍCULO SUBTOTAL', f0=2020, period='Y', ts_period='W')

      df = s.reset_index()
      df.rename(columns={'index': 'fecha', df.columns[1]: 'y'}, inplace=True)

      fig = st.time_series_plot(df, verb='Ventas', watermark=True, watermark_text1=group, watermark_text2=search)
   else:
      s = st.time_series(group=group, value=value, date_col='NOTA DE VENTA FECHA', 
            n_col='ARTÍCULO SUBTOTAL', f0=2020, period='Y', ts_period='W')

      df = s.reset_index()
      df.rename(columns={'index': 'fecha', df.columns[1]: 'y'}, inplace=True)

      fig = st.time_series_plot(df, verb='Ventas', watermark=True, watermark_text1=group, watermark_text2=value)

   return [fig]


@app.callback([Output('revenue_dd_search', 'value')], 
      [Input('revenue_plot', 'hoverData')])
def clear_search(value):
   return ['']


app.config.suppress_callback_exceptions = True

app.layout = html.Div([
   dcc.Location(id='url', refresh=False),
   html.Div(nav), 
   html.Div(id='page')
   ], style={'height': '100vh'})

if __name__ == '__main__':
   app.run_server(host=host, port=port, debug=False)

