import numpy as np
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import datetime
import importlib
import locale
import base64


locale.setlocale(locale.LC_ALL, '')
navbar = importlib.import_module(name='navbar').Navbar()
st = importlib.import_module(name='snapshot_tools')  # snapshot tools

año1 = '2020'
año0 = '2019'


# Sección 1; General


def makekpi(name, _id, x1, x0, y1, y0, pct, top3, status, icon):
   kpi = dbc.Card(
         children=[ 
            dbc.CardHeader(
               dbc.Row([ 
                  dbc.Col(name, style={'fontSize': 12, 'padding': '5px', 'text-align': 'center', 'fontWeight': 'bold'}), 
                  ]), style={'padding': '0px'}
               ), 
            dbc.CardBody(
               children=[
                  dbc.Row(children=[ 
                     dbc.Col(html.Img(src=f'assets/icons/{icon}', height='80%', id=f'{_id}-ind', style={'opacity': 0.5}), style={'padding': '0px', 'text-align': 'right'}), 
                     dbc.Tooltip(
                        children=[
                           html.P(f'Cambio: {pct:.2f}%', style={'margin': '0px', 'fontSize': 9})
                           ], target=f'{_id}-ind', placement='left'
                        ), 
                     dbc.Col(html.H5(y1, className='card-title', style={'margin': '0px', 'text-align': 'left', 'color': status})), 
                     dbc.Col(
                        children=[
                           dbc.Row(
                              html.P(x0, 
                                 style={'fontSize': 9, 'margin': '0px', 'color': 'grey', 'font-weight': 'bold'}
                                 )
                              ), 
                           dbc.Row(
                              html.P(y0, 
                                 style={'fontSize': 11, 'margin': '0px', 'color': 'grey'}
                                 )
                              )
                        ], width=3), 
                     ]), 
                  dbc.Col(children=[
                     dbc.Row(
                        children=[
                           dbc.Col(f'{top3[2][0]["ESTILO"]}', id=f'{_id}-t1', className='card-text', style={'fontSize': 11, 'text-align': 'center'}), 
                           dbc.Tooltip(
                              children=[
                                 html.P(f'Marca: {top3[2][0]["MARCA"].title()}', style={'margin': '0px', 'fontSize': 9}), 
                                 html.P(f'Color: {top3[2][0]["color"].title()}', style={'margin': '0px', 'fontSize': 9}), 
                                 html.P(f'Acabado: {top3[2][0]["ACABADO"].title()}', style={'margin': '0px', 'fontSize': 9}), 
                                 html.P(f'Concepto: {top3[2][0]["concepto"].title()}', style={'margin': '0px', 'fontSize': 9})
                                 ], target=f'{_id}-t1', placement='bottom'
                              ), 
                           dbc.Col(f'{top3[2][1]}%', className='card-text', style={'fontSize': 11, 'text-align': 'left'})
                           ]
                        ), 
                     dbc.Row(
                        children=[
                           dbc.Col(f'{top3[1][0]["ESTILO"]}', id=f'{_id}-t2', className='card-text', style={'fontSize': 11, 'text-align': 'center'}), 
                           dbc.Tooltip(
                              children=[
                                 html.P(f'Marca: {top3[1][0]["MARCA"].title()}', style={'margin': '0px', 'fontSize': 9}), 
                                 html.P(f'Color: {top3[1][0]["color"].title()}', style={'margin': '0px', 'fontSize': 9}), 
                                 html.P(f'Acabado: {top3[1][0]["ACABADO"].title()}', style={'margin': '0px', 'fontSize': 9}), 
                                 html.P(f'Concepto: {top3[1][0]["concepto"].title()}', style={'margin': '0px', 'fontSize': 9})
                                 ], target=f'{_id}-t2', placement='bottom'
                              ), 
                           dbc.Col(f'{top3[1][1]}%', className='card-text', style={'fontSize': 11, 'text-align': 'left'})
                           ]
                        ), 
                     dbc.Row(
                        children=[
                           dbc.Col(f'{top3[0][0]["ESTILO"]}', id=f'{_id}-t3', className='card-text', style={'fontSize': 11, 'text-align': 'center'}), 
                           dbc.Tooltip(
                              children=[
                                 html.P(f'Marca: {top3[0][0]["MARCA"].title()}', style={'margin': '0px', 'fontSize': 9}), 
                                 html.P(f'Color: {top3[0][0]["color"].title()}', style={'margin': '0px', 'fontSize': 9}), 
                                 html.P(f'Acabado: {top3[0][0]["ACABADO"].title()}', style={'margin': '0px', 'fontSize': 9}), 
                                 html.P(f'Concepto: {top3[0][0]["concepto"].title()}', style={'margin': '0px', 'fontSize': 9})
                                 ], target=f'{_id}-t3', placement='bottom'
                              ), 
                           dbc.Col(f'{top3[0][1]}%', className='card-text', style={'fontSize': 11, 'text-align': 'left'})
                           ]
                        ), 
                     ], width=8, style={'display': 'inline-block', 'padding': '0px', 'margin': '0px'}), 
                  dbc.Col(
                        html.H3(f'{pct:.1f}%', style={'margin': '0px', 'padding': '0px', 'color': status}), width=4, 
                        style={'display': 'inline-block', 'padding': '0px', 'margin': '0px'}
                        ), 
                  ], style={'padding': '5px'}
               )
            ], style={'marginRight': '5px'}
         )
   return kpi


