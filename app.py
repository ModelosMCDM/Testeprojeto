import streamlit as st
import numpy as np
import pandas as pd

# Função para gerar a matriz de comparação
def get_comparison_matrix(num_criteria, names, values):
    matrix = np.zeros((num_criteria, num_criteria))
    idx = 0
    for i in range(num_criteria):
        for j in range(i + 1, num_criteria):
            value = float(values[idx])
            matrix[i][j] = value
            matrix[j][i] = 1 / value
            idx += 1
    np.fill_diagonal(matrix, 1)  # Preencher a diagonal principal com 1
    return matrix

# Configuração da página
st.set_page_config(page_title="Avaliação de Alternativas", layout="wide", initial_sidebar_state="expanded")

def main():
    st.title("Avaliação de Alternativas")

    # Solicitar o número de critérios
    num_criteria = st.number_input("Quantos critérios você deseja usar na avaliação?", min_value=1, step=1)

    if num_criteria > 0:
        # Coletar nomes dos critérios
        st.subheader("Nome dos Critérios")
        criteria_names = [st.text_input(f"Informe o nome do critério {i + 1}", key=f"criteria_{i}") for i in range(num_criteria)]

        if st.button("Gerar Matriz de Comparação dos Critérios"):
            # Coletar comparações par a par
            st.subheader("Insira as Comparações Par a Par para os Critérios:")
            values = []
            for i in range(num_criteria):
                for j in range(i + 1, num_criteria):
                    value = st.number_input(f"Comparação entre {criteria_names[i]} e {criteria_names[j]}", min_value=1.0, step=0.1, key=f"pair_{i}_{j}")
                    values.append(value)

            # Verificar se todos os campos foram preenchidos
            if len(values) == (num_criteria * (num_criteria - 1) // 2):
                # Matriz de comparação par a par para critérios
                matrix_criteria = get_comparison_matrix(num_criteria, criteria_names, values)
                matriz_df = pd.DataFrame(matrix_criteria, index=criteria_names, columns=criteria_names)

                # Exibir a matriz
                st.write("Matriz de Comparação em Pares dos Critérios:")
                st.dataframe(matriz_df)

                # Ou exibir de forma mais parecida com a imagem:
                st.write(matriz_df.to_string(index=True))
            else:
                st.warning("Por favor, preencha todos os campos de comparação.")

if __name__ == "__main__":
    main()
