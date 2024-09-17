# 1° importa a biblioteca pandass

import sys
import streamlit as st
import numpy as np
import pandas as pd
from sklearn.preprocessing import Normalizer
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")
backgroundColor = "#ADD8E6"

# set page configuration
st.set_page_config(
page_title= "jAN",
layout="wide",
initial_sidebar_state="expanded",  # Pode ser "auto", "expanded" ou "collapsed"
)


html_temp = """
<img src="https://static-media.hotmart.com/d0IFT5pYRau6qyuHzfkd7_dgt6Q=/300x300/smart/filters:format(webp):background_color(white)/hotmart/product_pictures/686dcc4a-78b0-4b94-923b-c673a8ef5e75/Avatar.PNG" 
         alt="Descrição da imagem"
         style="width: 50px; height: 50px;">


<div style="text-align:center; background-color: #f0f0f0; border: 1px solid #ccc; padding: 10px;">
    <h3 style="color: black; margin-bottom: 10px;">Metodologia de apoio à decisão para manutenção inteligente, combinando abordagens multicritério</h3>
    <p style="color: black; margin-bottom: 10px;"">AHP - Xxxxxx 3</p>
    <p style="color: black; margin-bottom: 10px;"">Modo de uso: Aplique-o para escolha entre  quaisquer alternativas e critérios</p>
    <p style="color: black; margin-bottom: 10px;"">Todos os métodos funcionarão automaticamente</p>
    <p style="color: black; margin-bottom: 10px;"">Jaqueline Alves do Nascimento</p>
</div>

"""

st.markdown(html_temp, unsafe_allow_html=True)



#### Criando as funções matemáticas
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
        print('Inconsistente: %.2f' % cr)
    else:
        print('É Consistente: %.2f' % cr)

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
            print(f"O quão preferível o critério {names[i]} é em relação a {names[j]}:")
            value = float(input("Insira o valor de comparação (de 1 a 9): "))
            matrix[i][j] = value
            matrix[j][i] = 1 / value
    np.fill_diagonal(matrix, 1)  # Preencher a diagonal principal com 1
    return matrix
#### Encerrando as funções matemáticas

##### Criando as funções para o AHP
def exibir_tabela_comparacao_criterios(nomes, matriz):
    df = pd.DataFrame(matriz, index=nomes, columns=nomes)
    df = df.round(2)  # Arredondar para duas casas decimais
    print("\nTabela de Comparação dos Critérios:")
    print(df.to_string())

def exibir_tabela_comparacao_alternativas(nomes, matriz, criterio_nome):
    df = pd.DataFrame(matriz, index=nomes, columns=nomes)
    df = df.round(2)  # Arredondar para duas casas decimais
    print(f"\nTabela de Comparação das Alternativas para o critério '{criterio_nome}':")
    print(df.to_string())

def processar_matriz_alternativas(matriz, criterio_nome):
    # Normaliza a matriz
    normalizada = NormalizingConsistency(pd.DataFrame(matriz, columns=alternative_names, index=alternative_names))
    print(f"\nMatriz de comparação em pares das alternativas para o critério '{criterio_nome}' normalizada:")
    print(normalizada)

    # Teste de consistência
    print(f"\nTeste de consistência para o critério '{criterio_nome}':")
    Consistencia = normalizada.to_numpy()
    l, v = VV(Consistencia)
    print('Autovalor: %.2f' % l)
    print('Autovetor: ', np.round(v, 2))
    DadosSaaty(l, Consistencia.shape[0])

    # Vetor de peso
    peso = NormalizingCritera(pd.DataFrame(matriz, columns=alternative_names, index=alternative_names))
    print(f"\nVetor de peso para o critério '{criterio_nome}':")
    print(peso)

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

    print("\nMatriz de Priorização de todas as alternativas:")
    print(matrizPriorizacaoAlternativas)
    return matrizPriorizacaoAlternativas

##### Encerrando as funções para o AHP

##### Iniciando a matriz de peso dos criterios
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
             
        if st.button("Gerar Matriz de Comparação"):

            # Matriz de comparação par a par para critérios
            st.subheader("Insira as Comparações Par a Par para os Critérios:")
            matrix_criteria = get_comparison_matrix(num_criteria, criteria_names)
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
            DadosSaaty(l, Consistencia1.shape[0])

            # Código para obter dados, criar e normalizar matrizes, etc
            TabelaPesoDosCriterios = NormalizingCritera(desafioData)

            st.write("Vetor de Peso dos Critérios:")
            st.dataframe(TabelaPesoDosCriterios)

            # Gráfico de colunas dos valores normalizados dos critérios
            st.subheader("Gráfico de Peso dos Critérios")
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.set_title("Matriz de Peso dos Critérios", fontsize=20)

            # Plotando o gráfico com seaborn
            sns.barplot(x=TabelaPesoDosCriterios.index, y=TabelaPesoDosCriterios.values, ax=ax)

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
  

if __name__ == "__main__":
    main()

##### Finalizando a matriz de peso dos criterios