# Ventas netas
t3vn = st.top3_kpi_by_sheet_precalculated(col='% VENTAS', x=1)

ventas_netas_1 = st.kpi_by_sheet(col='VENTAS NETAS', x=1)
ventas_netas_0 = st.kpi_by_sheet(col='VENTAS NETAS', x=0)
ventas_netas_pct = (float(ventas_netas_1.replace(",", '')) - float(ventas_netas_0.replace(",", "")))*100 / float(ventas_netas_0.replace(",", ""))
ventas_netas_status = 'lightseagreen' if ventas_netas_pct > 0 else 'grey' if ventas_netas_pct == 0 else 'lightcoral'
ventas_netas_icon = 'increase-24.png' if ventas_netas_pct >= 0 else 'decrease-24.png'

card_ventas_netas = makekpi('Ventas Netas', 't1', año1, año0, ventas_netas_1, ventas_netas_0, ventas_netas_pct, t3vn, ventas_netas_status, ventas_netas_icon)


# Utilidades 
t3u = st.top3_kpi_by_sheet_precalculated(col='% UTILIDAD GLOBAL', x=1)

utilidad_1 = st.kpi_by_sheet(col='UTILIDAD BRUTA', x=1)
utilidad_0 = st.kpi_by_sheet(col='UTILIDAD BRUTA', x=0)
utilidad_pct = (float(utilidad_1.replace(",", '')) - float(utilidad_0.replace(",", "")))*100 / float(utilidad_0.replace(",", ""))
utilidad_status = 'lightseagreen' if utilidad_pct > 0 else 'grey' if utilidad_pct == 0 else 'lightcoral'
utilidad_icon = 'increase-24.png' if utilidad_pct >= 0 else 'decrease-24.png'

card_utilidad = makekpi('Utilidades', 't2', año1, año0, utilidad_1, utilidad_0, utilidad_pct, t3u, utilidad_status, utilidad_icon)


# Devoluciones
t3dev = st.top3_kpi_by_period_manual_calc(st.devoluciones, 'ARTS.', año1, 'Y')

devoluciones_1 = st.kpi_by_period(st.devoluciones, 'ARTS.', año1, 'Y')
devoluciones_0 = st.kpi_by_period(st.devoluciones, 'ARTS.', año0, 'Y')
devoluciones_pct = (float(devoluciones_1.replace(",", '')) - float(devoluciones_0.replace(",", "")))*100 / float(devoluciones_0.replace(",", ""))
devoluciones_status = 'lightseagreen' if devoluciones_pct < 0 else 'grey' if devoluciones_pct == 0 else 'lightcoral'
devoluciones_icon = 'increase-24.png' if devoluciones_pct >= 0 else 'decrease-24.png'

card_devoluciones = makekpi('Devoluciones', 't3',  año1, año0, devoluciones_1, devoluciones_0, devoluciones_pct, t3dev, devoluciones_status, devoluciones_icon)


