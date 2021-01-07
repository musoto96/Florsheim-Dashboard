import numpy as np
import pandas as pd
import scipy
import datetime
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from pmdarima.arima import auto_arima
import importlib


st = importlib.import_module(name='snapshot_tools')  # snapshot tools

# Autoarima
data = st.time_series(df=st.base, date_col='NOTA DE VENTA FECHA', 
      n_col='ARTÍCULO SUBTOTAL', f0=2020, period='Y', ts_period='D')

model = auto_arima(data, m=7)
print(model.summary())


