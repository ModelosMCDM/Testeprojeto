Para ajustar o código fornecido para funcionar no Streamlit, você precisará fazer algumas modificações, especialmente para substituir as entradas de console por widgets do Streamlit e para exibir os gráficos e tabelas diretamente na interface do Streamlit. Aqui está uma versão ajustada do seu código:

```python
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def NormalizingConsistency(dataP):
    resultP = dataP.copy()
    columnsP = resultP.columns.tolist()
    for x in columnsP:
        resultP[x] = resultP[x] / sum(resultP[x])
    return resultP

def NormalizingCritera(dataP):
    resultP = dataP.copy()
    columnsP = resultP.columns.tolist()
    resultP["Csoma"] = 0
    for x in columnsP:
        resultP[x] = resultP[x] / sum(resultP[x])
        resultP["Csoma"] += resultP[x]
    resultP['MatrizdePeso'] = resultP["Csoma"] / len(columnsP)
    return resultP

def DadosSaaty(lamb, N):
    ri = [0, 0, 0.58, 0.9, 1.12, 1.32, 1.35, 1.41, 1.45, 1.49, 1.52, 1.54, 1.56, 1.58, 1.59]
    ci = (lamb - N) / (N - 1)
    cr = ci / ri[N]
    if cr > 0.1:
        st.write('Inconsistente: %.2f' % cr)
    else:
        st.write('É Consistente: %.2f' % cr)

def VV(Consistencia):
    l, v = np.linalg.eig(Consistencia)
    v = v.T
    i = np.where(l == np.max(l))[0][0]
    l = l[i]
    v = v[i]
    v = v / np.sum(v)
    return np.real(l), np.real(v)

def get_comparison_matrix(n, names):
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            value = st.number_input(f"O quão preferível a alternativa {names[i]} é em relação a {names[j]}:", min_value=1.0, max_value=9.0, step=1.0)
            matrix[i][j] = value
            matrix[j][i] = 1 / value
    np.fill_diagonal(matrix, 1)
    return matrix

def exibir_tabela_comparacao_criterios(nomes, matriz):
    df = pd.DataFrame(matriz, index=nomes, columns=nomes)
    df = df.round(2)
    st.write("Tabela de Comparação dos Critérios:")
    st.dataframe(df)

def exibir_tabela_comparacao_alternativas(nomes, matriz, criterio_nome):
    df = pd.DataFrame(matriz, index=nomes, columns=nomes)
    df = df.round(2)
    st.write(f"Tabela de Comparação das Alternativas para o critério '{criterio_nome}':")
    st.dataframe(df)

def processar_matriz_alternativas(matriz, criterio_nome):
    normalizada = NormalizingConsistency(pd.DataFrame(matriz, columns=alternative_names, index=alternative_names))
    st.write(f"Matriz de comparação em pares das alternativas para o critério '{criterio_nome}' normalizada:")
    st.dataframe(normalizada)
 
    st.write(f"Teste de consistência para o critério '{criterio_nome}':")
    Consistencia = normalizada.to_numpy()
    l, v = VV(Consistencia)
    st.write('Autovalor: %.2f' % l)
    st.write('Autovetor: ', np.round(v, 2))
    DadosSaaty(l, Consistencia.shape[0])
    peso = NormalizingCritera(pd.DataFrame(matriz, columns=alternative_names, index=alternative_names))
    st.write(f"Vetor de peso para o critério '{criterio_nome}':")
    st.dataframe(peso)
    return peso[['MatrizdePeso']]

def finalizar_matriz_priorizacao_alternativas(desafioNormalAll, criteriosList, alternativasList):
    matrizPriorizacaoAlternativas = pd.DataFrame(desafioNormalAll[0]['MatrizdePeso'])
    matrizPriorizacaoAlternativas.columns = ['Peso dos Critérios']
    for alt in alternativasList:
        auxList = []
        for crit in criteriosList:
            i = criteriosList.index(crit) + 1
            auxList.append(desafioNormalAll[i]['MatrizdePeso'][alt])
        matrizPriorizacaoAlternativas[alt] = auxList
    st.write("Matriz de Priorização de todas as alternativas:")
    st.dataframe(matrizPriorizacaoAlternativas)
    return matrizPriorizacaoAlternativas

def main():
    global desafioData, num_alternatives, alternative_names, num_criteria, criteria_names, desafioNormalAll
    st.title("Análise de Decisão Multicritério")
    
    num_alternatives = st.number_input("Quantas alternativas você deseja avaliar? Inclua no mínimo 2", min_value=2, step=1)
    num_criteria = st.number_input("Quantos critérios você deseja usar na avaliação?", min_value=1, step=1)
    
    criteria_names = []
    for i in range(num_criteria):
        criteria_name = st.text_input(f"Informe o nome do critério {i + 1}:")
        criteria_names.append(criteria_name)
    
    alternative_names = []
    for i in range(num_alternatives):
        alternative_name = st.text_input(f"Informe o nome da alternativa {i + 1}:")
        alternative_names.append(alternative_name)
    
    st.write("Insira as comparações par a par para os critérios:")
    matrix_criteria = get_comparison_matrix(num_criteria, criteria_names)
    desafioData = pd.DataFrame(matrix_criteria, index=criteria_names, columns=criteria_names)
    desafioData = desafioData.round(2)
    st.write("Matriz de comparação em pares dos critérios:")
    st.dataframe(desafioData)
    
    normalizandocriterio = NormalizingConsistency(desafioData)
    st.write("Matriz de comparação em pares dos critérios normalizada:")
    st.dataframe(normalizandocriterio)
    
    st.write("Teste de consistência:")
    Consistencia1 = normalizandocriterio.to_numpy()
    l, v = VV(Consistencia1)
    st.write('Autovalor: %.2f' % l)
    st.write('Autovetor: ', np.round(v, 2))
    DadosSaaty(l, Consistencia1.shape[0])
    
    TabelaPesoDosCriterios = NormalizingCritera(desafioData)
    desafioNormalAll.append(TabelaPesoDosCriterios)
    st.write("Vetor de peso dos critérios:")
    st.dataframe(TabelaPesoDosCriterios)
    
    plt.figure(figsize=(12, 6))
    plt.title("Matriz de peso dos critérios", fontsize=20)
    ax = sns.barplot(x=TabelaPesoDosCriterios.index, y='MatrizdePeso', data=TabelaPesoDosCriterios, legend=False)
    for p in ax.patches:
        height = p.get_height()
        ax.text(p.get_x() + p.get_width() / 2, height, '{:.2f}'.format(height), ha='center', va='bottom', fontsize=10)
    plt.xlabel('Critérios', fontsize=12)
    plt.ylabel('Pesos', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    st.pyplot(plt)

    alternativas_por_criterio = {}
    for i in range(num_criteria):
        criterio_nome = criteria_names[i]
        st.write(f"Insira a matriz de priorizações par a par de cada alternativa para o critério {i + 1} ({criterio_nome}):")
        DadosCriterio = get_comparison_matrix(num_alternatives, alternative_names)
        exibir_tabela_comparacao_alternativas(alternative_names, DadosCriterio, criterio_nome)
        peso_criterio = processar_matriz_alternativas(DadosCriterio, criterio_nome)
        desafioNormalAll.append(peso_criterio)
    
    matrizPriorizacaoAlternativas = finalizar_matriz_priorizacao_alternativas(desafioNormalAll, criteria_names, alternative_names)
    peso_dos_criterios = matrizPriorizacaoAlternativas['Peso dos Critérios'].values
    soma_ponderada = {}
    for alternativa in alternative_names:
        soma_ponderada[alternativa] = np.sum(matrizPriorizacaoAlternativas[alternativa].values * peso_dos_criterios)
    soma_ponderada_series = pd.Series(soma_ponderada, name='soma')
    matrizPriorizacaoAlternativas = pd.concat([matrizPriorizacaoAlternativas, soma_ponderada_series.to_frame().T])
    matrizPriorizacaoAlternativas = matrizPriorizacaoAlternativas.drop(columns=['Peso dos Critérios'])
    st.write(matrizPriorizacaoAlternativas)
    st.write(type(matrizPriorizacaoAlternativas))
    matriz_np = np.array(matrizPriorizacaoAlternativas)
    matriz_df = pd
