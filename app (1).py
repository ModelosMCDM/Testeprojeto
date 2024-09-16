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

sheetNr = 0
print(desafioLabels[sheetNr])

# Busca dados da planilha
desafioData = ReadSheetByNr(desafioFile, sheetNr);
desafioData


#08
#2.4
st.subheader("1.2 Normalizando os valores dos critérios - Decisor Gerente")
# Normaliza dados
normalizandocriterio = NormalizingConsistency(desafioData);
normalizandocriterio


#09
st.subheader("1.3 - Consistencia (01) dos dados de critério vs objetivo (LOCAL) onde é comparado os 6 critérios par a par - Decisor Gerente")
st.write("transformando em array")
array_ahp = normalizandocriterio.to_numpy()
array_ahp

# Verificação de consistência
N = len(array_ahp)
lamb = np.sum(array_ahp, axis=1)
result = DadosSaaty(lamb, N)
# Exibindo o resultado na tela
st.write("Resultado da Verificação de Consistência:")
st.markdown(result)

# Realizando o cálculo VV se os dados são consistentes
if "Consistente" in result:
    l, v = VV(array_ahp)
    st.write("Autovalor (l):", l)
    #st.write("Autovetor (v):", v)
    st.write("Autovetor (v):", ' '.join(map(str, v)))



#11
st.subheader("1.4 Vetor de peso - Decisor Gerente")

desafioNormal = NormalizingCritera(desafioData);
desafioNormalAll.append(desafioNormal)
desafioNormal


#12
st.subheader("1.5 Gráfico matriz de peso - Grafico Gerente")

desafioNormal[desafioSeets[sheetNr]] = desafioNormal.index
plt.figure(figsize=(22,2))
plt.title("Matriz de peso", fontsize=14)

ax = sns.barplot(x=desafioSeets[sheetNr], y='MatrizdePeso', data=desafioNormal)

# Aqui vem a parte para incluir os rótulos:
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x() + p.get_width() / 2, height + 0, '{:1.2f}'.format((height)), ha='center', fontsize=12)

# Exibe o gráfico usando st.pyplot()
st.pyplot(plt)


#13
st.subheader("1.6 Critério 01 Falhas - Decisor Gerente")
st.write("Lendo os dados do decisor")

sheetNr = 1
print(desafioLabels[sheetNr])

# Busca dados da planilha
desafioData = ReadSheetByNr(desafioFile, sheetNr);
desafioData

#11
st.subheader("1.7 Normalizando o criterio Falhas - Decisor Gerente")

# Normaliza dados
desafioNormal = NormalizingCritera(desafioData);
desafioNormalAll.append(desafioNormal)
desafioNormal


st.subheader("1.8 Teste de consistência do critério 01 Falhas - Decisor Gerente")
st.write("Nova matriz do criterio normalizada sem soma e peso")
#Retira-se a Soma e  matriz de peso. Se não tirar não funciona.
desafioNormal2 = desafioNormal.copy()
del desafioNormal2['Csoma']
del desafioNormal2['MatrizdePeso']
desafioNormal2


st.write("Transformando para array")
#00
#teste de consistencia recebe o nome da matriz ja normalizada para teste Assim....  ""  Consistencia00 = nometabela.to_numpy()
array_criterio1 = desafioNormal2.to_numpy()
array_criterio1


# Verificação de consistência
N = len(array_criterio1)
lamb = np.sum(array_criterio1, axis=1)
result = DadosSaaty(lamb, N)
# Exibindo o resultado na tela
st.write("Resultado da Verificação de Consistência:")
st.markdown(result)

# Realizando o cálculo VV se os dados são consistentes
if "Consistente" in result:
    l, v = VV(array_criterio1)
    st.write("Autovalor (l):", l)
    #st.write("Autovetor (v):", v)
    st.write("Autovetor (v):", ' '.join(map(str, v)))


#2.9
st.subheader("1.9 Critério  Segurança - Decisor Gerente")
st.write("Lendo os dados do decisor")

sheetNr = 2
print(desafioLabels[sheetNr])

# Busca dados da planilha
DadosCriterioSeguranca = ReadSheetByNr(desafioFile, sheetNr);
DadosCriterioSeguranca


# Normaliza dados
st.write("1.10 Normalizando o criterio seguranca - Decisor Gerente")
NormalizandoSeguranca = NormalizingCritera(DadosCriterioSeguranca);
desafioNormalAll.append(NormalizandoSeguranca)
NormalizandoSeguranca

st.write("1.11 Recebendo a matriz do criterio segurança normalizada - Decisor Gerente")
#Retira-se a Soma e  mtriz de peso. Se não tirar não funciona.
ajustetabelaseguranca = NormalizandoSeguranca.copy()
del ajustetabelaseguranca['Csoma']
del ajustetabelaseguranca['MatrizdePeso']
ajustetabelaseguranca

st.write("1.12 Transformando para array")
#00
#teste de consistencia recebe o nome da matriz ja normalizada para teste Assim....  ""  Consistencia00 = nometabela.to_numpy()
array_criterio2 = ajustetabelaseguranca.to_numpy()
array_criterio2


# Verificação de consistência
N = len(array_criterio2)
lamb = np.sum(array_criterio2, axis=1)
result = DadosSaaty(lamb, N)
# Exibindo o resultado na tela
st.write("Resultado da Verificação de Consistência:")
st.markdown(result)

# Realizando o cálculo VV se os dados são consistentes
if "Consistente" in result:
    l, v = VV(array_criterio2)
    st.write("Autovalor (l):", l)
    #st.write("Autovetor (v):", v)
    st.write("Autovetor (v):", ' '.join(map(str, v)))


#2.10
st.subheader("1.13 Critério 03 OEE - Decisor Gerente")
st.write("Lendo os dados do decisor")
sheetNr = 3
print(desafioLabels[sheetNr])

# Busca dados da planinha
desafioData = ReadSheetByNr(desafioFile, sheetNr);
desafioData


st.write("1.14 Normalizando o criterio OEE")
# Normaliza dados
NormalizandoOEE = NormalizingCritera(desafioData);
desafioNormalAll.append(NormalizandoOEE)
NormalizandoOEE

st.write("1.15 Teste de consistência do critério OEE")
#Retira-se a Soma e  mtriz de peso. Se não tirar não funciona.
ajustetabelaOEE = NormalizandoSeguranca.copy()
del ajustetabelaOEE['Csoma']
del ajustetabelaOEE['MatrizdePeso']
ajustetabelaOEE

st.write("1.16 Transformando para array")
#00
array_criterio3 = ajustetabelaOEE.to_numpy()
array_criterio3

# Verificação de consistência
N = len(array_criterio3)
lamb = np.sum(array_criterio1, axis=1)
result = DadosSaaty(lamb, N)
# Exibindo o resultado na tela
st.write("Resultado da Verificação de Consistência:")
st.markdown(result)

# Realizando o cálculo VV se os dados são consistentes
if "Consistente" in result:
    l, v = VV(array_criterio3)
    st.write("Autovalor (l):", l)
    #st.write("Autovetor (v):", v)
    st.write("Autovetor (v):", ' '.join(map(str, v)))


#2.11
st.subheader("1.17 Critério 04 Custo - Decisor Gerente")
st.write("Lendo os dados do decisor")

#19
sheetNr = 4
print(desafioLabels[sheetNr])
desafioData = ReadSheetByNr(desafioFile, sheetNr);
desafioData

st.write("1.18 Normalizando o critério CUSTO")
#20
NormalizandoCusto = NormalizingCritera(desafioData);
desafioNormalAll.append(NormalizandoCusto)
NormalizandoCusto

st.write("1.19 Teste de consistência do critério Custo")
#Retira-se a Soma e  mtriz de peso. Se não tirar não funciona.
ajustetabelaCusto = NormalizandoSeguranca.copy()
del ajustetabelaCusto['Csoma']
del ajustetabelaCusto['MatrizdePeso']
ajustetabelaCusto

st.write("1.20 Transformando para array")
array_criterio4 = ajustetabelaCusto.to_numpy()

# Verificação de consistência
N = len(array_criterio4)
lamb = np.sum(array_criterio4, axis=1)
result = DadosSaaty(lamb, N)
# Exibindo o resultado na tela
st.write("Resultado da Verificação de Consistência:")
st.markdown(result)

# Realizando o cálculo VV se os dados são consistentes
if "Consistente" in result:
    l, v = VV(array_criterio4)
    st.write("Autovalor (l):", l)
    #st.write("Autovetor (v):", v)
    st.write("Autovetor (v):", ' '.join(map(str, v)))

#2.12 Critério 05 Preventiva
st.subheader("1.21 Critério 05 Preventiva - Decisor Gerente")
st.write("Lendo os dados do decisor")
#22
sheetNr = 5
print(desafioLabels[sheetNr])
desafioData = ReadSheetByNr(desafioFile, sheetNr);
desafioData

st.write("1.22 Normalizando o criterio Preventiva")
NormalizandoPreventiva = NormalizingCritera(desafioData);
desafioNormalAll.append(NormalizandoPreventiva)
NormalizandoPreventiva

st.write("1.23 Teste de consistência do critério Preventiva")
st.write("Recebendo a matriz do criterio normalizada")
#Retira-se a Soma e  mtriz de peso. Se não tirar não funciona.
ajustetabelaPreventiva = NormalizandoPreventiva.copy()
del ajustetabelaPreventiva['Csoma']
del ajustetabelaPreventiva['MatrizdePeso']
ajustetabelaPreventiva

st.write("1.24 Transformando para array")
#00
#teste de consistencia recebe o nome da matriz ja normalizada para teste Assim....  ""  Consistencia00 = nometabela.to_numpy()
array_criterio5 = ajustetabelaPreventiva.to_numpy()
st.write(array_criterio5)

# Verificação de consistência
N = len(array_criterio5)
lamb = np.sum(array_criterio5, axis=1)
result = DadosSaaty(lamb, N)
# Exibindo o resultado na tela
st.write("Resultado da Verificação de Consistência:")
st.markdown(result)

