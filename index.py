import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import importlib

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

# Snapshot
# Snapshot
@app.callback([Output('ts_nforecast-label', 'children')], 
      [Input('ts_nforecast', 'value')])
def update_ts_label(n):
   return [n]


@app.callback([Output('ts_table', 'children'), Output('ts_plot', 'figure')], 
      [Input('ts', 'value'), Input('ts_period', 'value'), Input('ts_nforecast', 'value')])
def update_timeseries(ts, period, n):
   ## Ventas
   ventas_tab_D, ventas_fig_D = st.ts_plot_table(n=n, verb='Ventas', *st.ventas_args_D)
   ventas_tab_W, ventas_fig_W = st.ts_plot_table(n=n, verb='Ventas', *st.ventas_args_W)
   ventas_tab_M, ventas_fig_M = st.ts_plot_table(n=n, verb='Ventas', *st.ventas_args_M)

   ## Devoluciones
   devs_tab_D, devs_fig_D = st.ts_plot_table(n=n, verb='Devoluciones', *st.devs_args_D)
   devs_tab_W, devs_fig_W = st.ts_plot_table(n=n, verb='Devoluciones', *st.devs_args_W)
   devs_tab_M, devs_fig_M = st.ts_plot_table(n=n, verb='Devoluciones', *st.devs_args_M)

   ## Negados
   negs_tab_D, negs_fig_D = st.ts_plot_table(n=n, verb='Negados', *st.negs_args_D)
   negs_tab_W, negs_fig_W = st.ts_plot_table(n=n, verb='Negados', *st.negs_args_W)
   negs_tab_M, negs_fig_M = st.ts_plot_table(n=n, verb='Negados', *st.negs_args_M)

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


app.config.suppress_callback_exceptions = True

app.layout = html.Div([
   dcc.Location(id='url', refresh=False),
   html.Div(nav), 
   html.Div(id='page')
   ], style={'height': '100vh'})

if __name__ == '__main__':
   app.run_server(host='192.168.1.100', port='8085', debug=False)