# Negados
t3neg = st.top3_kpi_by_period_manual_calc(st.negados, 'ARTS', año1, 'Y')

negados_1 = st.kpi_by_period(st.negados, 'ARTS', año1, 'Y')
negados_0 = st.kpi_by_period(st.negados, 'ARTS', año0, 'Y')
negados_pct = (float(negados_1.replace(",", '')) - float(negados_0.replace(",", "")))*100 / float(negados_0.replace(",", ""))
negados_status = 'lightseagreen' if negados_pct < 0 else 'grey' if negados_pct == 0 else 'lightcoral'
negados_icon = 'increase-24.png' if negados_pct >= 0 else 'decrease-24.png'

card_negados = makekpi('Negados', 't4', año1, año0, negados_1, negados_0, negados_pct, t3neg, negados_status, negados_icon)


# KPIs secundarios

def makekpi_sec(name, _id, n, top3):
   kpi = dbc.Card(
         children=[ 
            dbc.CardHeader(
               dbc.Row([ 
                  dbc.Col(name, style={'fontSize': 10, 'padding': '2px', 'text-align': 'center', 'fontWeight': 'bold'}), 
                  ]), style={'padding': '0px'}
               ), 
            dbc.CardBody(
               children=[
                  dbc.Row(children=[ 
                     dbc.Col(
                        children=[
                           dbc.Row(
                              html.P('Promedio', 
                                 style={'fontSize': 9, 'margin': '0px', 'color': 'grey', 'font-weight': 'bold'}
                                 )
                              ), 
                           dbc.Row(
                              html.P(n, 
                                 style={'fontSize': 15, 'margin': '0px', 'color': 'grey', 'text-align': 'center', 'font-weight': 'bold'}
                                 )
                              )
                           ], xs=12, sm=4, md=4, lg=12, xl=4, style={'padding': '0px', 'paddingLeft': '30px'}), 
                     dbc.Col(children=[
                        dbc.Row(
                           children=[
                              dbc.Col(f'{top3[2][0]["ESTILO"]}', id=f'{_id}-t1', className='card-text', style={'fontSize': 11, 'text-align': 'center'}), 
                              dbc.Tooltip(
                                 children=[
                                    html.P(f'Marca: {top3[2][0]["MARCA"].title()}', style={'margin': '0px', 'fontSize': 9}), 
                                    html.P(f'Color: {top3[2][0]["color"].title()}', style={'margin': '0px', 'fontSize': 9}), 
                                    html.P(f'Acabado: {top3[2][0]["ACABADO"].title()}', style={'margin': '0px', 'fontSize': 9}), 
                                    html.P(f'Concepto: {top3[2][0]["concepto"].title()}', style={'margin': '0px', 'fontSize': 9})
                                    ], target=f'{_id}-t1', placement='bottom'
                                 ), 
                              dbc.Col(f'{top3[2][1]}', className='card-text', style={'fontSize': 11, 'text-align': 'left'})
                              ]
                           ), 
                        dbc.Row(
                           children=[
                              dbc.Col(f'{top3[1][0]["ESTILO"]}', id=f'{_id}-t2', className='card-text', style={'fontSize': 11, 'text-align': 'center'}), 
                              dbc.Tooltip(
                                 children=[
                                    html.P(f'Marca: {top3[1][0]["MARCA"].title()}', style={'margin': '0px', 'fontSize': 9}), 
                                    html.P(f'Color: {top3[1][0]["color"].title()}', style={'margin': '0px', 'fontSize': 9}), 
                                    html.P(f'Acabado: {top3[1][0]["ACABADO"].title()}', style={'margin': '0px', 'fontSize': 9}), 
                                    html.P(f'Concepto: {top3[1][0]["concepto"].title()}', style={'margin': '0px', 'fontSize': 9})
                                    ], target=f'{_id}-t2', placement='bottom'
                                 ), 
                              dbc.Col(f'{top3[1][1]}', className='card-text', style={'fontSize': 11, 'text-align': 'left'})
                              ]
                           ), 
                        dbc.Row(
                           children=[
                              dbc.Col(f'{top3[0][0]["ESTILO"]}', id=f'{_id}-t3', className='card-text', style={'fontSize': 11, 'text-align': 'center'}), 
                              dbc.Tooltip(
                                 children=[
                                    html.P(f'Marca: {top3[0][0]["MARCA"].title()}', style={'margin': '0px', 'fontSize': 9}), 
                                    html.P(f'Color: {top3[0][0]["color"].title()}', style={'margin': '0px', 'fontSize': 9}), 
                                    html.P(f'Acabado: {top3[0][0]["ACABADO"].title()}', style={'margin': '0px', 'fontSize': 9}), 
                                    html.P(f'Concepto: {top3[0][0]["concepto"].title()}', style={'margin': '0px', 'fontSize': 9})
                                    ], target=f'{_id}-t3', placement='bottom'
                                 ), 
                              dbc.Col(f'{top3[0][1]}', className='card-text', style={'fontSize': 11, 'text-align': 'left'})
                              ]
                           ), 
                        ], style={'padding': '0px'})
                     ])
                  ], style={'padding': '5px'}
               )
            ], style={
                  'height': '100%', 
                  'marginRight': '5px', 
                  'marginTop': '5px'
                  }
         )
   return kpi