# Realizando o cálculo VV se os dados são consistentes
if "Consistente" in result:
    l, v = VV(array_criterio5)
    st.write("Autovalor (l):", l)
    #st.write("Autovetor (v):", v)
    st.write("Autovetor (v):", ' '.join(map(str, v)))



#2.13 Critério 06 Treinamento
st.subheader("1.25 Critério 06 Treinamento - Decisor Gerente")
st.write("Lendo os dados do decisor")
sheetNr = 6
print(desafioLabels[sheetNr])
desafioData = ReadSheetByNr(desafioFile, sheetNr);
desafioData


st.write("1.26 Normalizando o critério Treinamento")
NormalizandoTreinamento = NormalizingCritera(desafioData);
desafioNormalAll.append(NormalizandoTreinamento)
NormalizandoTreinamento


st.write("1.27 Teste de consistência do critério Treinamento")
ajustetabelaTreinamento = NormalizandoTreinamento.copy()
del ajustetabelaTreinamento['Csoma']
del ajustetabelaTreinamento['MatrizdePeso']
ajustetabelaTreinamento


st.write("1.28 Transformando para array")
array_criterio6 = ajustetabelaTreinamento.to_numpy()
st.write(array_criterio6)

# Verificação de consistência
N = len(array_criterio6)
lamb = np.sum(array_criterio6, axis=1)
result = DadosSaaty(lamb, N)
# Exibindo o resultado na tela
st.write("Resultado da Verificação de Consistência:")
st.markdown(result)

# Realizando o cálculo VV se os dados são consistentes
if "Consistente" in result:
    l, v = VV(array_criterio6)
    st.write("Autovalor (l):", l)
    #st.write("Autovetor (v):", v)
    st.write("Autovetor (v):", ' '.join(map(str, v)))



st.subheader("1.29  Finalizando Matriz de pesos locais - Priorização das alternativas - Decisor Gerente")
st.write("PARA ENVIAR AO MOORA DADOS GERENTE")
#25

# Criando Matriz de Priorização das alternativas
matrizData = pd.DataFrame(desafioNormalAll[0]['MatrizdePeso'])
criteriosList = desafioNormalAll[0].index.tolist();
alternativasList = desafioNormalAll[1].index.tolist();
# print(criteriosList)
# print(alternativasList)

for x in alternativasList:
  auxList = [];
  for x2 in criteriosList:
    i = criteriosList.index(x2) + 1
    auxList.append(desafioNormalAll[i]['MatrizdePeso'][x])
  matrizData[x] = auxList
#matrizData

#armazenando em um DataFrame
MatrizDePesoGerenteParaAHP = matrizData.transpose()
# Exibindo o DataFrame resultante
MatrizDePesoGerenteParaAHP


#26

somaData = list_of_zeros = [0] * len(alternativasList)

matrizPesoXAlt = matrizData.to_numpy()
i = 0
for x in matrizPesoXAlt:
    p = matrizPesoXAlt[i][0]
    j = 0
    for x2 in x:
        if j > 0:
            pa = p * matrizPesoXAlt[i][j]
            matrizPesoXAlt[i][j] = pa
            somaData[j - 1] += matrizPesoXAlt[i][j]
        j = j + 1

    i = i + 1
matrizPesoXAlt

somaTable = pd.DataFrame([somaData], index=['SOMA'], columns=alternativasList)
somaTable



st.subheader("1.30 Resultado RankingDecisor_01_de_04_Gerado_No_AHP - Gerente")
#28
RankingDecisor1 = pd.DataFrame(somaData, index=alternativasList, columns=['RankinDecisor_01_de_04_Gerado_No_AHP'])
RankingDecisor1_sorted = RankingDecisor1.sort_values(by=['RankinDecisor_01_de_04_Gerado_No_AHP'], ascending=False)

# Exibir DataFrame ordenado
st.write(RankingDecisor1_sorted)


#........................
with st.container():
  st.write("---")


#29
st.subheader("1.31 - Gerando a Matriz de comparação dos 5 critérios - Decisor Supervisor:")
sheetNr = 7
print(desafioLabels[sheetNr])

# Busca dados da planilha
desafioData = ReadSheetByNr(desafioFile, sheetNr);
desafioData



#2.4
st.subheader("1.32 - Normalizando os valores dos critérios - Decisor Supervisor")
# Normaliza dados
normalizandocriterio = NormalizingConsistency(desafioData);
normalizandocriterio


#09
st.subheader("1.33 - Consistencia (01) dos dados de critério vs objetivo (LOCAL) onde é comparado os 6 critérios par a par - Decisor Gerente")
Consistencia1 = normalizandocriterio.to_numpy()
Consistencia1



st.subheader("Obtém o autovetor e autovalor e Calcula a consistência - Decisor Supervisor ")
l, v = VV(Consistencia1)

#print('Autovalor: %.2f' %l)
#print('Autovetor: ', np.round(v, 2))

DadosSaaty(l, Consistencia1.shape[0])




#11
st.subheader("1.34 Vetor de peso - Decisor Supervisor")

desafioNormal = NormalizingCritera(desafioData);
desafioNormalAll.append(desafioNormal)
desafioNormal


#12
st.subheader("1.35 Gráfico matriz de peso - Grafico Supervisor")

desafioNormal[desafioSeets[sheetNr]] = desafioNormal.index
plt.figure(figsize=(22,2))
plt.title("Matriz de peso", fontsize=20)

ax = sns.barplot(x=desafioSeets[sheetNr], y='MatrizdePeso', data=desafioNormal)

# Aqui vem a parte para incluir os rótulos:
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x() + p.get_width() / 2, height + 0, '{:1.2f}'.format((height)), ha='center', fontsize=12)

# Exibe o gráfico usando st.pyplot()
st.pyplot(plt)

#13
st.subheader("1.36 Critério 01 Falhas - Decisor Supervisor")
st.write("Lendo os dados do decisor")

sheetNr = 8
print(desafioLabels[sheetNr])

# Busca dados da planilha
desafioData = ReadSheetByNr(desafioFile, sheetNr);
desafioData

#11
st.subheader("1.37 Normalizando o criterio Falhas - Decisor Supervisor")

# Normaliza dados
desafioNormal = NormalizingCritera(desafioData);
desafioNormalAll.append(desafioNormal)
desafioNormal


st.subheader("1.38 Teste de consistência do critério 01 Falhas - Decisor Supervisor")
st.write("Recebendo a matriz do criterio normalizada")
#Retira-se a Soma e  matriz de peso. Se não tirar não funciona.
desafioNormal2 = desafioNormal.copy()
del desafioNormal2['Csoma']
del desafioNormal2['MatrizdePeso']
desafioNormal2


st.write("1.39 Transformando para array")
#00
#teste de consistencia recebe o nome da matriz ja normalizada para teste Assim....  ""  Consistencia00 = nometabela.to_numpy()
array_criterio11 = desafioNormal2.to_numpy()
array_criterio11

# Verificação de consistência
N = len(array_criterio11)
lamb = np.sum(array_criterio11, axis=1)
result = DadosSaaty(lamb, N)
# Exibindo o resultado na tela
st.write("Resultado da Verificação de Consistência:")
st.markdown(result)

# Realizando o cálculo VV se os dados são consistentes
if "Consistente" in result:
    l, v = VV(array_criterio11)
    st.write("Autovalor (l):", l)
    #st.write("Autovetor (v):", v)
    st.write("Autovetor (v):", ' '.join(map(str, v)))



#2.9
st.subheader("1.40 Critério 02 Segurança - Decisor Supervisor")
st.write("Lendo os dados do decisor")

sheetNr = 9
print(desafioLabels[sheetNr])

# Busca dados da planilha
DadosCriterioSeguranca = ReadSheetByNr(desafioFile, sheetNr);
DadosCriterioSeguranca


# Normaliza dados
st.write("1.41 Normalizando o criterio seguranca - Decisor Supervisor")
NormalizandoSeguranca = NormalizingCritera(DadosCriterioSeguranca);
desafioNormalAll.append(NormalizandoSeguranca)
NormalizandoSeguranca

st.write("1.42 Recebendo a matriz do criterio segurança normalizada - Decisor supervisor")
#Retira-se a Soma e  mtriz de peso. Se não tirar não funciona.
ajustetabelaseguranca = NormalizandoSeguranca.copy()
del ajustetabelaseguranca['Csoma']
del ajustetabelaseguranca['MatrizdePeso']
ajustetabelaseguranca

st.write("Transformando para array")
#00
#teste de consistencia recebe o nome da matriz ja normalizada para teste Assim....  ""  Consistencia00 = nometabela.to_numpy()
ConsistenciaSeguranca = ajustetabelaseguranca.to_numpy()
ConsistenciaSeguranca


st.write("1.43 Resultado consistencia critério 02 segurança - Decisor Supervisor")

l, v = VV(ConsistenciaSeguranca)

print('Autovalor: %.2f' %l)
print('Autovetor: ', np.round(v, 2))

DadosSaaty(l, ConsistenciaSeguranca.shape[0])


#2.10
st.subheader(" 1.44. Critério 03 OEE - Decisor Supervisor")
st.write("Lendo os dados do decisor")
sheetNr = 10
print(desafioLabels[sheetNr])

# Busca dados da planinha
desafioData = ReadSheetByNr(desafioFile, sheetNr);
desafioData


st.write(" 1.45 Normalizando o criterio OEE")
# Normaliza dados
NormalizandoOEE = NormalizingCritera(desafioData);
desafioNormalAll.append(NormalizandoOEE)
NormalizandoOEE

st.write("1.46 Teste de consistência do critério OEE")
#Retira-se a Soma e  mtriz de peso. Se não tirar não funciona.
ajustetabelaOEE = NormalizandoSeguranca.copy()
del ajustetabelaOEE['Csoma']
del ajustetabelaOEE['MatrizdePeso']
ajustetabelaOEE

st.write("1.47 Transformando para array")
#00
#teste de consistencia recebe o nome da matriz ja normalizada para teste Assim....  ""  Consistencia00 = nometabela.to_numpy()
array_criterio33 = ajustetabelaOEE.to_numpy()
array_criterio33

