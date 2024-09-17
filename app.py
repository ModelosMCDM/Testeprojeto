import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")

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
    return cr

def VV(Consistencia):
    l, v = np.linalg.eig(Consistencia)
    v = v.T
    i = np.where(l == np.max(l))[0][0]
    l = l[i]
    v = v[i]
    v = v / np.sum(v)
    return np.real(l), np.real(v)

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

html_temp = """
<img src="https://static-media.hotmart.com/d0IFT5pYRau6qyuHzfkd7_dgt6Q=/300x300/smart/filters:format(webp):background_color(white)/hotmart/product_pictures/686dcc4a-78b0-4b94-923b-c673a8ef5e75/Avatar.PNG" 
         alt="Descrição da imagem"
         style="width: 50px; height: 50px;">
<div style="text-align:center; background-color: #f0f0f0; border: 1px solid #ccc; padding: 10px;">
    <h3 style="color: black; margin-bottom: 10px;">Metodologia de apoio à decisão para manutenção inteligente, combinando abordagens multicritério</h3>
    <p style="color: black; margin-bottom: 10px;">AHP - Xxxxxx 3</p>
    <p style="color: black; margin-bottom: 10px;">Modo de uso: Aplique-o para escolha entre quaisquer alternativas e critérios</p>
    <p style="color: black; margin-bottom: 10px;">Todos os métodos funcionarão automaticamente</p>
    <p style="color: black; margin-bottom: 10px;">Jaqueline Alves do Nascimento</p>
</div>
"""
st.markdown(html_temp, unsafe_allow_html=True)

def main():
    st.title("Avaliação de Alternativas")

    # Solicitar o número de alternativas e critérios do usuário
    num_alternatives = st.number_input("Quantas alternativas você deseja avaliar? Inclua no mínimo 2", min_value=2, step=1)
    num_criteria = st.number_input("Quantos critérios você deseja usar na avaliação?", min_value=1, step=1)

    if num_criteria > 0 and num_alternatives > 0:
        # Coletar nomes das alternativas
        st.subheader("Nome das Alternativas")
        alternative_names = [st.text_input(f"Informe o nome da alternativa {i + 1}", key=f"alternative_{i}") for i in range(num_alternatives)]

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
                if st.button("Calcular Matriz de Comparação"):
                    # Matriz de comparação par a par para critérios
                    matrix_criteria = get_comparison_matrix(num_criteria, criteria_names, values)
                    desafioData = pd.DataFrame(matrix_criteria, index=criteria_names, columns=criteria_names)
                    desafioData = desafioData.round(2)  # Arredondar para duas casas decimais

                    st.write("Matriz de Comparação em Pares dos Critérios:")
                    st.dataframe(desafioData)

                    # Normaliza dados
                    normalizandocriterio = NormalizingConsistency(desafioData)
                    st.write("Matriz de Comparação em Pares dos Critérios Normalizada:")
                    st.dataframe(normalizandocriterio)

                    # Teste de consistência
                    Consistencia1 = normalizandocriterio.to_numpy()
                    l, v = VV(Consistencia1)
                    st.write(f'Autovalor: {l:.2f}')
                    st.write(f'Autovetor: {np.round(v, 2)}')
                    cr = DadosSaaty(l, Consistencia1.shape[0])
                    st.write(f'Teste de Consistência: {"Inconsistente" if cr > 0.1 else "Consistente"} (CR: {cr:.2f})')

                    # Código para obter dados, criar e normalizar matrizes, etc
                    TabelaPesoDosCriterios = NormalizingCritera(desafioData)

                    st.write("Vetor de Peso dos Critérios:")
                    st.dataframe(TabelaPesoDosCriterios)

                    # Gráfico de colunas dos valores normalizados dos critérios
                    st.subheader("Gráfico de Peso dos Critérios")
                    fig, ax = plt.subplots(figsize=(12, 6))
                    ax.set_title("Matriz de Peso dos Critérios", fontsize=20)

                    # Plotando o gráfico com seaborn
                    sns.barplot(x=TabelaPesoDosCriterios.index, y=TabelaPesoDosCriterios['MatrizdePeso'], ax=ax)

                    # Adicionando rótulos às barras
                    for p in ax.patches:
                        height = p.get_height()
                        ax.text(p.get_x() + p.get_width() / 2, height, '{:.2f}'.format(height),
                                ha='center', va='bottom', fontsize=10)

                    ax.set_xlabel('Critérios', fontsize=12)
                    ax.set_ylabel('Pesos', fontsize=12)
                    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=12)
                    ax.tick_params(axis='y', labelsize=12)
                    plt.tight_layout()

                    st.pyplot(fig)
            else:
                st.warning("Por favor, preencha todos os campos de comparação.")

if __name__ == "__main__":
    main()
