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

# Função para gerar matriz de comparação par a par entre alternativas
def get_comparison_matrix(n, alternative_names, matrix_key="matrix_alternatives"):
    """ Função para gerar uma matriz de comparação par a par entre alternativas. """
    matrix = np.zeros((n, n))
    
    # Armazena o estado da matriz entre interações
    if matrix_key not in st.session_state:
        st.session_state[matrix_key] = matrix
    else:
        matrix = st.session_state[matrix_key]

    for i in range(n):
        for j in range(i + 1, n):
            value = st.number_input(
                f"O quão preferível a alternativa '{alternative_names[i]}' é em relação à alternativa '{alternative_names[j]}'?",
                value=matrix[i][j] if matrix[i][j] != 0 else 1.0,
                min_value=1.0, max_value=9.0, step=1.0,
                key=f"{i}-{j}-{matrix_key}"
            )
            matrix[i][j] = value
            matrix[j][i] = 1 / value
    np.fill_diagonal(matrix, 1)  # Preenche a diagonal principal com 1
    st.session_state[matrix_key] = matrix
    return matrix

def exibir_tabela_comparacao_alternativas(alternative_names, DadosCriterio, criterio_nome):
    """Exibe a tabela de comparação de alternativas."""
    st.write(f"Tabela de Comparação para o Critério: {criterio_nome}")
    st.write(pd.DataFrame(DadosCriterio, index=alternative_names, columns=alternative_names))

def processar_matriz_alternativas(DadosCriterio, criterio_nome):
    """Processa a matriz de alternativas e retorna pesos."""
    # Normalização e cálculo de pesos - modifique conforme necessário
    normalizada = NormalizingCritera(pd.DataFrame(DadosCriterio))
    return normalizada['MatrizdePeso']

# HTML de Cabeçalho
html_temp = """<img src="https://static-media.hotmart.com/d0IFT5pYRau6qyuHzfkd7_dgt6Q=/300x300/smart/filters:format(webp):background_color(white)/hotmart/product_pictures/686dcc4a-78b0-4b94-923b-c673a8ef5e75/Avatar.PNG" alt="Descrição da imagem" style="width: 50px; height: 50px;">
<div style="text-align:center; background-color: #f0f0f0; border: 1px solid #ccc; padding: 10px;">
    <h3 style="color: black; margin-bottom: 10px;">Metodologia de apoio à decisão para manutenção inteligente, combinando abordagens multicritério</h3>
    <p style="color: black; margin-bottom: 10px;">AHP 5555 - Xxxxxx 3</p>
    <p style="color: black; margin-bottom: 10px;">Modo de uso: Aplique-o para escolha entre quaisquer alternativas e critérios</p>
    <p style="color: black; margin-bottom: 10px;">Todos os métodos funcionarão automaticamente</p>
    <p style="color: black; margin-bottom: 10px;">Jaqueline Alves do Nascimento</p></div>"""

st.markdown(html_temp, unsafe_allow_html=True)

# Função principal para o AHP
def main():
    st.title("Avaliação de Alternativas com AHP")
    
    num_alternatives = st.number_input("Quantas alternativas você deseja avaliar?", min_value=2, step=1)
    num_criteria = st.number_input("Quantos critérios você deseja usar?", min_value=1, step=1)

    if num_alternatives > 1 and num_criteria > 0:
        # Nome dos critérios
        st.subheader("Nome dos Critérios")
        criteria_names = []
        for i in range(num_criteria):
            criteria_names.append(st.text_input(f"Critério {i + 1}", key=f"criterio-{i}"))

        # Verifica se todos os critérios foram preenchidos
        if all(criteria_names):
            # Nome das alternativas
            st.subheader("Nome das Alternativas")
            alternative_names = []
            for i in range(num_alternatives):
                alternative_names.append(st.text_input(f"Alternativa {i + 1}", key=f"alternativa-{i}"))

            # Verifica se todas as alternativas foram preenchidas
            if all(alternative_names):
                # Matriz de comparação par a par dos critérios
                st.subheader("Matriz de Comparação dos Critérios:")
                matrix_criteria = get_comparison_matrix_criteria(num_criteria, criteria_names, "matrix_criteria")
                df_criteria = pd.DataFrame(matrix_criteria, index=criteria_names, columns=criteria_names)

                # Botão para gerar a matriz
                gerar_matriz = st.button("Gerar Matriz de Comparação dos Critérios")

                if gerar_matriz:
                    # Exibe a matriz de comparação
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
                    st.write("Vetor de Peso dos Critérios:")
                    st.write(TabelaPesoDosCriterios)

                    # Gráfico de peso dos critérios
                    st.subheader("Gráfico de Peso dos Critérios")
                    plt.figure(figsize=(10, 5))
                    ax = sns.barplot(x=TabelaPesoDosCriterios.index, y=TabelaPesoDosCriterios['MatrizdePeso'])
                    plt.xticks(rotation=45)
                    st.pyplot(plt)

                # Função para montagem da matriz de priorizações par a par de cada alternativa
                st.subheader("Montagem da matriz de priorizações par a par de cada alternativa por critério")
                desafioNormalAll = []  # Inicializa a lista para armazenar pesos

                for i in range(num_criteria):
                    criterio_nome = criteria_names[i]
                    DadosCriterio = get_comparison_matrix(num_alternatives, alternative_names)
                    exibir_tabela_comparacao_alternativas(alternative_names, DadosCriterio, criterio_nome)

                    # Processar a matriz de alternativas
                    peso_criterio = processar_matriz_alternativas(DadosCriterio, criterio_nome)
                    desafioNormalAll.append(peso_criterio)

if __name__ == "__main__":
    main()