# Verificação de consistência
N = len(array_criterio33)
lamb = np.sum(array_criterio33, axis=1)
result = DadosSaaty(lamb, N)
# Exibindo o resultado na tela
st.write("Resultado da Verificação de Consistência:")
st.markdown(result)

# Realizando o cálculo VV se os dados são consistentes
if "Consistente" in result:
    l, v = VV(array_criterio33)
    st.write("Autovalor (l):", l)
    #st.write("Autovetor (v):", v)
    st.write("Autovetor (v):", ' '.join(map(str, v)))



#2.11
st.subheader("1.48 Critério 04 Custo - Decisor Supervisor")
st.write("Lendo os dados do decisor")

#19
sheetNr = 11
print(desafioLabels[sheetNr])
desafioData = ReadSheetByNr(desafioFile, sheetNr);
desafioData

st.write("1.49 Normalizando o critério CUSTO")
#20
NormalizandoCusto = NormalizingCritera(desafioData);
desafioNormalAll.append(NormalizandoCusto)
NormalizandoCusto

st.write("1.50 Teste de consistência do critério Custo")
#Retira-se a Soma e  mtriz de peso. Se não tirar não funciona.
ajustetabelaCusto = NormalizandoSeguranca.copy()
del ajustetabelaCusto['Csoma']
del ajustetabelaCusto['MatrizdePeso']
ajustetabelaCusto

st.write("1.51 Transformando para array")
array_criterio44 = ajustetabelaCusto.to_numpy()
array_criterio44 = ajustetabelaCusto.to_numpy()

# Verificação de consistência
N = len(array_criterio44)
lamb = np.sum(array_criterio44, axis=1)
result = DadosSaaty(lamb, N)
# Exibindo o resultado na tela
st.write("Resultado da Verificação de Consistência:")
st.markdown(result)

# Realizando o cálculo VV se os dados são consistentes
if "Consistente" in result:
    l, v = VV(array_criterio44)
    st.write("Autovalor (l):", l)
    #st.write("Autovetor (v):", v)
    st.write("Autovetor (v):", ' '.join(map(str, v)))



#2.12 Critério 05 Preventiva
st.subheader("1.52 Critério 05 Preventiva - Decisor Supervisor")
st.write("Lendo os dados do decisor")
#22
sheetNr = 12
print(desafioLabels[sheetNr])
desafioData = ReadSheetByNr(desafioFile, sheetNr);
desafioData

st.write("1.53 1Normalizando o criterio Preventiva")
NormalizandoPreventiva = NormalizingCritera(desafioData);
desafioNormalAll.append(NormalizandoPreventiva)
NormalizandoPreventiva

st.write("1.54 Teste de consistência do critério Preventiva Supervisor")
st.write("Recebendo a matriz do criterio normalizada")
#Retira-se a Soma e  mtriz de peso. Se não tirar não funciona.
ajustetabelaPreventiva = NormalizandoPreventiva.copy()
del ajustetabelaPreventiva['Csoma']
del ajustetabelaPreventiva['MatrizdePeso']
ajustetabelaPreventiva

st.write("Transformando para array")
#00
#teste de consistencia recebe o nome da matriz ja normalizada para teste Assim....  ""  Consistencia00 = nometabela.to_numpy()
array_criterio55 = ajustetabelaPreventiva.to_numpy()
array_criterio55

# Verificação de consistência
N = len(array_criterio55)
lamb = np.sum(array_criterio55, axis=1)
result = DadosSaaty(lamb, N)
# Exibindo o resultado na tela
st.write("Resultado da Verificação de Consistência:")
st.markdown(result)

# Realizando o cálculo VV se os dados são consistentes
if "Consistente" in result:
    l, v = VV(array_criterio55)
    st.write("Autovalor (l):", l)
    #st.write("Autovetor (v):", v)
    st.write("Autovetor (v):", ' '.join(map(str, v)))





#2.13 Critério 06 Treinamento
st.subheader("1.55 Critério 06 Treinamento - Decisor Supervisor")
st.write("Lendo os dados do decisor")
sheetNr = 13
print(desafioLabels[sheetNr])
desafioData = ReadSheetByNr(desafioFile, sheetNr);
desafioData


st.write("1.56 Normalizando o critério Treinamento")
NormalizandoTreinamento = NormalizingCritera(desafioData);
desafioNormalAll.append(NormalizandoTreinamento)
NormalizandoTreinamento


st.write("1.57 Teste de consistência do critério Treinamento")
ajustetabelaTreinamento = NormalizandoTreinamento.copy()
del ajustetabelaTreinamento['Csoma']
del ajustetabelaTreinamento['MatrizdePeso']
ajustetabelaTreinamento


st.write("Transformando para array")
array_criterio66 = ajustetabelaTreinamento.to_numpy()
# Verificação de consistência
N = len(array_criterio66)
lamb = np.sum(array_criterio66, axis=1)
result = DadosSaaty(lamb, N)
# Exibindo o resultado na tela
st.write("Resultado da Verificação de Consistência:")
st.markdown(result)

# Realizando o cálculo VV se os dados são consistentes
if "Consistente" in result:
    l, v = VV(array_criterio66)
    st.write("Autovalor (l):", l)
    #st.write("Autovetor (v):", v)
    st.write("Autovetor (v):", ' '.join(map(str, v)))



st.subheader("1.58 Finalizando Matriz de pesos locais - Priorização das alternativas - Decisor Supervisor")
st.write("2.14.1 PARA ENVIAR AO MOORA DADOS SUPERVISOR")
#25

# Criando Matriz de Priorização das alternativas
matrizData = pd.DataFrame(desafioNormalAll[0]['MatrizdePeso'])
criteriosList = desafioNormalAll[0].index.tolist();
alternativasList = desafioNormalAll[1].index.tolist();
# print(criteriosList)
# print(alternativasList)

for x in alternativasList:
  auxList = [];
  for x2 in criteriosList:
    i = criteriosList.index(x2) + 1
    auxList.append(desafioNormalAll[i]['MatrizdePeso'][x])
  matrizData[x] = auxList
#matrizData

#armazenando em um DataFrame
MatrizDePesoSupervisorParaAHP = matrizData.transpose()
# Exibindo o DataFrame resultante

MatrizDePesoSupervisorParaAHP



#26

somaData = list_of_zeros = [0] * len(alternativasList)

matrizPesoXAlt = matrizData.to_numpy()
i = 0
for x in matrizPesoXAlt:
    p = matrizPesoXAlt[i][0]
    j = 0
    for x2 in x:
        if j > 0:
            pa = p * matrizPesoXAlt[i][j]
            matrizPesoXAlt[i][j] = pa
            somaData[j - 1] += matrizPesoXAlt[i][j]
        j = j + 1

    i = i + 1
matrizPesoXAlt

somaTable = pd.DataFrame([somaData], index=['SOMA'], columns=alternativasList)
somaTable



st.subheader("1.59 Resultado RankingDecisor_02_de_04_Gerado_No_AHP - Supervisor")
#28
RankingDecisor2 = pd.DataFrame(somaData, index=alternativasList, columns=['RankinDecisor_02_de_04_Gerado_No_AHP'])
RankingDecisor2.sort_values(by=['RankinDecisor_02_de_04_Gerado_No_AHP'],ascending=False)

# Exibir DataFrame ordenado
st.write(RankingDecisor2)



#............................................................................................
with st.container():
  st.write("---")



#29
st.subheader("1.60 Gerando a Matriz de comparação dos 5 critérios - Decisor 3 Técnico 01:")
sheetNr = 14
print(desafioLabels[sheetNr])

# Busca dados da planilha
desafioData = ReadSheetByNr(desafioFile, sheetNr);
desafioData



#2.4
st.subheader("1.61 Normalizando os valores dos critérios - Decisor 3 Técnico 01")
# Normaliza dados
normalizandocriterio = NormalizingConsistency(desafioData);
normalizandocriterio


#09
st.subheader("1.62 Consistencia (01) dos dados de critério vs objetivo (LOCAL) onde é comparado os 6 critérios par a par - Decisor Gerente")
Consistencia1 = normalizandocriterio.to_numpy()
Consistencia1



#10   NÃO ESTA FUNCIONANDO   NÃO ESTA FUNCIONANDO
st.subheader("Obtém o autovetor e autovalor e Calcula a consistência - Decisor 3 Técnico 01 ")
l, v = VV(Consistencia1)

#print('Autovalor: %.2f' %l)
#print('Autovetor: ', np.round(v, 2))

DadosSaaty(l, Consistencia1.shape[0])




#11
st.subheader("1.63 Vetor de peso - Decisor 3 Técnico 01")

desafioNormal = NormalizingCritera(desafioData);
desafioNormalAll.append(desafioNormal)
desafioNormal


#12
st.subheader("1.64 Gráfico matriz de peso - Grafico 3 Técnico 01")

desafioNormal[desafioSeets[sheetNr]] = desafioNormal.index
plt.figure(figsize=(22,2))
plt.title("Matriz de peso", fontsize=20)

ax = sns.barplot(x=desafioSeets[sheetNr], y='MatrizdePeso', data=desafioNormal)

# Aqui vem a parte para incluir os rótulos:
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x() + p.get_width() / 2, height + 0, '{:1.2f}'.format((height)), ha='center', fontsize=12)

# Exibe o gráfico usando st.pyplot()
st.pyplot(plt)

#13
st.subheader("1.65 Critério 01 Falhas - Decisor 3 Técnico 01")
st.write("Lendo os dados do decisor")

sheetNr = 15
print(desafioLabels[sheetNr])

# Busca dados da planilha
desafioData = ReadSheetByNr(desafioFile, sheetNr);
desafioData

#11
st.subheader(" 1.66 Normalizando o criterio Falhas - Decisor 3 Técnico 01")

# Normaliza dados
desafioNormal = NormalizingCritera(desafioData);
desafioNormalAll.append(desafioNormal)
desafioNormal


st.subheader("1.67 Teste de consistência do critério 01 Falhas - Decisor 3 Técnico 01")
st.write("Recebendo a matriz do criterio normalizada")
#Retira-se a Soma e  matriz de peso. Se não tirar não funciona.
desafioNormal2 = desafioNormal.copy()
del desafioNormal2['Csoma']
del desafioNormal2['MatrizdePeso']
desafioNormal2


