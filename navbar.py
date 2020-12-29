import dash_html_components as html
import dash_bootstrap_components as dbc

def Navbar():
    navbar = dbc.NavbarSimple(
          children=[
             html.A('Versión Experimental', target='_blank', href='http://187.211.53.55:8080'), 
             html.A(html.Img(src='assets/Logo.png', height='40px', width='90'), target='_blank', href='https://florsheimshoes.com.mx')
             ], 
          dark=False)

    return navbar