# Días de existencia
t3dex = st.top3_dexistencia_total()
dexistencia_1 = st.dexistencia_total()

card_dexistencia = makekpi_sec('Menores Días de Existencia', 'dext', dexistencia_1, t3dex)

# Desplazamiento
t3des = st.top3_desplazamiento_total()
desplazamiento_1 = st.desplazamiento_total()

card_desplazamiento = makekpi_sec('Mayor % Desplazamiento', 'desp', desplazamiento_1, t3des)



# Serie de tiempo
# ventas
card_ts = dbc.Card(
      dcc.Graph(id='ts_plot', config={'displayModeBar': False, 'responsive': True}),
      style={
         'height': '100%', 
         'marginRight': '5px', 
         'marginTop': '5px', 
         'paddingTop': '0px', 
         'paddingLeft': '0px', 
         'paddingRight': '0px'}
      )

card_ts_controles = dbc.Card(
      children=[ 
         dbc.CardBody(children=[
            html.H6('Serie de Tiempo', style={'fontSize': 11, 'padding': '2px', 'paddingBottom': '0px', 'text-align': 'center', 'fontWeight': 'bold'}),
            dcc.RadioItems(
               id='ts', 
               options=[ 
                  {'label': 'Ventas', 'value': 'ventas'},
                  {'label': 'Devoluciones', 'value': 'devoluciones'},
                  {'label': 'Negados', 'value': 'negados'}
                  ], value='ventas',
               labelStyle={'display': 'inline-block', 'padding': '0px', 'paddingLeft': '2px', 'paddingRight': '2px'}, 
               style={
                  'fontSize': 10, 
                  'padding': '0px', 
                  'margin': '0px'}
               ), 
            html.H6('Periódo', style={'fontSize': 11, 'padding': '2px', 'paddingBottom': '0px', 'text-align': 'center', 'fontWeight': 'bold'}),
            dcc.RadioItems(
               id='ts_period', 
               options=[ 
                  {'label': 'Día', 'value': 'D'},
                  {'label': 'Semana', 'value': 'W'},
                  {'label': 'Mes', 'value': 'M'}
                  ], value='M',
               labelStyle={'display': 'inline-block', 'padding': '0px', 'paddingLeft': '2px', 'paddingRight': '2px'}, 
               style={
                  'fontSize': 10, 
                  'padding': '0px', 
                  'margin': '0px'}
               ), 
            html.H6(children=['Periodos a Pronosticar: ', html.Span(id='ts_nforecast-label', style={'color': 'violet', 'fontSize': 14})], style={'fontSize': 11, 'padding': '4px', 'paddingBottom': '0px', 'text-align': 'left', 'fontWeight': 'bold'}),
            dcc.Slider(id='ts_nforecast', min=2, max=30, step=1, value=6), 
            ], 
            style={
               'padding': '0px', 
               'margin': '0px'
               }
            ),
         ], 
      style={
         'text-align': 'center', 
         'overflow': 'auto', 
         'height': '100%', 
         'width': '100%', 
         'margin': '0px', 
         'marginRight': '5px', 
         'marginTop': '5px', 
         'padding': '0px'}
      )