st.write("1.68 Transformando para array")
#00
#teste de consistencia recebe o nome da matriz ja normalizada para teste Assim....  ""  Consistencia00 = nometabela.to_numpy()
Consistencia2 = desafioNormal2.to_numpy()
Consistencia2

st.write("1.69 Resultado consistencia critério 01 - falhas NÃO ESTA FUNCIONANDO")
l, v = VV(Consistencia2)

print('Autovalor: %.2f' %l)
print('Autovetor: ', np.round(v, 2))

DadosSaaty(l, Consistencia2.shape[0])


#2.9
st.subheader("1.70 Critério 02 Segurança - Decisor 3 Técnico 01")
st.write("Lendo os dados do decisor")

# Busca dados da planilha
DadosCriterioSeguranca = ReadSheetByNr(desafioFile, sheetNr);
DadosCriterioSeguranca


# Normaliza dados
st.write("1.71 Normalizando o criterio seguranca - Decisor 3 Técnico 01")
NormalizandoSeguranca = NormalizingCritera(DadosCriterioSeguranca);
desafioNormalAll.append(NormalizandoSeguranca)
NormalizandoSeguranca

st.write("1.72 Recebendo a matriz do criterio segurança normalizada - Decisor 3 Técnico 01")
#Retira-se a Soma e  mtriz de peso. Se não tirar não funciona.
ajustetabelaseguranca = NormalizandoSeguranca.copy()
del ajustetabelaseguranca['Csoma']
del ajustetabelaseguranca['MatrizdePeso']
ajustetabelaseguranca

st.write("Transformando para array")
#00
#teste de consistencia recebe o nome da matriz ja normalizada para teste Assim....  ""  Consistencia00 = nometabela.to_numpy()
ConsistenciaSeguranca = ajustetabelaseguranca.to_numpy()
ConsistenciaSeguranca


st.write("1.73 Resultado consistencia critério 02 segurança - Decisor 3 Técnico 01")

l, v = VV(ConsistenciaSeguranca)

print('Autovalor: %.2f' %l)
print('Autovetor: ', np.round(v, 2))

DadosSaaty(l, ConsistenciaSeguranca.shape[0])


#2.10
st.subheader("1.74 Critério 03 OEE - Decisor Supervisor")
st.write("Lendo os dados do decisor")
sheetNr = 9
print(desafioLabels[sheetNr])

# Busca dados da planinha
desafioData = ReadSheetByNr(desafioFile, sheetNr);
desafioData


st.write("1.75 Normalizando o criterio OEE")
# Normaliza dados
NormalizandoOEE = NormalizingCritera(desafioData);
desafioNormalAll.append(NormalizandoOEE)
NormalizandoOEE

st.write("1.76 Teste de consistência do critério OEE")
#Retira-se a Soma e  mtriz de peso. Se não tirar não funciona.
ajustetabelaOEE = NormalizandoSeguranca.copy()
del ajustetabelaOEE['Csoma']
del ajustetabelaOEE['MatrizdePeso']
ajustetabelaOEE

st.write("Transformando para array")
#00
#teste de consistencia recebe o nome da matriz ja normalizada para teste Assim....  ""  Consistencia00 = nometabela.to_numpy()
ConsistenciaOEE = ajustetabelaOEE.to_numpy()
ConsistenciaOEE

st.write("1.77 TResultado consistencia critério 03 OEE ")
#00
'''
Obtém o autovetor e autovalor
Calcula a consistência
'''
l, v = VV(ConsistenciaOEE)

print('Autovalor: %.2f' %l)
print('Autovetor: ', np.round(v, 2))

DadosSaaty(l, ConsistenciaOEE.shape[0])



#2.11
st.subheader("1.78 Critério 04 Custo - Decisor 3 Técnico 01")
st.write("Lendo os dados do decisor")

#19
sheetNr = 10
print(desafioLabels[sheetNr])
desafioData = ReadSheetByNr(desafioFile, sheetNr);
desafioData

st.write("1.79 Normalizando o critério CUSTO")
#20
NormalizandoCusto = NormalizingCritera(desafioData);
desafioNormalAll.append(NormalizandoCusto)
NormalizandoCusto

st.write(" 1.80 Teste de consistência do critério Custo")
#Retira-se a Soma e  mtriz de peso. Se não tirar não funciona.
ajustetabelaCusto = NormalizandoSeguranca.copy()
del ajustetabelaCusto['Csoma']
del ajustetabelaCusto['MatrizdePeso']
ajustetabelaCusto

st.write("Transformando para array")
ConsistenciaCusto = ajustetabelaCusto.to_numpy()
print(ConsistenciaCusto)

st.write("1.81 Resultado consistencia critério 04 Custo Não esta funcionando")
l, v = VV(ConsistenciaCusto)
print('Autovalor: %.2f' %l)
print('Autovetor: ', np.round(v, 2))
DadosSaaty(l, ConsistenciaCusto.shape[0])




#2.12 Critério 05 Preventiva
st.subheader("1.82 Critério 05 Preventiva - Decisor 3 Técnico 01")
st.write("Lendo os dados do decisor")
#22
sheetNr = 12
print(desafioLabels[sheetNr])
desafioData = ReadSheetByNr(desafioFile, sheetNr);
desafioData

st.write("Normalizando o criterio Preventiva")
NormalizandoPreventiva = NormalizingCritera(desafioData);
desafioNormalAll.append(NormalizandoPreventiva)
NormalizandoPreventiva

st.write(" 1.83 Teste de consistência do critério Preventiva Supervisor")
st.write("Recebendo a matriz do criterio normalizada")
#Retira-se a Soma e  mtriz de peso. Se não tirar não funciona.
ajustetabelaPreventiva = NormalizandoPreventiva.copy()
del ajustetabelaPreventiva['Csoma']
del ajustetabelaPreventiva['MatrizdePeso']
ajustetabelaPreventiva

st.write("Transformando para array")
#00
#teste de consistencia recebe o nome da matriz ja normalizada para teste Assim....  ""  Consistencia00 = nometabela.to_numpy()
array_criterio55 = ajustetabelaPreventiva.to_numpy()
array_criterio55
# Verificação de consistência
N = len(array_criterio55)
lamb = np.sum(array_criterio55, axis=1)
result = DadosSaaty(lamb, N)
# Exibindo o resultado na tela
st.write("Resultado da Verificação de Consistência:")
st.markdown(result)

# Realizando o cálculo VV se os dados são consistentes
if "Consistente" in result:
    l, v = VV(array_criterio55)
    st.write("Autovalor (l):", l)
    #st.write("Autovetor (v):", v)
    st.write("Autovetor (v):", ' '.join(map(str, v)))




#2.13 Critério 06 Treinamento
st.subheader("1.84 Critério 06 Treinamento - Decisor 3 Técnico 01")
st.write("Lendo os dados do decisor")
sheetNr = 12
print(desafioLabels[sheetNr])
desafioData = ReadSheetByNr(desafioFile, sheetNr);
desafioData


st.write("Normalizando o critério Treinamento")
NormalizandoTreinamento = NormalizingCritera(desafioData);
desafioNormalAll.append(NormalizandoTreinamento)
NormalizandoTreinamento


st.write("1.85 Teste de consistência do critério Treinamento")
ajustetabelaTreinamento = NormalizandoTreinamento.copy()
del ajustetabelaTreinamento['Csoma']
del ajustetabelaTreinamento['MatrizdePeso']
ajustetabelaTreinamento


st.write("Transformando para array")
array_criterio66 = ajustetabelaTreinamento.to_numpy()
st.write(array_criterio66)

# Verificação de consistência
N = len(array_criterio66)
lamb = np.sum(array_criterio66, axis=1)
result = DadosSaaty(lamb, N)
# Exibindo o resultado na tela
st.write("Resultado da Verificação de Consistência:")
st.markdown(result)

# Realizando o cálculo VV se os dados são consistentes
if "Consistente" in result:
    l, v = VV(array_criterio66)
    st.write("Autovalor (l):", l)
    #st.write("Autovetor (v):", v)
    st.write("Autovetor (v):", ' '.join(map(str, v)))



st.subheader(" 1.86 Finalizando Matriz de pesos locais - Priorização das alternativas - 3 Técnico 01")
st.write(" PARA ENVIAR AO MOORA DADOS TÉCNICO 01")
#25

# Criando Matriz de Priorização das alternativas
matrizData = pd.DataFrame(desafioNormalAll[0]['MatrizdePeso'])
criteriosList = desafioNormalAll[0].index.tolist();
alternativasList = desafioNormalAll[1].index.tolist();
# print(criteriosList)
# print(alternativasList)

for x in alternativasList:
  auxList = [];
  for x2 in criteriosList:
    i = criteriosList.index(x2) + 1
    auxList.append(desafioNormalAll[i]['MatrizdePeso'][x])
  matrizData[x] = auxList
#matrizData

#armazenando em um DataFrame
MatrizDePesoTec1ParaAHP = matrizData.transpose()
# Exibindo o DataFrame resultante

MatrizDePesoTec1ParaAHP



#26

somaData = list_of_zeros = [0] * len(alternativasList)

matrizPesoXAlt = matrizData.to_numpy()
i = 0
for x in matrizPesoXAlt:
    p = matrizPesoXAlt[i][0]
    j = 0
    for x2 in x:
        if j > 0:
            pa = p * matrizPesoXAlt[i][j]
            matrizPesoXAlt[i][j] = pa
            somaData[j - 1] += matrizPesoXAlt[i][j]
        j = j + 1

    i = i + 1
matrizPesoXAlt

somaTable = pd.DataFrame([somaData], index=['SOMA'], columns=alternativasList)
somaTable


st.subheader("1.87 Resultado RankingDecisor_03_de_04_Gerado_No_AHP - Téc 01")
#28
RankingDecisor3 = pd.DataFrame(somaData, index=alternativasList, columns=['RankinDecisor_03_de_04_Gerado_No_AHP'])
RankingDecisor3.sort_values(by=['RankinDecisor_03_de_04_Gerado_No_AHP'],ascending=False)

# Exibir DataFrame ordenado
st.write(RankingDecisor3)




