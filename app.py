import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Inicializa variáveis globais
desafioNormalAll = []  # Para armazenar as tabelas normalizadas
alternative_names = None
criteria_names = None

# Funções Matemáticas
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
    return cr

def VV(Consistencia):
    l, v = np.linalg.eig(Consistencia)
    v = v.T
    i = np.where(l == np.max(l))[0][0]
    l = l[i]
    v = v[i]
    v = v / np.sum(v)
    return np.real(l), np.real(v)

# Função para gerar matriz de comparação
def get_comparison_matrix(n, names):
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            value = st.number_input(f"Comparação entre {names[i]} e {names[j]}", min_value=1.0, max_value=9.0, step=1.0)
            matrix[i][j] = value
            matrix[j][i] = 1 / value
    np.fill_diagonal(matrix, 1)  # Preenche a diagonal principal com 1
    return matrix

# Função principal para o AHP
def main():
    global alternative_names, criteria_names, desafioNormalAll  # Variáveis globais

    st.title("Avaliação de Alternativas com AHP")

    num_alternatives = st.number_input("Quantas alternativas você deseja avaliar?", min_value=2, step=1)
    num_criteria = st.number_input("Quantos critérios você deseja usar?", min_value=1, step=1)

    if num_alternatives > 1 and num_criteria > 0:
        # Nome dos critérios
        st.subheader("Nome dos Critérios")
        criteria_names = [st.text_input(f"Critério {i + 1}") for i in range(num_criteria)]

        # Nome das alternativas
        st.subheader("Nome das Alternativas")
        alternative_names = [st.text_input(f"Alternativa {i + 1}") for i in range(num_alternatives)]

        if st.button("Gerar Matriz de Comparação dos Critérios"):
            # Matriz de comparação par a par dos critérios
            matrix_criteria = get_comparison_matrix(num_criteria, criteria_names)
            df_criteria = pd.DataFrame(matrix_criteria, index=criteria_names, columns=criteria_names)

            st.write("Matriz de Comparação dos Critérios:")
            st.write(df_criteria)

            # Normalização e consistência
            normalizandocriterio = NormalizingConsistency(df_criteria)
            st.write("Matriz de Comparação Normalizada dos Critérios:")
            st.write(normalizandocriterio)

            Consistencia1 = normalizandocriterio.to_numpy()
            l, v = VV(Consistencia1)
            cr = DadosSaaty(l, Consistencia1.shape[0])
            st.write(f"Autovalor: {l:.2f}")
            st.write(f"Autovetor: {np.round(v, 2)}")
            st.write(f"Índice de Consistência: {cr:.2f}")

            if cr > 0.1:
                st.warning("A matriz é inconsistente!")
            else:
                st.success("A matriz é consistente!")

            # Vetor de peso dos critérios
            TabelaPesoDosCriterios = NormalizingCritera(df_criteria)
            desafioNormalAll.append(TabelaPesoDosCriterios)

            st.write("Vetor de Peso dos Critérios:")
            st.write(TabelaPesoDosCriterios)

            # Gráfico de peso dos critérios
            st.subheader("Gráfico de Peso dos Critérios")
            plt.figure(figsize=(10, 5))
            ax = sns.barplot(x=TabelaPesoDosCriterios.index, y=TabelaPesoDosCriterios['MatrizdePeso'])
            plt.xticks(rotation=45)
            st.pyplot(plt)

    # Adicionar funcionalidade para comparar alternativas, se desejar
    # ...

if __name__ == "__main__":
    main()
