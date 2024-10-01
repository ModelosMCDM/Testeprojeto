import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")

# Configuração da página
st.set_page_config(
    page_title="MESTRADO",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Função para gerar a matriz de comparação
def gerar_matriz_comparacao(num_criterios):
    matriz = np.zeros((num_criterios, num_criterios))
    for i in range(num_criterios):
        for j in range(i + 1, num_criterios):
            key = f"comparacao_{i}_{j}"
            if key not in st.session_state:
                st.session_state[key] = 1.0  # Default value

            valor = st.number_input(
                f"Informe a importância do critério {i+1} em relação ao critério {j+1}", 
                min_value=0.0, step=0.1, value=st.session_state[key],
                key=key
            )
            
            # Check to avoid division by zero
            if valor == 0:
                st.warning(f"O valor não pode ser zero para a comparação entre critério {i+1} e critério {j+1}.")
                continue  # Skip the current iteration if valor is 0

            matriz[i, j] = valor
            matriz[j, i] = 1 / valor

    return matriz

# Função para calcular consistência usando o método de Saaty
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

# Função para calcular autovalores e autovetores
def VV(Consistencia):
    l, v = np.linalg.eig(Consistencia)
    v = v.T
    i = np.where(l == np.max(l))[0][0]
    l = l[i]
    v = v[i]
    v = v / np.sum(v)
    return np.real(l), np.real(v)

# Interface do Streamlit para inputs do usuário
st.title("Método AHP - Comparação de Critérios")

# Input de critérios e alternativas
num_criterios = st.number_input("Quantos critérios você deseja avaliar?", min_value=2, step=1)
criterios = []
for i in range(num_criterios):
    criterio = st.text_input(f"Digite o nome do critério {i+1}:")
    criterios.append(criterio)

num_alternativas = st.number_input("Quantas alternativas você deseja avaliar?", min_value=2, step=1)
alternativas = []
for i in range(num_alternativas):
    alternativa = st.text_input(f"Digite o nome da alternativa {i+1}:")
    alternativas.append(alternativa)

if st.button("Gerar Matriz de Comparação"):
    # Geração da matriz de comparação de critérios
    matriz_criterios = gerar_matriz_comparacao(num_criterios)
    st.subheader("Matriz de Comparação dos Critérios")
    st.write(pd.DataFrame(matriz_criterios, index=criterios, columns=criterios))

    # Verificação de consistência
    lamb = np.sum(matriz_criterios, axis=1)
    consistencia = DadosSaaty(lamb, num_criterios)
    st.write("Resultado da Verificação de Consistência:")
    st.markdown(consistencia)

    if "Consistente" in consistencia:
        l, v = VV(matriz_criterios)
        st.write("Autovalor (l):", l)
        st.write("Autovetor (v):", ' '.join(map(str, v)))

        # Exibindo gráfico com o vetor de pesos
        plt.figure(figsize=(10, 4))
        plt.bar(criterios, v, color='lightblue')
        plt.title("Vetor de Peso dos Critérios")
        st.pyplot(plt)