#29
st.subheader("1.88 Gerando a Matriz de comparação dos 5 critérios - Decisor 3 Técnico 02:")
sheetNr = 21
print(desafioLabels[sheetNr])

# Busca dados da planilha
desafioData = ReadSheetByNr(desafioFile, sheetNr);
desafioData



#2.4
st.subheader("1.89 Normalizando os valores dos critérios - Decisor 3 Técnico 02")
# Normaliza dados
normalizandocriterio = NormalizingConsistency(desafioData);
normalizandocriterio


#09
st.subheader(" 1.9 Consistencia (01) dos dados de critério vs objetivo (LOCAL) onde é comparado os 6 critérios par a par - Decisor Gerente")
Consistencia1 = normalizandocriterio.to_numpy()
Consistencia1



st.subheader("1.91 btém o autovetor e autovalor e Calcula a consistência - Decisor 3 Técnico 01 ")
l, v = VV(Consistencia1)

#print('Autovalor: %.2f' %l)
#print('Autovetor: ', np.round(v, 2))

DadosSaaty(l, Consistencia1.shape[0])




#11
st.subheader("1.92 Vetor de peso - Decisor 3 Técnico 02")

desafioNormal = NormalizingCritera(desafioData);
desafioNormalAll.append(desafioNormal)
desafioNormal


#12
st.subheader("1.93 Gráfico matriz de peso - Grafico 3 Técnico 02")

desafioNormal[desafioSeets[sheetNr]] = desafioNormal.index
plt.figure(figsize=(22,2))
plt.title("Matriz de peso", fontsize=20)

ax = sns.barplot(x=desafioSeets[sheetNr], y='MatrizdePeso', data=desafioNormal)

# Aqui vem a parte para incluir os rótulos:
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x() + p.get_width() / 2, height + 0, '{:1.2f}'.format((height)), ha='center', fontsize=12)

# Exibe o gráfico usando st.pyplot()
st.pyplot(plt)

#13
st.subheader("Critério 01 Falhas - Decisor 3 Técnico 02")
st.write("Lendo os dados do decisor")

sheetNr = 22
print(desafioLabels[sheetNr])

# Busca dados da planilha
desafioData = ReadSheetByNr(desafioFile, sheetNr);
desafioData

#11
st.subheader(" 1.94 Normalizando o criterio Falhas - Decisor 3 Técnico 02")

# Normaliza dados
desafioNormal = NormalizingCritera(desafioData);
desafioNormalAll.append(desafioNormal)
desafioNormal


st.subheader("1.95 Teste de consistência do critério 01 Falhas - Decisor 3 Técnico 02")
st.write("Recebendo a matriz do criterio normalizada")
#Retira-se a Soma e  matriz de peso. Se não tirar não funciona.
desafioNormal2 = desafioNormal.copy()
del desafioNormal2['Csoma']
del desafioNormal2['MatrizdePeso']
desafioNormal2


st.write("Transformando para array")
#00
#teste de consistencia recebe o nome da matriz ja normalizada para teste Assim....  ""  Consistencia00 = nometabela.to_numpy()
Consistencia2 = desafioNormal2.to_numpy()
Consistencia2

st.write("1.96 Resultado consistencia critério 01 - falhas NÃO ESTA FUNCIONANDO")
l, v = VV(Consistencia2)

print('Autovalor: %.2f' %l)
print('Autovetor: ', np.round(v, 2))

DadosSaaty(l, Consistencia2.shape[0])


#2.9
st.subheader("1.97 Critério 02 Segurança - Decisor 3 Técnico 02")
st.write("Lendo os dados do decisor")

# Busca dados da planilha
DadosCriterioSeguranca = ReadSheetByNr(desafioFile, sheetNr);
DadosCriterioSeguranca


# Normaliza dados
st.write("Normalizando o criterio seguranca - Decisor 3 Técnico 02")
NormalizandoSeguranca = NormalizingCritera(DadosCriterioSeguranca);
desafioNormalAll.append(NormalizandoSeguranca)
NormalizandoSeguranca

st.write("1.98 Recebendo a matriz do criterio segurança normalizada - Decisor 3 Técnico 01")
#Retira-se a Soma e  mtriz de peso. Se não tirar não funciona.
ajustetabelaseguranca = NormalizandoSeguranca.copy()
del ajustetabelaseguranca['Csoma']
del ajustetabelaseguranca['MatrizdePeso']
ajustetabelaseguranca

st.write("Transformando para array")
#00
#teste de consistencia recebe o nome da matriz ja normalizada para teste Assim....  ""  Consistencia00 = nometabela.to_numpy()
ConsistenciaSeguranca = ajustetabelaseguranca.to_numpy()
ConsistenciaSeguranca


st.write("1.99 Resultado consistencia critério 02 segurança - Decisor 3 Técnico 01")

l, v = VV(ConsistenciaSeguranca)

print('Autovalor: %.2f' %l)
print('Autovetor: ', np.round(v, 2))

DadosSaaty(l, ConsistenciaSeguranca.shape[0])


#2.10
st.subheader("1.100 Critério 03 OEE - Decisor tec2")
st.write("Lendo os dados do decisor")
sheetNr = 24
print(desafioLabels[sheetNr])

# Busca dados da planinha
desafioData = ReadSheetByNr(desafioFile, sheetNr);
desafioData


st.write("1.101 Normalizando o criterio OEE")
# Normaliza dados
NormalizandoOEE = NormalizingCritera(desafioData);
desafioNormalAll.append(NormalizandoOEE)
NormalizandoOEE

st.write("1.102 Teste de consistência do critério OEE")
#Retira-se a Soma e  mtriz de peso. Se não tirar não funciona.
ajustetabelaOEE = NormalizandoSeguranca.copy()
del ajustetabelaOEE['Csoma']
del ajustetabelaOEE['MatrizdePeso']
ajustetabelaOEE

st.write("Transformando para array")
#00
#teste de consistencia recebe o nome da matriz ja normalizada para teste Assim....  ""  Consistencia00 = nometabela.to_numpy()
ConsistenciaOEE = ajustetabelaOEE.to_numpy()
ConsistenciaOEE

st.write("1.103 TResultado consistencia critério 03 OEE NAO FUNCIONA")
#00
'''
Obtém o autovetor e autovalor
Calcula a consistência
'''
l, v = VV(ConsistenciaOEE)

print('Autovalor: %.2f' %l)
print('Autovetor: ', np.round(v, 2))

DadosSaaty(l, ConsistenciaOEE.shape[0])



#2.11
st.subheader("1.104 Critério 04 Custo - Decisor 3 Técnico 02")
st.write("Lendo os dados do decisor")

#19
sheetNr = 25
print(desafioLabels[sheetNr])
desafioData = ReadSheetByNr(desafioFile, sheetNr);
desafioData

st.write("1.105 Normalizando o critério CUSTO")
#20
NormalizandoCusto = NormalizingCritera(desafioData);
desafioNormalAll.append(NormalizandoCusto)
NormalizandoCusto

st.write("1.106 Teste de consistência do critério Custo")
#Retira-se a Soma e  mtriz de peso. Se não tirar não funciona.
ajustetabelaCusto = NormalizandoSeguranca.copy()
del ajustetabelaCusto['Csoma']
del ajustetabelaCusto['MatrizdePeso']
ajustetabelaCusto

st.write("Transformando para array")
ConsistenciaCusto = ajustetabelaCusto.to_numpy()
print(ConsistenciaCusto)

st.write("1.107 Resultado consistencia critério 04 Custo Não esta funcionando")
l, v = VV(ConsistenciaCusto)
print('Autovalor: %.2f' %l)
print('Autovetor: ', np.round(v, 2))
DadosSaaty(l, ConsistenciaCusto.shape[0])




#2.12 Critério 05 Preventiva
st.subheader("1.108 Critério 05 Preventiva - Decisor 3 Técnico 02")
st.write("Lendo os dados do decisor")
#22
sheetNr = 26
print(desafioLabels[sheetNr])
desafioData = ReadSheetByNr(desafioFile, sheetNr);
desafioData

st.write("1.109 Normalizando o criterio Preventiva")
NormalizandoPreventiva = NormalizingCritera(desafioData);
desafioNormalAll.append(NormalizandoPreventiva)
NormalizandoPreventiva

st.write("1.110 Teste de consistência do critério Preventiva Supervisor")
st.write("Recebendo a matriz do criterio normalizada")
#Retira-se a Soma e  mtriz de peso. Se não tirar não funciona.
ajustetabelaPreventiva = NormalizandoPreventiva.copy()
del ajustetabelaPreventiva['Csoma']
del ajustetabelaPreventiva['MatrizdePeso']
ajustetabelaPreventiva

st.write("1.111Transformando para array")
#00
#teste de consistencia recebe o nome da matriz ja normalizada para teste Assim....  ""  Consistencia00 = nometabela.to_numpy()
ConsistenciaPreventiva = ajustetabelaPreventiva.to_numpy()
print(ConsistenciaPreventiva )

st.write("1.112 resultado consistencia Noa esta funcioando")
l, v = VV(ConsistenciaPreventiva )
print('Autovalor: %.2f' %l)
print('Autovetor: ', np.round(v, 2))
DadosSaaty(l, ConsistenciaPreventiva .shape[0])



#2.13 Critério 06 Treinamento
st.subheader("1.113 Critério 06 Treinamento - Decisor 3 Técnico 02")
st.write("Lendo os dados do decisor")
sheetNr = 27
print(desafioLabels[sheetNr])
desafioData = ReadSheetByNr(desafioFile, sheetNr);
desafioData


st.write("1.114 Normalizando o critério Treinamento")
NormalizandoTreinamento = NormalizingCritera(desafioData);
desafioNormalAll.append(NormalizandoTreinamento)
NormalizandoTreinamento


st.write("1.115 Teste de consistência do critério Treinamento")
ajustetabelaTreinamento = NormalizandoTreinamento.copy()
del ajustetabelaTreinamento['Csoma']
del ajustetabelaTreinamento['MatrizdePeso']
ajustetabelaTreinamento