card_ts_tabla = dbc.Card(
      children=[ 
         dbc.CardHeader('Pronóstico', style={'fontSize': 12, 'padding': '2px', 'text-align': 'center', 'fontWeight': 'bold'}),
         dbc.CardBody(id='ts_table', style={'overflow': 'auto', 'fontSize': 10, 'padding': '0px', 'margin': '0px', 'text-align': 'center'}),
      ], 
      style={
         'height': '100%', 
         'width': '100%', 
         'marginRight': '5px', 
         'marginTop': '10px', 
         'padding': '0px'}
      )

# EBIT (UAFI: Utilidad antes de financiamiento e impuestos)
costo_1 = st.kpi_by_sheet(col='COSTO', x=1)
costo_2 = '0'
costo_3 = '0'
costo_4 = '0'
devs = '0'

ebit = dbc.Jumbotron(
      children=[
         dbc.Container(children=[
            html.H6('EBIT', className='display-4', style={'fontSize': '20px', 'color': 'grey', 'text-align': 'center'}), 
            dbc.Card(
               children=[
                  html.P('Ventas', style={'paddingLeft': '10px', 'margin': '0px', 'fontSize': 12}), 
                  html.P(f'{ventas_netas_1} MXN', style={'margin': '0px', 'paddingRight': '10px', 'fontSize': 10, 'text-align': 'right', 'color': 'lightseagreen'}), 

                  html.P('Devoluciones', style={'paddingLeft': '10px', 'margin': '0px', 'fontSize': 12}), 
                  html.P(f'{devs} MXN', style={'margin': '0px', 'paddingRight': '10px', 'fontSize': 10, 'text-align': 'right', 'color': 'lightcoral'}), 

                  html.P('Costo', style={'paddingLeft': '10px', 'margin': '0px', 'fontSize': 12}), 
                  html.P(f'{costo_1} MXN', style={'margin': '0px', 'paddingRight': '10px', 'fontSize': 10, 'text-align': 'right', 'color': 'lightcoral'}), 
                  ]
               ), 
            dbc.Card(
               children=[
                  html.P('Utilidad', style={'paddingLeft': '10px', 'margin': '0px', 'fontSize': 12}), 
                  html.P(f'{utilidad_1} MXN', style={'margin': '0px', 'paddingRight': '10px', 'fontSize': 10, 'text-align': 'right', 'color': 'lightseagreen'})
                     ]
                  ), 
            dbc.Card(
               children=[
                  html.P('Costo de Ventas', style={'paddingLeft': '10px', 'margin': '0px', 'fontSize': 12}), 
                  html.P(f'{costo_2} MXN', style={'margin': '0px', 'paddingRight': '10px', 'fontSize': 10, 'text-align': 'right', 'color': 'lightcoral'}), 
                  html.P(f'{costo_3} MXN', style={'margin': '0px', 'paddingRight': '10px', 'fontSize': 10, 'text-align': 'right', 'color': 'lightcoral'}), 
                  html.P(f'{costo_4} MXN', style={'margin': '0px', 'paddingRight': '10px', 'fontSize': 10, 'text-align': 'right', 'color': 'lightcoral'})
                     ]
                  ), 
            dbc.Card(
               children=[
                  html.P('Utilidad Antes de Impuestos', style={'paddingLeft': '10px', 'margin': '0px', 'fontSize': 12}), 
                  html.P(f'{utilidad_1} MXN', style={'margin': '0px', 'paddingRight': '10px', 'fontSize': 10, 'text-align': 'right', 'color': 'lightseagreen'})
                     ]
                  ), 
            ], fluid=True)
         ], 
      style={
         'height': '100%', 
         'width': '100%', 
         'padding': '0px', 
         'paddingTop': '5px', 
         'paddingLeft': '0px', 
         'paddingRight': '0px'}, 
      fluid=True
      )

