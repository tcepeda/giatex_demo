import os
import pandas as pd
import numpy as np

""" 
Definir Hashtable Upper Limit, Lower Limit
Remove     'Cor\n(Pt-Co)': [,],     'Azoto amoniacal (mg/L)': [,],     'Hidrocarbonetos totais\n(mg/L)': [,],     'Óleos e gorduras\n(mg/L)': [,],     'Fósforo total (mg/L)': [,],
"""
limites_aquatex = {
    'Parametro': ['Upper', 'Lower'],
    'pH': [9,6],
    'Condutividade': [900,0],
    'Alcalinidade': [200,0],
    'Dureza': [45,0],
    'Turbidez': [1,0],
    'Sólidos_suspensos_totais': [5,0],
    'Carência_química_de_oxigénio': [50,0],
    'Carência_bioquímica_de_oxigénio': [20,0],
    'Carbono_orgânico_total': [30,0],
    'Azoto_total': [20,0],
    'Nitratos': [10,0],
    'Nitritos': [100,0],
    'Alumínio': [0.2,0],
    'Chumbo': [0.1,0],
    'Cobre': [0.2,0],
    'Crómio_total': [0.05,0],
    'Ferro': [0.2,0],
    'Manganês': [0.2,0],
    'Magnésio': [10,0],
    'Zinco': [1.5,0],
    'Cálcio': [80,0],
    'Cloretos': [300,0],
    'Sulfatos': [200,0],
    'Sulfitos': [1,0],
    'Sulfuretos': [5,0],
    'Detergentes_aniónicos': [0.025,0]
    }