st.write("1.115 Transformando para array")
array_criterio_Treinamento_tec1 = ajustetabelaTreinamento.to_numpy()
st.write(array_criterio_Treinamento_tec1)

# Verificação de consistência
N = len(array_criterio_Treinamento_tec1)
lamb = np.sum(array_criterio_Treinamento_tec1, axis=1)
result = DadosSaaty(lamb, N)
# Exibindo o resultado na tela
st.write("Resultado da Verificação de Consistência:")
st.markdown(result)

# Realizando o cálculo VV se os dados são consistentes
if "Consistente" in result:
    l, v = VV(array_criterio_Treinamento_tec1)
    st.write("Autovalor (l):", l)
    #st.write("Autovetor (v):", v)
    st.write("Autovetor (v):", ' '.join(map(str, v)))





st.subheader(" 1.116 Finalizando Matriz de pesos locais - Priorização das alternativas - 3 Técnico 02")
st.write("2.14.1 PARA ENVIAR AO MOORA DADOS TEC02")
#25

# Criando Matriz de Priorização das alternativas
matrizData = pd.DataFrame(desafioNormalAll[0]['MatrizdePeso'])
criteriosList = desafioNormalAll[0].index.tolist();
alternativasList = desafioNormalAll[1].index.tolist();
# print(criteriosList)
# print(alternativasList)

for x in alternativasList:
  auxList = [];
  for x2 in criteriosList:
    i = criteriosList.index(x2) + 1
    auxList.append(desafioNormalAll[i]['MatrizdePeso'][x])
  matrizData[x] = auxList
#matrizData

#armazenando em um DataFrame
MatrizDePesoTec2ParaAHP = matrizData.transpose()
# Exibindo o DataFrame resultante

MatrizDePesoTec2ParaAHP



#26
st.subheader(" 1.117 AHP ADITIVO Tec2")

somaData = list_of_zeros = [0] * len(alternativasList)

matrizPesoXAlt = matrizData.to_numpy()
i = 0
for x in matrizPesoXAlt:
    p = matrizPesoXAlt[i][0]
    j = 0
    for x2 in x:
        if j > 0:
            pa = p * matrizPesoXAlt[i][j]
            matrizPesoXAlt[i][j] = pa
            somaData[j - 1] += matrizPesoXAlt[i][j]
        j = j + 1

    i = i + 1
matrizPesoXAlt

somaTable = pd.DataFrame([somaData], index=['SOMA'], columns=alternativasList)
somaTable



st.subheader("1.118 Resultado RankingDecisor_04_de_04_Gerado_No_AHP - Téc 02")
#28
RankingDecisor4 = pd.DataFrame(somaData, index=alternativasList, columns=['RankinDecisor_04_de_04_Gerado_No_AHP'])
RankingDecisor4.sort_values(by=['RankinDecisor_04_de_04_Gerado_No_AHP'],ascending=False)

# Exibir DataFrame ordenado
st.write(RankingDecisor4)



dataframes = [RankingDecisor1, RankingDecisor2, RankingDecisor3, RankingDecisor4]

# Concatenando os DataFrames ao longo das colunas
tabela_combinada = pd.concat(dataframes, axis=1)

# Calculando a média aritmética para cada linha
media_aritmetica = tabela_combinada.mean(axis=1)
media_aritmetica = pd.DataFrame(media_aritmetica, columns=['MediaAritmetica'])

# Adicionando a coluna de média aritmética à tabela combinada
tabela_combinada = pd.concat([tabela_combinada, media_aritmetica], axis=1)
tabela_combinada = tabela_combinada.sort_values(by=['MediaAritmetica'], ascending=False)

# Exibindo a tabela combinada
tabela_combinada

st.subheader('1.119 Ranking final AHP')

# Filtrar apenas as colunas "MediaAritmetica"

# Mantenha a primeira e a última coluna
Ranking_final_AHP = tabela_combinada.copy

colunas_desejadas = [tabela_combinada.columns[-1]]
Ranking_final_AHP = tabela_combinada[colunas_desejadas]

# Exiba o DataFrame resultante
#st.write(Ranking_final_AHP)

# Dê um nome à coluna de índice
Ranking_final_AHP.index.name = 'Alternativas'

# Exiba o DataFrame resultante
st.write(Ranking_final_AHP)




################
with st.container():
    st.markdown("<h2 style='text-align: center; background-color: #6495ED;'>02 - Método MOORA</h2>", unsafe_allow_html=True)
    st.subheader('Brauers e Zavadskas')

dataframes = [MatrizDePesoGerenteParaAHP, MatrizDePesoSupervisorParaAHP, MatrizDePesoTec1ParaAHP, MatrizDePesoTec2ParaAHP]

# Verificando se os DataFrames têm a mesma estrutura (mesmas colunas)
colunas_esperadas = dataframes[0].columns.tolist()
for df in dataframes[1:]:
    if df.columns.tolist() != colunas_esperadas:
        raise ValueError("Os DataFrames não têm a mesma estrutura (colunas).")

# Criando um DataFrame vazio para armazenar a média
tabela_media = pd.DataFrame(columns=colunas_esperadas)

# Calculando a média para cada coluna, excluindo a linha "MatrizdePeso"
for coluna in colunas_esperadas:
    valores_coluna = [df[coluna] for df in dataframes if coluna != "MatrizdePeso"]
    tabela_media[coluna] = pd.concat(valores_coluna, axis=0).groupby(level=0).mean()


# Exibindo o DataFrame com a média
#print("DataFrame com Média:")
#tabela_media


st.subheader('2.1 - Critérios de Maximização ou Minimização')
st.write("Informe ao sistema se o objetivo deve ser Minimizado ou Maximizado")

# Criando uma lista para armazenar as opções de maximização/minimização
opcoes = {}

# Exibindo a interface para cada coluna
for coluna in tabela_media.columns:
    # Adicionando uma opção para o usuário informar se é Maximizar ou Minimizar
    objetivo = st.radio(f"Selecione o objetivo para a coluna {coluna}:", ["Maximizar", "Minimizar"])
    opcoes[coluna] = objetivo

# Gerando um novo DataFrame com os nomes modificados
novo_dataframe = tabela_media.copy()

for coluna, objetivo in opcoes.items():
    novo_nome = f"{coluna}_{objetivo}"
    novo_dataframe.rename(columns={coluna: novo_nome}, inplace=True)

# Exibindo o novo DataFrame
st.write("Novo DataFrame com a escolha do usuário:")
st.write(novo_dataframe)



st.write("2.2 Guardando somente a linha de peso para usar depois")

# Criando uma cópia do DataFrame contendo apenas a linha "MatrizdePeso"
dados_peso_do_ahp = novo_dataframe.loc[['MatrizdePeso']].copy()

# Exibindo o novo DataFrame
st.write(dados_peso_do_ahp)



#st.write("Ficando com o data frame sem o peso")
# Criando uma cópia do DataFrame
matriz_moora = novo_dataframe.copy()

# Excluindo a linha "MatrizdePeso"
matriz_moora = matriz_moora.drop(index='MatrizdePeso')

# Exibindo o DataFrame atualizado
st.write("2.3 Novo DataFrame sem a Linha MatrizdePeso")
st.write(matriz_moora)

# Criando uma cópia do DataFrame para usar depois
matriz_Tchebycheff = matriz_moora.copy()



st.subheader('2.4 Normalizando')
st.write("Elevar os indicadores em análise ao quadrado")

normalizando = matriz_moora.pow(2).round(6)
# Exibindo o novo DataFrame resultante
st.write(normalizando)



st.write("2.5 Obtendo a soma de todos os critérios")
decisaoSumDf = normalizando.copy()
decisaoSumDf.loc['soma'] = decisaoSumDf.sum()
decisaoSumDf



st.write("2.6 Encontrando a raiz da soma ")

# Adicione a linha 'raiz_da_soma' ao final de cada coluna
decisaoSumDf.loc['raiz_da_soma'] = decisaoSumDf.sum()
decisaoSumDf

st.write("2.7 Dividindo cada valor pela raiz quadrada de cada critério")

# Iterando sobre as colunas e normalizando os valores
for coluna in decisaoSumDf.columns:
    raiz_da_soma = decisaoSumDf.at['raiz_da_soma', coluna]
    decisaoSumDf[coluna] = decisaoSumDf[coluna] / raiz_da_soma

# Exibindo o DataFrame após a normalização

st.write(decisaoSumDf)


st.subheader('2.8 Relacionando aos pesos')
st.write("Excluindo as linhas de soma e raiz da soma")

# Criando uma cópia do DataFrame
matriz_nova = decisaoSumDf.copy()

# Excluindo a linha "soma"
matriz_nova = matriz_nova.drop(index='soma')
matriz_nova = matriz_nova.drop(index='raiz_da_soma')
# Exibindo o DataFrame atualizado
st.write(matriz_nova)


st.write("Trazendo os pesos do AHP")
st.write(dados_peso_do_ahp)
primeira_coluna = dados_peso_do_ahp.columns[0]
st.write(f"O nome da primeira coluna é: {primeira_coluna}")



# Inicializa a variável global resultado
resultado = None

def main():
    global resultado  # Indica que estamos referenciando a variável global, não criando uma nova local

    # Simulando DataFrames (substitua isso pelos seus DataFrames reais)
    matriz_nova2 = pd.DataFrame(matriz_nova)
    dados_peso_do_ahp2 = pd.DataFrame(dados_peso_do_ahp)

    # Unindo os DataFrames pela coluna 'Alternativa'
    resultado = pd.concat([matriz_nova2, dados_peso_do_ahp2], ignore_index=False)
    #resultado = pd.merge(matriz_nova2, dados_peso_do_ahp2, on='', how='outer')

    # Exibindo o DataFrame resultante
    st.write("DataFrame Resultante:")
    st.write(resultado, width=800, height=400)

    resultado.reset_index(inplace=True)
    return resultado.copy()

# Chama a função principal
if __name__ == "__main__":
    main()

# Agora, você pode acessar a variável global 'resultado' fora da função main
st.write("Acesso a 'resultado' fora da função main:")
st.write(resultado)








st.subheader("2.9 Relacionando aos pesos ")
st.write("do data frame anterior cada valor foi multiplicado pela MatrizdePeso:")

