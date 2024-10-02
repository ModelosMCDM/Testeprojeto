import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Inicializando variáveis globais
desafioNormalAll = []

# Criando as funções matemáticas
def NormalizingConsistency(dataP):
    resultP = dataP.copy()
    for col in resultP.columns:
        resultP[col] = resultP[col] / sum(resultP[col])
    return resultP

def NormalizingCritera(dataP):
    resultP = dataP.copy()
    resultP["Csoma"] = 0
    for col in resultP.columns:
        resultP[col] = resultP[col] / sum(resultP[col])
        resultP["Csoma"] += resultP[col]
    resultP['MatrizdePeso'] = resultP["Csoma"] / len(resultP.columns)
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
            value = st.number_input(f"O quão preferível a alternativa {names[i]} é em relação a {names[j]}:", 1.0, 9.0)
            matrix[i][j] = value
            matrix[j][i] = 1 / value
    np.fill_diagonal(matrix, 1)
    return matrix

def processar_matriz_alternativas(matriz, criterio_nome):
    # Normaliza a matriz
    normalizada = NormalizingConsistency(pd.DataFrame(matriz, columns=alternative_names, index=alternative_names))
    st.write(f"Matriz de comparação em pares das alternativas para o critério '{criterio_nome}' normalizada:")
    st.write(normalizada)

    # Teste de consistência
    Consistencia = normalizada.to_numpy()
    l, v = VV(Consistencia)
    st.write(f"Autovalor: {l:.2f}")
    st.write(f"Autovetor: {np.round(v, 2)}")
    DadosSaaty(l, Consistencia.shape[0])

    # Vetor de peso
    peso = NormalizingCritera(pd.DataFrame(matriz, columns=alternative_names, index=alternative_names))
    st.write(f"Vetor de peso para o critério '{criterio_nome}':")
    st.write(peso)
    
    return peso[['MatrizdePeso']]

def finalizar_matriz_priorizacao_alternativas(desafioNormalAll, criteriosList, alternativasList):
    matrizPriorizacaoAlternativasAHP = pd.DataFrame(desafioNormalAll[0]['MatrizdePeso'])
    matrizPriorizacaoAlternativasAHP.columns = ['Peso dos Critérios']

    for alt in alternativasList:
        auxList = []
        for crit in criteriosList:
            i = criteriosList.index(crit) + 1
            auxList.append(desafioNormalAll[i]['MatrizdePeso'][alt])
        matrizPriorizacaoAlternativasAHP[alt] = auxList

    st.write("Matriz de Priorização de todas as alternativas:")
    st.write(matrizPriorizacaoAlternativasAHP)
    return matrizPriorizacaoAlternativasAHP

def main():
    st.title("Método AHP (Analytic Hierarchy Process)")
    
    # Entrada do número de alternativas e critérios
    num_alternatives = st.number_input("Quantas alternativas você deseja avaliar?", min_value=2, value=3)
    num_criteria = st.number_input("Quantos critérios você deseja usar na avaliação?", min_value=1, value=3)

    # Nome dos critérios
    criteria_names = []
    for i in range(num_criteria):
        criteria_name = st.text_input(f"Informe o nome do critério {i + 1}:", value=f"Critério {i + 1}")
        criteria_names.append(criteria_name)

    # Nome das alternativas
    alternative_names = []
    for i in range(num_alternatives):
        alternative_name = st.text_input(f"Informe o nome da alternativa {i + 1}:", value=f"Alternativa {i + 1}")
        alternative_names.append(alternative_name)

    # Matriz de comparação par a par para critérios
    st.write("Insira as comparações par a par para os critérios:")
    matrix_criteria = get_comparison_matrix(num_criteria, criteria_names)
    desafioData = pd.DataFrame(matrix_criteria, index=criteria_names, columns=criteria_names)
    st.write("Matriz de comparação em pares dos critérios:")
    st.write(desafioData)

    # Normaliza dados
    normalizandocriterio = NormalizingConsistency(desafioData)
    st.write("Matriz de comparação dos critérios normalizada:")
    st.write(normalizandocriterio)

    # Teste de consistência
    Consistencia1 = normalizandocriterio.to_numpy()
    l, v = VV(Consistencia1)
    st.write(f"Autovalor: {l:.2f}")
    st.write(f"Autovetor: {np.round(v, 2)}")
    DadosSaaty(l, Consistencia1.shape[0])

    # Vetor de peso dos critérios
    TabelaPesoDosCriterios = NormalizingCritera(desafioData)
    desafioNormalAll.append(TabelaPesoDosCriterios)
    st.write("Vetor de peso dos critérios:")
    st.write(TabelaPesoDosCriterios)

    # Comparação das alternativas para cada critério
    for i in range(num_criteria):
        criterio_nome = criteria_names[i]
        st.write(f"Insira a matriz de priorizações par a par de cada alternativa para o critério '{criterio_nome}':")
        DadosCriterio = get_comparison_matrix(num_alternatives, alternative_names)
        processar_matriz_alternativas(DadosCriterio, criterio_nome)

    # Finalizando a Matriz de Priorização de todas alternativas
    matrizPriorizacaoAlternativasAHP = finalizar_matriz_priorizacao_alternativas(desafioNormalAll, criteria_names, alternative_names)

    # Calculando a soma ponderada para cada coluna (alternativa)
    peso_dos_criterios = matrizPriorizacaoAlternativasAHP['Peso dos Critérios'].values
    soma_ponderada = {}
    
    for alternativa in alternative_names:
        soma_ponderada[alternativa] = np.sum(matrizPriorizacaoAlternativasAHP[alternativa].values * peso_dos_criterios)

    # Exibindo o ranking final
    soma_ponderada_series = pd.Series(soma_ponderada, name='Valor')
    ranking = soma_ponderada_series.rank(ascending=False, method='min').astype(int)
    ranking_df = pd.DataFrame({'Alternativa': soma_ponderada_series.index, 'Ranking': ranking, 'Valor': soma_ponderada_series.values})
    
    st.write("Ranking final das alternativas:")
    st.write(ranking_df)

if __name__ == "__main__":
    main()