# General
gral = html.Div(
      children=[
         # Static
         dbc.Row(
            children=[
               dbc.Col(card_ventas_netas, xs=12, md=6, lg=3, xl=3),
               dbc.Col(card_utilidad, xs=12, md=6, lg=3, xl=3), 
               dbc.Col(card_devoluciones, xs=12, md=6, lg=3, xl=3),
               dbc.Col(card_negados, xs=12, md=6, lg=3, xl=3),
               ], no_gutters=True
            ), 
         # Dynamic
         dbc.Row(children=[
            dbc.Col(
               children=[
                  dbc.Row(card_ts_controles, no_gutters=True, style={'height': '170px'}), 
                  dbc.Row(card_ts_tabla, no_gutters=True, style={'height': '280px'})
                  ], 
               xs=4, md=3, lg=2, xl=2, style={'marginBottom': '5px'}), 
            dbc.Col(card_ts, xs=8, md=9, lg=6, xl=6, style={'height': '450px', 'marginBottom': '2px'}), 
            dbc.Col(
               children=[
                  dbc.Row(children=[
                     dbc.Col(card_dexistencia), 
                     dbc.Col(card_desplazamiento)
                     ], no_gutters=True), 
                  dbc.Row(children=[
                     ebit
                     ], no_gutters=True, style={'height': '360px', 'margin': '10px'})
                  ], xs=12, md=12, lg=4, xl=4
               )
            ], no_gutters=True, 
            style={
               'display': 'flex', 
               'width': '100%', 
               'paddingTop': '5px'
               }), 
         ], style={
            'marginLeft': '25px', 
            'marginRight': '25px', 
            'marginTop': '5px'
            }
         )




# Sección 2; Detallado


revenue_dropdown = dcc.Dropdown(id='revenue_dropdown', 
      options=[
         {'label': 'Origen', 'value': 'origen'}, 
         {'label': 'Categoría', 'value': 'categoria'}, 
         {'label': 'Estilo', 'value': 'ESTILO'}, 
         {'label': 'Tienda', 'value': 'TIENDA'}, 
         {'label': 'Color', 'value': 'color'}, 
         {'label': 'Acabado', 'value': 'ACABADO'}, 
         {'label': 'Concepto', 'value': 'concepto'}
         ],
      value='origen', clearable=False
      )  

card_revenue_bubble = dbc.Card(
      children=[
         dcc.Graph(id='revenue_plot', 
            hoverData={'points': [{'text': 'Nacional'}]},
            config={'displayModeBar': False, 'responsive': True}, 
            style={
               'paddingLeft': '5px', 
               'paddingRight': '5px', 
               'paddingTop': '5px', 
               'paddingBottom': '0px'
               }
            )
         ], 
      style={
         'height': '100%', 
         'marginRight': '5px', 
         'marginTop': '5px', 
         'paddingTop': '0px', 
         'paddingLeft': '0px', 
         'paddingRight': '0px'}
      )


# Serie de tiempo de selección
card_ts_selection = dbc.Card(
      dcc.Graph(id='ts_plot_selection', config={'displayModeBar': False, 'responsive': True}),
      style={
         'height': '100%', 
         'marginRight': '5px', 
         'marginTop': '5px', 
         'paddingTop': '0px', 
         'paddingLeft': '0px', 
         'paddingRight': '0px'}
      )



# Detallado
detal= html.Div(
      dbc.Row(
         children=[ 
            dbc.Col(
               children=[
                  revenue_dropdown, 
                  card_revenue_bubble
                  ], width=3), 
            dbc.Col(card_ts_selection, width=9)
            ]), 
         style={
            'marginLeft': '25px', 
            'marginRight': '25px', 
            'marginTop': '5px'
            }
         )


# Tabulador
tabs_primary = dbc.Tabs(children=[
   dbc.Tab(gral, label='General', label_style={'fontSize': 14, 'height': '30px', 'fontWeight': 'bold'}), 
   dbc.Tab(detal, label='Detallado', label_style={'fontSize': 14, 'height': '30px', 'fontWeight': 'bold'})
   ], style={
      'marginTop': '5px'
      })


def layout():
   layout = html.Div(tabs_primary)
   return layout

