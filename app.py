# Importando pacotes
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Inicializando variáveis globais
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
            value = st.number_input(f"O quão preferível a alternativa {names[i]} é em relação a {names[j]} (de 1 a 9):", 1.0, 9.0, step=0.1)
            matrix[i][j] = value
            matrix[j][i] = 1 / value
    np.fill_diagonal(matrix, 1)  # Preencher a diagonal principal com 1
    return matrix

def processar_matriz_alternativas(matriz, criterio_nome):
    # Normaliza a matriz
    normalizada = NormalizingConsistency(pd.DataFrame(matriz, columns=alternative_names, index=alternative_names))
    st.write(f"Matriz de comparação em pares das alternativas para o critério '{criterio_nome}' normalizada:", normalizada)

    # Teste de consistência
    st.write(f"Teste de consistência para o critério '{criterio_nome}':")
    Consistencia = normalizada.to_numpy()
    l, v = VV(Consistencia)
    st.write(f'Autovalor: {l:.2f}')
    st.write(f'Autovetor: {np.round(v, 2)}')
    DadosSaaty(l, Consistencia.shape[0])

    # Vetor de peso
    peso = NormalizingCritera(pd.DataFrame(matriz, columns=alternative_names, index=alternative_names))
    st.write(f"Vetor de peso para o critério '{criterio_nome}':", peso)

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

    st.write("Matriz de Priorização de todas as alternativas:", matrizPriorizacaoAlternativas)
    return matrizPriorizacaoAlternativas

# Função principal
def main():
    global desafioData, num_alternatives, alternative_names, num_criteria, criteria_names, desafioNormalAll
    
    st.title("Análise de Decisão Multicritério (AHP)")
    
    num_alternatives = st.number_input("Quantas alternativas você deseja avaliar? Inclua no mínimo 2", min_value=2, step=1)
    num_criteria = st.number_input("Quantos critérios você deseja usar na avaliação?", min_value=1, step=1)
    
    # Nome dos critérios
    criteria_names = [st.text_input(f"Informe o nome do critério {i + 1}:") for i in range(num_criteria)]
    
    # Nome das alternativas
    alternative_names = [st.text_input(f"Informe o nome da alternativa {i + 1}:") for i in range(num_alternatives)]
    
    # Matriz de comparação par a par para critérios
    st.write("Insira as comparações par a par para os critérios:")
    matrix_criteria = get_comparison_matrix(num_criteria, criteria_names)
    desafioData = pd.DataFrame(matrix_criteria, index=criteria_names, columns=criteria_names)
    desafioData = desafioData.round(2)
    st.write("Matriz de comparação em pares dos critérios:", desafioData)

    # Normalização
    normalizandocriterio = NormalizingConsistency(desafioData)
    st.write("Matriz de comparação em pares dos critérios normalizada:", normalizandocriterio)

    # Teste de consistência
    st.write("Teste de consistência:")
    Consistencia1 = normalizandocriterio.to_numpy()
    l, v = VV(Consistencia1)
    st.write(f'Autovalor: {l:.2f}')
    st.write(f'Autovetor: {np.round(v, 2)}')
    DadosSaaty(l, Consistencia1.shape[0])

    # Vetor de pesos dos critérios
    TabelaPesoDosCriterios = NormalizingCritera(desafioData)
    desafioNormalAll.append(TabelaPesoDosCriterios)
    st.write("Vetor de peso dos critérios:", TabelaPesoDosCriterios)

    # Gráfico dos valores normalizados dos critérios
    st.write("Gráfico da matriz de peso dos critérios:")
    plt.figure(figsize=(12, 6))
    plt.title("Matriz de peso dos critérios", fontsize=20)
    ax = sns.barplot(x=TabelaPesoDosCriterios.index, y='MatrizdePeso', data=TabelaPesoDosCriterios)
    for p in ax.patches:
        height = p.get_height()
        ax.text(p.get_x() + p.get_width() / 2, height, '{:.2f}'.format(height), ha='center', va='bottom')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(plt)

    # Comparação par a par para alternativas por critério
    for i, criterio_nome in enumerate(criteria_names):
        st.write(f"Insira a matriz de priorizações par a par das alternativas para o critério {i + 1} ({criterio_nome}):")
        DadosCriterio = get_comparison_matrix(num_alternatives, alternative_names)
        peso_criterio = processar_matriz_alternativas(DadosCriterio, criterio_nome)
        desafioNormalAll.append(peso_criterio)

    # Finalizar a matriz de priorização
    matrizPriorizacaoAlternativas = finalizar_matriz_priorizacao_alternativas(desafioNormalAll, criteria_names, alternative_names)
    
if __name__ == "__main__":
    main()