# Obtendo os pesos dos critérios da última linha
pesos = resultado.iloc[-1, :]


# Multiplicando os valores das alternativas pelos pesos dos critérios
resultado.iloc[:-1, 1:] = resultado.iloc[:-1, 1:].multiply(pesos[1:])

# Excluindo a linha "MatrizdePeso"
resultado = resultado[resultado['index'] != 'MatrizdePeso']

# Resetando o índice para trazer a coluna 'Alternativa' de volta
resultado.reset_index(drop=True, inplace=True)
resultado = resultado.dropna()

# Exibindo o DataFrame resultante)
st.dataframe(resultado)




#st.subheader("2.10 Otimização do Modelo Moora")


# Carregue o DataFrame existente
otimizacao = pd.DataFrame(resultado)

# Listas para armazenar as otimizações otimizadas
alternativas = []
resultados_otimizados = []
info_crit = []

# Itera sobre as linhas do DataFrame 'otimizacao' usando iterrows()
for index, row in otimizacao.iterrows():
    # Adiciona a alternativa à lista de otimizações otimizadas
    alternativas.append(row['index'])

    # Inicializa a soma para critérios de maximização
    soma_max = 0

    # Itera sobre as colunas do DataFrame 'otimizacao'
    for coluna in otimizacao.columns:
        # Verifica se a coluna contém "Minimizar"
        if "minimizar" in coluna.lower():
            soma_max -= row[coluna]  # Corrigindo o sinal para minimização
            info_crit.append((coluna, row['index'], "Minimizar"))
        # Verifica se a coluna contém "Maximizar"
        elif "maximizar" in coluna.lower():
            soma_max += row[coluna]
            info_crit.append((coluna, row['index'], "Maximizar"))

    # Adiciona a soma para critérios de maximização à lista de resultados otimizados
    resultados_otimizados.append(soma_max)

# Cria um DataFrame com os resultados otimizados
otimizado_df = pd.DataFrame({"Alternativa": alternativas, "Resultado Otimizado": resultados_otimizados})

# Exibe o DataFrame resultante
st.subheader("2.10 Resultado Otimizado:")
st.write(otimizado_df, width=800, height=400)



st.subheader("2.11 - Ranking Moora")
# Cria um DataFrame para a ordenação
Ranking_Moora = pd.DataFrame(otimizado_df, columns=['Alternativa', 'Resultado Otimizado'])
Ranking_Moora = Ranking_Moora.sort_values(by=['Resultado Otimizado'], ascending=False)

# Exibe o DataFrame ordenado
st.write(Ranking_Moora, width=800, height=400)




################
with st.container():
    st.markdown("<h2 style='text-align: center; background-color: #6495ED;'>03 Método Tchebycheff</h2>", unsafe_allow_html=True)
    st.subheader('3.1 Iniciando com a matriz original do AHP.')
st.write(matriz_Tchebycheff)


#st.write("..............................TESTE.................................")
# Verificar se é um DataFrame
#if isinstance(matriz_Tchebycheff, pd.DataFrame):
#    st.write("É um DataFrame")
#else:
#    st.write("Não é um DataFrame")

# Verificar se o DataFrame tem colunas preenchidas
#if not matriz_Tchebycheff.empty and not matriz_Tchebycheff.columns.empty:
#    st.write("O DataFrame tem colunas preenchidas")
#else:
#    st.write("O DataFrame está vazio ou sem colunas")
#st.write("..............................TESTE.................................")

st.subheader('3.2 Achando o ponto de referência')
# Função para calcular o ponto de referência com base nos critérios
def calcular_ponto_referencia(df):
    ponto_referencia = []
    for coluna in df.columns:
        if 'Maximizar' in coluna:
            ponto_referencia.append(df[coluna].max())
        elif 'Minimizar' in coluna:
            ponto_referencia.append(df[coluna].min())
    return ponto_referencia

# Função para adicionar a linha de ponto de referência
def adicionar_linha_ponto_referencia(df):
    ponto_referencia = calcular_ponto_referencia(df)
    df.loc['Ponto_Referencia'] = ponto_referencia

# Função principal do Streamlit
def main():
    global matriz_Tchebycheff  # Garante que a variável global seja usada

    # Adicionar a linha de ponto de referência
    adicionar_linha_ponto_referencia(matriz_Tchebycheff)

    # Mostrar DataFrame no Streamlit
    st.dataframe(matriz_Tchebycheff)

# Executar a função principal
if __name__ == '__main__':
    main()

#...............................................................
st.subheader("3.3 . Avaliação final - FALTA CHEGAR O QUE DEVE SER REDUZIDO ")
st.write("Pega-se o valor de cada alternaytiva e diminui pelo valor do ponto de referencia?")
# Reduzir os valores das alternativas pelo valor na linha Ponto_Referencia
matriz_reduzida = matriz_Tchebycheff.iloc[:-1, :] - matriz_Tchebycheff.loc['Ponto_Referencia']

# Adicionar a linha de Ponto_Referencia à matriz reduzida
matriz_reduzida.loc['Ponto_Referencia'] = matriz_Tchebycheff.loc['Ponto_Referencia']

# Função principal do Streamlit
def main():
    global matriz_reduzida  # Garante que a variável global seja usada

    # Excluir a linha Ponto_Referencia do resultado
    matriz_reduzida = matriz_reduzida.drop('Ponto_Referencia')

    # Mostrar DataFrame reduzido no Streamlit
    st.dataframe(matriz_reduzida)

# Executar a função principal
if __name__ == '__main__':
    main()



st.subheader("3.4 Ordena-se as alternativas de acordo com maior distância. Ponto de referencia")


# Reduzir os valores das alternativas pelo valor na linha Ponto_Referencia
matriz_reduzida = matriz_Tchebycheff.iloc[:-1, :] - matriz_Tchebycheff.loc['Ponto_Referencia']

# Encontrar o maior valor em cada alternativa
maiores_valores = matriz_reduzida.max(axis=1)

# Criar DataFrame com os maiores valores
resultados = pd.DataFrame({'Maior_Valor': maiores_valores})

# Função principal do Streamlit
def main():
    global resultados  # Garante que a variável global seja usada

    # Mostrar DataFrame com os maiores valores no Streamlit
    st.dataframe(resultados)

# Executar a função principal
if __name__ == '__main__':
    main()


#...............................................................
st.subheader("3.5 Resultado tchebycheff")
st.write("Ordena-se do menor para o maior")
# Ordenar os resultados do menor para o maior
Ranking_tchebycheff = resultados.sort_values(by='Maior_Valor')
st.dataframe(Ranking_tchebycheff)

# Renomeando o índice para "Alternativas"
Ranking_tchebycheff = Ranking_tchebycheff.rename_axis('Alternativas')

# Exibindo o DataFrame modificado usando Streamlit
st.write(Ranking_tchebycheff)




################
with st.container():
    st.markdown("<h2 style='text-align: center; background-color: #6495ED;'>4 - MULTIMOORA</h2>", unsafe_allow_html=True)
    st.subheader('4.1 Iniciando com a matriz original do AHP.')
    st.write(" MULTIMOORA é a sequência adicional do método MOORA e da forma multiplicativa completa de múltiplos objetivos")
    matriz_multimoora = matriz_Tchebycheff.copy()
st.write(matriz_multimoora)


nomes_colunas = matriz_multimoora.columns.tolist()
# Exibir os nomes das colunas
#st.write("Nomes das Colunas:", nomes_colunas)

#...............................................................
st.subheader("4.2 Dividindo ou multiplicandox")
st.write("Se o critério for de max multiplica pelo ponto de referencia, senão divide")



# Obtendo os nomes das alternativas e critérios
alternativas = matriz_multimoora.index.tolist()
criterios = matriz_multimoora.columns.tolist()

# Obtendo os pontos de referência
ponto_referencia = matriz_multimoora.loc["Ponto_Referencia"]

# Aplicando a lógica MUTIMOORA
for criterio in criterios:
    if "Maximizar" in criterio:
        matriz_multimoora[criterio] *= ponto_referencia[criterio]
    else:
        matriz_multimoora[criterio] /= ponto_referencia[criterio]

# Excluindo a linha "Ponto_Referencia"
matriz_multimoora = matriz_multimoora.drop("Ponto_Referencia")

# Exibindo o DataFrame após a aplicação do método
st.write("DataFrame Após MUTIMOORA:", matriz_multimoora)



#...............................................................
st.subheader("Resultado MULTIMOORA")
st.write("Agregação dos Resultados e  Classificação das Alternativas")



# Obtendo os nomes das alternativas e critérios
alternativas = matriz_multimoora.index.tolist()
criterios = matriz_multimoora.columns.tolist()

# Página Streamlit

# Exibindo o DataFrame original
st.write("DataFrame Original:")
st.write(matriz_multimoora)


st.subheader("4.3 Descobrindo se é de max ou min:")
# Obtendo os nomes das colunas de critérios
colunas_critérios = matriz_multimoora.columns.tolist()

# Criando a lista colMinOrMax automaticamente
colMinOrMax = []

for coluna in colunas_critérios:
    if "Maximizar" in coluna:
        colMinOrMax.append('max')
    elif "Minimizar" in coluna:
        colMinOrMax.append('min')
    else:
        # Caso a coluna não contenha informações sobre maximizar ou minimizar, você pode adicionar lógica adicional ou definir um valor padrão.
        colMinOrMax.append('padrao')

# Exibindo a lista colMinOrMax
st.write("Lista colMinOrMax:", colMinOrMax)




st.write("4.4 Montando as novas colunas:")
# Obtendo os nomes das colunas de critérios
colunas_critérios = matriz_multimoora.columns.tolist()

# Criando a variável vColunas conforme o padrão mencionado
vColunas = []
for i, coluna in enumerate(colunas_critérios):
    vColunas.append(coluna)
    if i > 0:
        vColunas.append(f"{i+1}")

# Exibindo a lista vColunas

#st.write("vColunas:", vColunas)


st.subheader("4.4 Descobrindo nomes das alternativas de critérios:")
# Obtendo os nomes das alternativas de critérios
vIndice = matriz_multimoora.index.tolist()

