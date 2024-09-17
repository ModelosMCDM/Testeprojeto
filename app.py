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
page_title= "jAN",
layout="wide",
initial_sidebar_state="expanded",  # Pode ser "auto", "expanded" ou "collapsed"
)


html_temp = """
<img src="https://uvagpclass.wordpress.com/wp-content/uploads/2017/11/whatsapp-image-2017-11-02-at-08-36-14.jpeg" 

         alt="Descrição da imagem"
         style="width: 250px; height: auto;">

<div style="text-align:center; background-color: #f0f0f0; border: 1px solid #ccc; padding: 10px;">
    <h3 style="color: black; margin-bottom: 10px;">Metodologia de apoio à decisão para manutenção inteligente, combinando abordagens multicritério</h3>
    <p style="color: black; margin-bottom: 10px;"">AHP - Xxxxxx 3</p>
    <p style="color: black; margin-bottom: 10px;"">Modo de uso: Aplique-o para escolha entre  quaisquer alternativas e critérios</p>
    <p style="color: black; margin-bottom: 10px;"">Todos os métodos funcionarão automaticamente</p>
    <p style="color: black; margin-bottom: 10px;"">Jaqueline Alves do Nascimento</p>
</div>

"""

st.markdown(html_temp, unsafe_allow_html=True)



#05
def ReadSheetByNr(fileP, sheetsNrP):
  sheetP = desafioSeets[sheetsNrP]
  return pd.read_excel(fileP,sheet_name=sheetP,index_col=0)
def ReadAllSheets(fileP, sheetsP):
  resultP = []
  for x in sheetsP:
    # Lendo arquivo excel do Google Drive, por aba (sheet) utilizando Lib pandas
    resultP.append(pd.read_excel(fileP,sheet_name=x,index_col=0))
  return resultP




#<h3 style ="color:black;text-align:center;">Abrindo dados dos decisores </h3></div>

with st.container():
# Carregar uma planilha Excel
         desafioFile = st.file_uploader("Para iniciar, clique no botão Browse files para carregar a planilha em Excel com as respostas Par a Par dos decisores. ", type="xlsx")

