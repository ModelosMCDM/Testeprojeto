import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Inicializa variáveis globais
desafioData = None
num_alternatives = None
alternative_names = None
desafioNormalAll = []
alternativasList = None

# Funções matemáticas
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
        st.write(f'Inconsistente: {cr:.2f}')
    else:
        st.write(f'É Consistente: {cr:.2f}')

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
            value = st.number_input(f"O quão preferível a alternativa {names[i]} é em relação a {names[j]} (1 a 9):", min_value=1.0, max_value=9.0, step=0.1)
            matrix[i][j] = value
            matrix[j][i] = 1 / value
    np.fill_diagonal(matrix, 1)  # Preencher a diagonal principal com 1
    return matrix

# Funções de exibição e processamento
def processar_matriz_alternativas(matriz, criterio_nome):
    normalizada = NormalizingConsistency(pd.DataFrame(matriz, columns=alternative_names, index=alternative_names))
    st.write(f"Matriz normalizada para o critério '{criterio_nome}':")
    st.dataframe(normalizada)

    st.write(f"Teste de consistência para o critério '{criterio_nome}':")
    Consistencia = normalizada.to_numpy()
    l, v = VV(Consistencia)
    st.write(f"Autovalor: {l:.2f}")
    st.write('Autovetor:', np.round(v, 2))
    DadosSaaty(l, Consistencia.shape[0])

    peso = NormalizingCritera(pd.DataFrame(matriz, columns=alternative_names, index=alternative_names))
    st.write(f"Vetor de peso para o critério '{criterio_nome}':")
    st.dataframe(peso[['MatrizdePeso']])
    return peso[['MatrizdePeso']]

def main():
    global desafioData, num_alternatives, alternative_names, num_criteria, criteria_names, desafioNormalAll

    st.title("Metodologia AHP para Priorização de Alternativas")

    num_alternatives = st.number_input("Quantas alternativas você deseja avaliar? (min 2)", min_value=2, step=1)
    num_criteria = st.number_input("Quantos critérios você deseja usar na avaliação?", min_value=1, step=1)

    # Nome dos critérios
    criteria_names = []
    for i in range(num_criteria):
        criteria_name = st.text_input(f"Informe o nome do critério {i + 1}:")
        criteria_names.append(criteria_name)

    # Nome das alternativas
    alternative_names = []
    for i in range(num_alternatives):
        alternative_name = st.text_input(f"Informe o nome da alternativa {i + 1}:")
        alternative_names.append(alternative_name)

    st.write("Insira as comparações par a par para os critérios:")
    matrix_criteria = get_comparison_matrix(num_criteria, criteria_names)

    desafioData = pd.DataFrame(matrix_criteria, index=criteria_names, columns=criteria_names).round(2)
    st.write("Matriz de Comparação dos Critérios:")
    st.dataframe(desafioData)

    normalizandocriterio = NormalizingConsistency(desafioData)
    st.write("Matriz Normalizada dos Critérios:")
    st.dataframe(normalizandocriterio)

    st.write("Teste de consistência:")
    Consistencia1 = normalizandocriterio.to_numpy()
    l, v = VV(Consistencia1)
    st.write(f"Autovalor: {l:.2f}")
    st.write('Autovetor:', np.round(v, 2))
    DadosSaaty(l, Consistencia1.shape[0])

    TabelaPesoDosCriterios = NormalizingCritera(desafioData)
    desafioNormalAll.append(TabelaPesoDosCriterios)
    st.write("Vetor de Peso dos Critérios:")
    st.dataframe(TabelaPesoDosCriterios)

    # Gráfico de pesos
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=TabelaPesoDosCriterios.index, y='MatrizdePeso', data=TabelaPesoDosCriterios, ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

if __name__ == "__main__":
    main()
