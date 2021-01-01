# Este script contiene la recategorizacion de variables

# Los valores a la izquierda en los diccionarios (llaves), son las nuevas categorías, 
#  los valores a la derecha(valores) son, las categorias existetes (en letra minúscula).
#
#
# Categorías cambiadas:
# - color
# - concepto
# 
# Categorías agregadas:
# - origen
# - tono

import numpy as np
import pandas as pd


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


# ARTÍCULO CONCEPTO
con = {
        'Vestir': ['vestir', 'trabajo'], 
        'Casual/Vestir': ['casual', 'botas caballero', 'bota caballero'], 
        'Confort': ['confort'], 
        'Sport': ['sport', 'urbano'], 
        'Consumibles': ['autobrillante', 'producto', 'crema', 'cera', 'limpiador', 'reavivador', 'renovador', 'avivador', 'dilatador', 'jabon', 'jabón', 'cepillo', 'esponja'], 
        'Accesorios': ['cinturon', 'cinturón', 'calcetin', 'calcetín', 'cartera', 'mochila'], 
        'Dama': ['dama'], 
        'Marroquineria': ['marroquineria', 'marroquinería']
    }
cat = {
        'Zapato': ['vestir', 'casual', 'confort', 'urbano', 'botas', 'bota', 'botin', 'sport', 'trabajo', 'dama'], 
        'Accesorio': ['accesorios', 'consumibles'], 
        'Otro': ['marroquineria']
    }

def refactor_concepto_categoria(df, col_concepto='ARTÍCULO CONCEPTO'):
   df.copy()
   df.insert(loc=df.columns.get_loc(col_concepto)+1, 
         column='concepto', value=df.loc[:, col_concepto].apply(like, args=(con, )))
   df.insert(loc=df.columns.get_loc(col_concepto), 
         column='categoria', value=df.loc[:, 'concepto'].apply(like, args=(cat, )))
   df.drop(columns=[col_concepto], inplace=True)
   return df


# ARTÍCULO COLOR
color = {
        'Negro': ['negro'], 
        'Café/Chocolate': ['cafe', 'café', 'chocolate'], 
        'Café/Cognac': ['cognac', 'cafe claro', 'café claro'], 
        'Café/Tan': ['tan'], 
        'Arena': ['arena', 'miel', 'almendra'], 
        'Azul Marino': ['azul', 'azul marino'], 
        'Gris': ['gris'],
        'Vino/Burgundy': ['vino', 'burgundy'], 
        'Blanco': ['blanco'], 
        'Otros': ['rosa', 'rojo', 'plata', 'oxford', 'multicolor', 'castaño'], 
        'N/A': ['sin color']
        }
tono = {
        'Oscuro': ['negro', 'chocolate', 'vino', 'azul marino'], 
        'Mediano': ['café', 'cafe', 'azul', 'cognac'], 
        'Claro': ['café claro', 'cafe claro', 'tan', 'arena', 'miel', 'almendra', 'veige', 'gris', 'blanco'], 
        'N/A': ['sin color']
        }

def refactor_color_tono(df, col_color='ARTÍCULO COLOR'):
   df.insert(loc=df.columns.get_loc(col_color)+1, 
         column='color', value=df.loc[:, col_color].apply(like, args=(color, )))
   df.insert(loc=df.columns.get_loc('color')+2, 
         column='tono', value=df.loc[:, col_color].apply(like, args=(tono, )))
   df.drop(columns=[col_color], inplace=True)
   return df


# ARTÍCULO ACABADO
# sin usar
material = {
        'Piel': ['piel', 'gamuza', 'cerdo', 'ternera', 'ternero', 'becerro', 'venado', 'ante buck', 'ante nobuck', 'charol'], 
        'Tela': ['algodon', 'nylon', 'sintetico', 'lona']
        }


# zapato ARTÍCULO ESTILO -> nacional / internacional
def orig(x):
    if str(x).startswith('F'):
        return 'Nacional'
    elif len(str(x).split('-')[0]) == 5:
        return 'Internacional'


def refactor_origen(df, col_estilo='ARTÍCULO ESTILO'):
   df.insert(loc=df.columns.get_loc(col_estilo)+1, 
         column='origen', value=df.loc[:, col_estilo].map(orig, na_action='ignore'))
   return df


def refactor_all(df, col_concepto, col_color, col_estilo):
   df = refactor_concepto_categoria(df, col_concepto)
   df = refactor_color_tono(df, col_color)
   df = refactor_origen(df, col_estilo)
   return df


