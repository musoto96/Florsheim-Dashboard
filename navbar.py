import dash_html_components as html
import dash_bootstrap_components as dbc

def Navbar():
    navbar = dbc.NavbarSimple(
          children=[
             html.A('Versión Experimental', target='_blank', href='189.253.150.229:8085'), 
             html.A(html.Img(src='assets/Logo.png', height='40px', width='90'), target='_blank', href='https://florsheimshoes.com.mx')
             ], 
          dark=False)

    return navbar
