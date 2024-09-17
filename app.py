# 1° importa a biblioteca pandass

import sys
import streamlit as st
import numpy as np
import pandas as pd
from sklearn.preprocessing import Normalizer
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")
backgroundColor = "#ADD8E6"

# set page configuration
st.set_page_config(
page_title= "TOTOTOTOTOO",
layout="wide",
initial_sidebar_state="expanded",  # Pode ser "auto", "expanded" ou "collapsed"
)


html_temp = """
<img src="https://www.casadamoeda.gov.br/portal/imgs/logo-cmb-4.png" 
         alt="Descrição da imagem"
         style="width: 250px; height: auto;">

<div style="text-align:center; background-color: #f0f0f0; border: 1px solid #ccc; padding: 10px;">
    <h3 style="color: black; margin-bottom: 10px;">Metodologia de apoio à decisão para manutenção inteligente, combinando abordagens multicritério</h3>
    <p style="color: black; margin-bottom: 10px;"">Projeto desenvolvido no Mestrado acadêmico em Engenharia de Produção | DEI - Departamento de Engenharia Industrial - 2023</p>
   
</div>

