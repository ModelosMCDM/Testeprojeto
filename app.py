import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
def get_comparison_matrix(n, names, matrix_key):
    matrix = np.zeros((n, n))

    if matrix_key not in st.session_state:
        st.session_state[matrix_key] = matrix
    else:
        matrix = st.session_state[matrix_key]

    for i in range(n):
        for j in range(i + 1, n):
            value = st.number_input(f"O quão preferível a alternativa {names[i]} é em relação a {names[j]}",
                                    value=matrix[i][j] if matrix[i][j] != 0 else 1.0,
                                    min_value=1.0, max_value=9.0, step=1.0, key=f"{i}-{j}-{matrix_key}")
            matrix[i][j] = value
            matrix[j][i] = 1 / value
    np.fill_diagonal(matrix, 1)
    st.session_state[matrix_key] = matrix
    return matrix

def main():
    st.title("Avaliação de Alternativas com AHP")

    num_alternatives = st.number_input("Quantas alternativas você deseja avaliar?", min_value=2, step=1)
    num_criteria = st.number_input("Quantos critérios você deseja usar?", min_value=3, step=1)

    if num_alternatives > 1 and num_criteria > 0:
        st.subheader("Nome dos Critérios")
        criteria_names = []
        for i in range(num_criteria):
            criteria_names.append(st.text_input(f"Critério {i + 1}", key=f"criterio-{i}"))

        if all(criteria_names):
            st.subheader("Nome das Alternativas")
            alternative_names = []
            for i in range(num_alternatives):
                alternative_names.append(st.text_input(f"Alternativa {i + 1}", key=f"alternativa-{i}"))

            if all(alternative_names):
                st.subheader("Matriz de Comparação dos Critérios:")
                matrix_criteria = get_comparison_matrix(num_criteria, criteria_names, "matrix_criteria")
                df_criteria = pd.DataFrame(matrix_criteria, index=criteria_names, columns=criteria_names)

                gerar_matriz = st.button("Gerar Matriz de Comparação dos Critérios")

                if gerar_matriz:
                    st.write("Matriz de Comparação dos Critérios:")
                    st.write(df_criteria)

                    normalizandocriterio = NormalizingConsistency(df_criteria)
                    st.write("Matriz de Comparação Normalizada dos Critérios:")
                    st.write(normalizandocriterio)

                    Consistencia1 = normalizandocriterio.to_numpy()
                    l, v = VV(Consistencia1)

                    # Verificação adicional para evitar erro
                    if v is None or len(v) == 0:
                        st.error("Erro ao calcular os pesos dos critérios.")
                        return
                    
                    cr = DadosSaaty(l, Consistencia1.shape[0])
                    st.write(f"Autovalor: {l:.2f}")
                    st.write(f"Autovetor: {np.round(v, 2)}")
                    st.write(f"Índice de Consistência: {cr:.2f}")

                    if cr > 0.1:
                        st.warning("A matriz é inconsistente!")
                    else:
                        st.success("A matriz é consistente!")

                    TabelaPesoDosCriterios = NormalizingCritera(df_criteria)
                    st.write("Vetor de Peso dos Critérios:")
                    st.write(TabelaPesoDosCriterios)

                    st.subheader("Gráfico de Peso dos Critérios")
                    plt.figure(figsize=(10, 5))
                    ax = sns.barplot(x=TabelaPesoDosCriterios.index, y=TabelaPesoDosCriterios['MatrizdePeso'])
                    plt.xticks(rotation=45)
                    st.pyplot(plt)

                st.subheader("Montagem da matriz de priorizações par a par de cada alternativa por critério")
                alternativas_por_criterio = {}

                for i in range(num_criteria):
                    criterio_nome = criteria_names[i]
                    st.write(f"\nCritério {i + 1}: {criterio_nome}")
                    matriz_alternativas = get_comparison_matrix(num_alternatives, alternative_names, f"alternatives_matrix_{i}")
                    df_alternativas = pd.DataFrame(matriz_alternativas, index=alternative_names, columns=alternative_names)
                    st.write("Tabela de Comparação das Alternativas:")
                    st.write(df_alternativas)

                    normalizando_alternativas = NormalizingConsistency(df_alternativas)
                    st.write(f"Matriz de comparação em pares das alternativas para o critério '{criterio_nome}' normalizada:")
                    st.write(normalizando_alternativas)

                    Consistencia_alt = normalizando_alternativas.to_numpy()
                    l_alt, v_alt = VV(Consistencia_alt)
                    cr_alt = DadosSaaty(l_alt, Consistencia_alt.shape[0])
                    st.write(f"Teste de consistência para o critério '{criterio_nome}':")
                    st.write(f"Autovalor: {l_alt:.2f}")
                    st.write(f"Autovetor: {np.round(v_alt, 2)}")
                    st.write(f"Índice de Consistência: {cr_alt:.2f}")

                    if cr_alt > 0.1:
                        st.warning(f"A matriz de alternativas para o critério '{criterio_nome}' é inconsistente!")
                    else:
                        st.success(f"A matriz de alternativas para o critério '{criterio_nome}' é consistente!")

                    TabelaPesoDasAlternativas = NormalizingCritera(df_alternativas)
                    st.write(f"Vetor de peso para o critério '{criterio_nome}':")
                    st.write(TabelaPesoDasAlternativas)

                    alternativas_por_criterio[criterio_nome] = TabelaPesoDasAlternativas

                # Geração da matriz de priorização final
                if alternativas_por_criterio:
                    st.subheader("Matriz de Priorização de todas as alternativas")
                    
                    # Vetores de peso dos critérios
                    pesos_criterios = v

                    # Verificação adicional para evitar erro
                    if pesos_criterios is None or len(pesos_criterios) == 0:
                        st.error("Erro ao calcular os pesos dos critérios na matriz final.")
                        return

                    # Matriz de priorização final
                    matriz_priorizacao_final = pd.DataFrame(0, index=alternative_names, columns=criteria_names)

                    for criterio, pesos_alternativas in alternativas_por_criterio.items():
                        matriz_priorizacao_final[criterio] = pesos_alternativas["MatrizdePeso"].values

                    # Multiplicação dos vetores de peso dos critérios com os das alternativas
                    for alt in alternative_names:
                        matriz_priorizacao_final.loc[alt, "Total"] = np.sum(matriz_priorizacao_final.loc[alt, criteria_names] * pesos_criterios)

                    st.write(matriz_priorizacao_final)

if __name__ == "__main__":
    main()
