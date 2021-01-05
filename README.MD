# Dashboard Zapatería Florsheim.
Para reglas de re-nombramiento de variables **color** y **concepto** revisar el script `refactor.py`.

## Estructura de archivos
```
.
├── assets
│   ├── bootstrap.min.css
│   ├── icons
│   │   ├── decrease-24.png
│   │   ├── increase-24.png
│   └── Logo.png
├── config.py
├── datos
│   └── bases
│       ├── adm_finanzas
│       │   ├── utilidades_por_art_2019.TXT
│       │   ├── utilidades_por_art_2020.TXT
│       │   ├── utilidades_por_art.TXT
│       │   ├── ventas_19-20.TXT
│       │   └── ventas_acumuladas_por_articulo.TXT
│       ├── compras
│       │   └── neg_19-20.TXT
│       └── inventario
│           └── cardex_gral_19-20.TXT
├── etc.py
├── index.py
├── navbar.py
├── README.MD
├── refactor.py
├── requirements.txt
├── snapshot.py
└── snapshot_tools.py

8 directories, 35 files
```

Catálogo de variables.

| Nuevos Valores | Concepto |
| --- | --- |
| Vestir | Vestir, Trabajo | 
| Casual/Vestir | Casual, Bota Caballero |
| Confort | Confort |
| Consumibles | Autobrillante, Producto, Crema, Cera, Limpiador, Reavivador, Renovador, Avivador, Dilatador, Jabón, Cepillo, Esponja |
| Accesorios | Cinturón, Calcetín, Cartera, Mochila |
| Dama | Dama |
| Marroquinería | Marroquinería |


| Nueva Variable | Categoría |
| Zapato | Vestir, Casual, Confort, Urbano, Botas, Sport, Trabajo, Dama |
| Accesorio | Accesorios, Consumibles |
| Otro | Marroquinería |


| Nuevos Valores | Color |
| Negro | Negro |
| Café/Chocolate | Café, Chocolate |
| Café/Cognac | Cognac, Café Claro |
| Café/Tan | Tan |
| Arena | Arena, Miel, Almendra |
| Gris | Gris |
| Vino/Burgundy | Vino | Burgundy |
| Blanco | Blanco |
| Otros | Rosa, Rojo, Plata, Oxford, Multicolor, Castaño |
| N/A | Sin Color |


| Nueva Variable | Tono |
| Oscuro | Negro, Chocolate, Vino, Azul Marino |
| Mediano | Café, Azul, Cognac | 
| Claro | Café Claro, Tan, Arena, Miel, Almendra, Veige, Gris, Blanco | 
| N/A | Sin Color |


| Nueva Variable | Material |
| Piel | Piel, Gamuza, Cerdo, Ternera, Becerro, Venado, Ante Buck, Ante Nobuck, Charol | 
| Tela | Algodón, Nylon, Sintético, Lona |


| Nueva Variable | Origen |
| Empieza con F | Nacional |
| Empieza con 5 caracteres seguidos de un guión | Internacional | 



