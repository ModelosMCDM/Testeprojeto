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
page_title= "MESTRADO",
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
    <p style="color: black; margin-bottom: 10px;"">Modo de uso: Aplique-o para escolha entre 8 quaisquer alternativas e 6 critérios</p>
    <p style="color: black; margin-bottom: 10px;"">Todos os métodos funcionarão automaticamente</p>
    <p style="color: black; margin-bottom: 10px;"">Após o upload da planilha dos decisores, caso queira interagir com o Framework vá na seção 2.1 - MOORA</p>
</div>

"""

st.markdown(html_temp, unsafe_allow_html=True)


#02 FUNCAO SAATY
def DadosSaaty(lamb, N):
    ri = np.array([0, 0, 0.58, 0.9, 1.12, 1.32, 1.35, 1.41, 1.45, 1.49, 1.52, 1.54, 1.56, 1.58, 1.59])
    ci = (lamb - N) / (N - 1)

    if N < len(ri):
        cr = ci / ri[N]
        if np.any(cr > 0.1):
            return 'Inconsistente: %.2f' % np.max(cr)
        else:
            return 'É Consistente: %.2f' % np.max(cr)
    else:
        return 'Número de elementos excede o tamanho de ri'

#if np.any(cr > 0.1) Verifica se pelo menos um dos valores em cr é maior que 0.1.
#Se algum valor exceder esse limite, a matriz de julgamento é considerada inconsistente.


#FUNCAO CONSISTENCIA
def VV(Consistencia):
    l, v = np.linalg.eig(Consistencia)
    v = v.T
    i = np.where(l == np.max(l))[0][0]
    l = l[i]
    v = v[i]
    v = v / np.sum(v)
    return np.real(l), np.real(v)

#03 Função que normaliza dados sem soma e peso

def NormalizingConsistency(dataP):
  resultP = dataP
  columnsP = resultP.columns.tolist()
  for x in columnsP:
    resultP[x] = resultP[x]/sum(resultP[x])

  return resultP


def NormalizingCritera(dataP):
  resultP = dataP
  columnsP = resultP.columns.tolist()
  resultP["Csoma"] = 0
  for x in columnsP:
    resultP[x] = resultP[x]/sum(resultP[x])
    resultP["Csoma"] += resultP[x]

  resultP['MatrizdePeso'] = resultP["Csoma"]/len(columnsP)
  return resultP


#04 Função que normaliza uma lista de dados
def NormalizingAll(dataListP):
  resultP2 = []
  for x in dataListP:
    # Lendo arquivo excel do Google Drive, por aba (sheet) utilizando Lib pandas
    resultP2.append(NormalizingCritera(x))
  return resultP2


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

#06
desafioNormalAll = []
desafioDataAll = []
desafioAlternativas = []
#desafioSeets = ['Par_criterios_gerente','Cr01_Falhas_gerente','Cr02_Seguranca_gerente','Cr03_OEE_gerente','Cr04_Custo_gerente','Cr05_Preventiva_gerente',
#  'Cr06_Treinamento_gerente']
#desafioLabels = ['Par_criterios_gerente','Cr01_Falhas_gerente','Cr02_Seguranca_gerente','Cr03_OEE_gerente','Cr04_Custo_gerente','Cr05_Preventiva_gerente',
#  'Cr06_Treinamento_gerente']

desafioSeets = ['Par_criterios_gerente','Cr01_Falhas_gerente','Cr02_Seguranca_gerente','Cr03_OEE_gerente','Cr04_Custo_gerente','Cr05_Preventiva_gerente','Cr06_Treinamento_gerente',
  'Par_criterios_sup7','Cr01_Falhas_sup8','Cr02_Seguranca_sup9','Cr03_OEE_sup10','Cr04_Custo_sup11','Cr05_Preventiva_sup12','Cr06_Treinamento_sup13',
  'Par_criteriosTec1_14','Cr01_FalhasTec1_15','Cr02_SegurancaTec1_16','Cr03_OEETec1_17','Cr04_CustoTec1_18','Cr05_PreventivaTec1_19','Cr06_TreinamentoTec1_20',
  'Par_criteriosTec2_21','Cr01_FalhasTec2_22','Cr02_SegurancaTec2_23','Cr03_OEETec2_24','Cr04_CustoTec2_25','Cr05_PreventivaTec2_26','Cr06_TreinamentoTec2_27']

desafioLabels = ['Par_criterios_gerente','Cr01_Falhas_gerente','Cr02_Seguranca_gerente','Cr03_OEE_gerente','Cr04_Custo_gerente','Cr05_Preventiva_gerente','Cr06_Treinamento_gerente',
  'Par_criterios_sup7','Cr01_Falhas_sup8','Cr02_Seguranca_sup9','Cr03_OEE_sup10','Cr04_Custo_sup11','Cr05_Preventiva_sup12','Cr06_Treinamento_sup13',
  'Par_criteriosTec1_14','Cr01_FalhasTec1_15','Cr02_SegurancaTec1_16','Cr03_OEETec1_17','Cr04_CustoTec1_18','Cr05_PreventivaTec1_19','Cr06_TreinamentoTec1_20',
  'Par_criteriosTec2_21','Cr01_FalhasTec2_22','Cr02_SegurancaTec2_23','Cr03_OEETec2_24','Cr04_CustoTec2_25','Cr05_PreventivaTec2_26','Cr06_TreinamentoTec2_27']

#........................


#<h3 style ="color:black;text-align:center;">Abrindo dados dos decisores </h3></div>

with st.container():
  #st.subheader("Carregando o Projeto")
#  st.markdown("<h2 style='text-align: left;'>--- Iniciando o sistema para tomada de decisões gerenciais --- </h3>", unsafe_allow_html=True)

# Carregar uma planilha Excel
         desafioFile = st.file_uploader("Para iniciar, clique no botão Browse files para carregar a planilha em Excel com as respostas Par a Par dos decisores. ", type="xlsx")

if desafioFile is not None:
    try:
        # Ler a planilha Excel
        df = pd.read_excel(desafioFile)

        # Mostrar os dados
        #st.write("Dados da planilha:")
        #st.write(df)
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {str(e)}")
else:
    st.info("Por favor, faça o upload do arquivo Dados_decisores.xlsx.")
    sys.exit()

with st.container():
    st.markdown("<h2 style='text-align: center; background-color: #6495ED;'>01 - Método AHP</h2>", unsafe_allow_html=True)
#07

st.subheader("1.1 - Gerando a Matriz de comparação dos 5 critérios - Decisor Gerente:")