# Exibindo a lista vIndice
st.write("Lista vIndice:", vIndice)




st.subheader(" 4.5 Implementando a lógica do método MULTIMOORA")
st.write("Recebe a primeira e a segunda coluna original do dataframe e cria as proximas colunas numerando seus títulos - comencando pelo numero 2 - e nas linhas das alternativas recebe os valores das colunas multiplicados")


MultimooraMt = []
MultimooraOrderMt = []
for k, linha in enumerate(matriz_multimoora.values):
    v = 0  # Inicialize v com um valor numérico
    MultimooraMt.append([])
    MultimooraOrderMt.append([0])

    for k2, valor in enumerate(linha):
        MultimooraMt[k].append(valor)

        if k2 > 0:
            if colMinOrMax[k2] == 'max':
                v = v * float(valor)  # Converta para float antes de multiplicar
            else:
                v = v / float(valor)  # Converta para float antes de dividir
            MultimooraMt[k].append(v)
        else:
            v = float(valor)  # Converta para float no início do loop
        MultimooraOrderMt[k][0] = v


MultimooraDf = pd.DataFrame(MultimooraMt, index=vIndice, columns=vColunas)
MultimooraDf


st.subheader("4.6 Resultado MULTIMOORA")

Ranking_Multimoora = pd.DataFrame(MultimooraOrderMt, index=vIndice, columns=['RankingMultiMoora'])

# Ajustando a exibição de casas decimais
pd.set_option('display.float_format', '{:.6f}'.format)

# Arredondando o DataFrame para 6 casas decimais
Ranking_Multimoora = Ranking_Multimoora.round(6)

Ranking_Multimoora = Ranking_Multimoora.sort_values(by=['RankingMultiMoora'], ascending=False)
st.write(Ranking_Multimoora)




################
with st.container():
    st.markdown("<h2 style='text-align: center; background-color: #6495ED;'>5 BORDA", unsafe_allow_html=True)
    st.write(" Nesse método, se houver t alternativas, a primeira colocada recebe t votos e a segunda recebe um voto a menos, e assim por diante.")
    st.subheader('5.1 Recebendo todos os rankings ')
    st.write("Ranking_final_AHP, Ranking_Moora, Ranking_tchebycheff, Ranking_Multimoora")


st.subheader('5.2 AHP')
#st.write(Ranking_final_AHP)
#st.write(" -------AHP Verificar se é DataFrame ou Series")
Ranking_final_AHP = Ranking_final_AHP.rename(columns={'Indice': 'Alternativas'})
Ranking_final_AHP= Ranking_final_AHP.rename(columns={'MediaAritmetica': 'Ranking_final_AHP'})


st.write(Ranking_final_AHP)
if isinstance(Ranking_final_AHP, pd.DataFrame):
    st.write("Ranking_final_AHP, é um DataFrame.")
elif isinstance(Ranking_final_AHP, pd.Series):
    st.write("Ranking_final_AHP, é uma Series.")
else:
    st.write("Não é nem DataFrame nem Series. Verifique o tipo do objeto.")
#st.write(" --------Verificar se 'index' está nas colunas do DataFrame")
tem_coluna_index_ahp = 'index' in Ranking_final_AHP.columns
st.write(f"O DataFrame tem uma coluna chamada 'Indice: {tem_coluna_index_ahp}")






st.subheader('5.3 MOORA')
st.write(" Ranking_Moora Verificar se é DataFrame ou Series")
# Renomeando a coluna
Ranking_Moora= Ranking_Moora.rename(columns={'Resultado Otimizado': 'Ranking_Moora'})
Ranking_Moora= Ranking_Moora.rename(columns={'Alternativa': 'Alternativas'})
st.write(Ranking_Moora)
if isinstance(Ranking_Moora, pd.DataFrame):
    st.write("Ranking_Moora é um DataFrame.")
    # Se for um DataFrame, você pode realizar operações específicas de DataFrame
    # Exemplo: st.dataframe(Ranking_Moora)
elif isinstance(Ranking_Moora, pd.Series):
    st.write("Ranking_Moora é uma Series.")
    # Se for uma Series, você pode realizar operações específicas de Series
    # Exemplo: st.write(Ranking_Moora)
else:
    st.write("Não é nem DataFrame nem Series. Verifique o tipo do objeto.")

#st.write(" --------Verificar se 'index' está nas colunas do DataFrame")
tem_coluna_index_moora = 'index' in Ranking_Moora.columns
st.write(f"O DataFrame tem uma coluna chamada 'index': {tem_coluna_index_moora}")




st.subheader('5.4 tchebychefff')
#st.write(" Ranking_Moora Verificar se é DataFrame ou Series")
#st.write(Ranking_tchebycheff)

# Renomeando a coluna
Ranking_tchebycheff = Ranking_tchebycheff.rename(columns={'Maior_Valor': 'Ranking_tchebycheff'})
# Renomeando o índice para "Alternativas"
Ranking_tchebycheff = Ranking_tchebycheff.rename_axis('Alternativas')
st.write(Ranking_tchebycheff)



st.subheader('5.5 Multimoora')
st.write(" Ranking_Moora Verificar se é DataFrame ou Series")
#st.write(Ranking_Multimoora)
if isinstance(Ranking_Multimoora, pd.DataFrame):
    st.write("Ranking_Multimoora é um DataFrame.")
    # Se for um DataFrame, você pode realizar operações específicas de DataFrame
    # Exemplo: st.dataframe(Ranking_Multimoora)

elif isinstance(Ranking_Multimoora, pd.Series):
    st.write("Ranking_Multimoora é uma Series.")
    # Se for uma Series, você pode realizar operações específicas de Series
    # Exemplo: st.write(Ranking_Multimoora)
else:
    st.write("Não é nem DataFrame nem Series. Verifique o tipo do objeto.")

# Renomeando o índice para "Alternativas"
Ranking_Multimoora = Ranking_Multimoora.rename_axis('Alternativas')

# Exibindo o DataFrame modificado usando Streamlit
st.write(Ranking_Multimoora)
# para obter os nomes das colunas
#nomes_colunas = Ranking_Multimoora.columns
st.write("Nomes das Colunas do Ranking_Multimoora:", nomes_colunas)

# Renomeando o índice para "Alternativas"
Ranking_Multimoora= Ranking_Multimoora.rename_axis('Alternativas')


st.subheader('5.6 Unindo os rankings Ranking_final_AHP, Ranking_tchebycheff, Ranking_Multimoora, Ranking_Moora')
st.markdown("<h2 style='text-align: center; background-color: #6495ED;'>RANQUEAMENTO FINAL</h2>", unsafe_allow_html=True)
# Unindo os DataFrames com base na coluna 'Alternativas'
borda_inicio_df = pd.merge(Ranking_final_AHP, Ranking_tchebycheff, on='Alternativas')
borda_inicio_df = pd.merge(borda_inicio_df, Ranking_Moora, on='Alternativas')
borda_inicio_df = pd.merge(borda_inicio_df, Ranking_Multimoora, on='Alternativas')

# Exibindo o DataFrame resultante
st.table(borda_inicio_df)

# Fazendo o Ranking
#função para Ordenar
def reoder(x, y):
    return y.index(x)+1

col1 = borda_inicio_df['Ranking_final_AHP'].values.tolist()
col1_ordered = borda_inicio_df['Ranking_final_AHP'].sort_values().values.tolist()
borda_inicio_df['ordem1'] = borda_inicio_df['Ranking_final_AHP'].apply(reoder, y=col1_ordered)

col2 = borda_inicio_df['Ranking_Moora'].values.tolist()
col2_ordered = borda_inicio_df['Ranking_Moora'].sort_values().values.tolist()
borda_inicio_df['ordem2'] = borda_inicio_df['Ranking_Moora'].apply(reoder, y=col2_ordered)


col3 = borda_inicio_df['RankingMultiMoora'].values.tolist()
col3_ordered = borda_inicio_df['RankingMultiMoora'].sort_values().values.tolist()
borda_inicio_df['ordem3'] = borda_inicio_df['RankingMultiMoora'].apply(reoder, y=col3_ordered)


col4 = borda_inicio_df['Ranking_tchebycheff'].values.tolist()
col4_ordered = borda_inicio_df['Ranking_tchebycheff'].sort_values().values.tolist()
borda_inicio_df['ordem4'] = borda_inicio_df['Ranking_tchebycheff'].apply(reoder, y=col4_ordered)




# Reordenando as colunas para mover 'ordem1' para a terceira posição
ordem1 = borda_inicio_df.pop('ordem1')  # Remove a coluna 'ordem1'
borda_inicio_df.insert(2, 'ordem1', ordem1)  # Insere 'ordem1' na posição desejada (posição 2 neste caso)

# Reordenando as colunas para mover 'ordem2' para a terceira posição
ordem2 = borda_inicio_df.pop('ordem2')  # Remove a coluna 'ordem2'
borda_inicio_df.insert(4, 'ordem2', ordem2)  # Insere 'ordem1' na posição desejada (posição 4 neste caso)

# Reordenando as colunas para mover 'ordem3' para a terceira posição
ordem3 = borda_inicio_df.pop('ordem3')  # Remove a coluna 'ordem2'
borda_inicio_df.insert(6, 'ordem3', ordem3)  # Insere 'ordem1' na posição desejada (posição 6 neste caso)

st.write(borda_inicio_df)

# Criando a nova coluna "Ranking_Borda" somando as colunas "ordem1", "ordem2", "ordem3" e "ordem4"
borda_inicio_df['Ranking_Borda'] = borda_inicio_df[['ordem1', 'ordem2', 'ordem3', 'ordem4']].sum(axis=1)

# Exibindo o DataFrame resultante
st.table(borda_inicio_df)



# Mantendo apenas a primeira e a última coluna
borda_inicio_df = borda_inicio_df.iloc[:, [0, -1]]

# Renomeando a coluna
borda_inicio_df = borda_inicio_df.rename(columns={'Ranking_Borda': 'Ranking_Final'})
st.write(borda_inicio_df)

st.caption("Desenvolvido pela empregada Jaqueline Alves do Nascimento")
