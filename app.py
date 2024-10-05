import sys
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")
backgroundColor = "#ADD8E6"

# Configuração inicial da página
st.set_page_config(
    page_title="JACKE",
    layout="wide",
    initial_sidebar_state="expanded",
)

html_temp = """
<img src="https://www.casadamoeda.gov.br/portal/imgs/logo-cmb-4.png" 
         alt="Descrição da imagem"
         style="width: 250px; height: auto;">

<div style="text-align:center; background-color: #f0f0f0; border: 1px solid #ccc; padding: 10px;">
    <h3 style="color: black; margin-bottom: 10px;">Metodologia de apoio à decisão </h3>
    <p style="color: black; margin-bottom: 10px;"">Modo de uso: Digite a quantidade de alternativas e critérios que você usará para a tomada de decisão. Em seguida, preencha as opções conforme necessário </p>
    <p style="color: black; margin-bottom: 10px;"">Com base na métodologia de Thomas Saaty - Por Jaqueline Alves </p>
    <p style="color: black; margin-bottom: 10px;"">Todos os cálculos dos métodos irão funcionar automaticamente</p>
</div>

"""
st.markdown(html_temp, unsafe_allow_html=True)

# Calculando o total das linhas e a importância de cada critério
def calcular_importancia(df_normalizada):
    # Calcula o total das linhas
    total_linhas = df_normalizada.sum(axis=1)
    
    # Calcula a importância percentual de cada critério
    importancia = (total_linhas / total_linhas.sum()) * 100
    
    # Adiciona as novas colunas na matriz
    df_normalizada['Total das Linhas'] = total_linhas
    df_normalizada['Importância (%)'] = importancia
    
    return df_normalizada
    
# Função de consistência de Saaty
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

# Função para normalizar a matriz de consistência
def NormalizingConsistency(dataP):
    resultP = dataP.copy()
    for col in resultP.columns:
        resultP[col] = resultP[col] / sum(resultP[col])
    return resultP

# PerguntaNndo ao usuário o número de critérios e alternativas

st.markdown("<h3 style='text-align: center; background-color: #6495ED;'> Estrutura hierárquica </h3>", unsafe_allow_html=True)


# Exibindo o texto em negrito acima do campo de entrada
st.markdown("<strong>Inicie informando qual a decisão a ser tomada</strong>", unsafe_allow_html=True)
titulo_pesquisa = st.text_input("Digite aqui o título da pesquisa")

num_alternativas = st.number_input("Quantas alternativas serão analisadas?", min_value=2, step=1)
alternativas = []
for i in range(num_alternativas):
    alternativa = st.text_input(f"Informe o nome da alternativa {i + 1}:")
    alternativas.append(alternativa)

num_criterios = st.number_input("Quantos critérios serão utilizados?", min_value=2, step=1)
criterios = []
for i in range(num_criterios):
    criterio = st.text_input(f"Informe o nome do critério {i + 1}:")
    criterios.append(criterio)

# Verificar se todos os critérios e alternativas foram preenchidos
if any(criterio == '' for criterio in criterios):
    st.error("Por favor, preencha todos os critérios.")
elif any(alternativa == '' for alternativa in alternativas):
    st.error("Por favor, preencha todas as alternativas.")
else:
    # Gerar matriz de comparação dos critérios
    st.subheader("1.1 - Matriz de Comparação dos Critérios")
    matriz_comparacao_criterios = np.ones((num_criterios, num_criterios))

    # Entrada dos valores de comparação
    for i in range(num_criterios):
        for j in range(i + 1, num_criterios):
            valor_comparacao = st.number_input(f"Para você, o quanto o critério {criterios[i]} é mais importante que  {criterios[j]} (escala 1-9)", min_value=1, max_value=9)
            matriz_comparacao_criterios[i, j] = valor_comparacao
            matriz_comparacao_criterios[j, i] = 1 / valor_comparacao

    # Exibir a matriz gerada
    df_matriz_comparacao = pd.DataFrame(matriz_comparacao_criterios, index=criterios, columns=criterios)
    st.write(df_matriz_comparacao)

    # Normalizando a matriz de comparação
    st.subheader("1.2 - Normalizando a Matriz de Comparação")
    normalizada = NormalizingConsistency(df_matriz_comparacao)
    st.write(normalizada)

    # Aplicando a função na matriz normalizada
    df_com_importancia = calcular_importancia(normalizada)

    # Exibindo a nova matriz com as colunas adicionais
    st.subheader("1.3 - Matriz com Total das Linhas e Importância de Cada Critério")
    st.write(df_com_importancia)


    # Cálculo de consistência
    st.subheader("1.4 - Verificação de Consistência")
    array_ahp = normalizada.to_numpy()
    N = len(array_ahp)
    lamb = np.sum(array_ahp, axis=1)
    resultado_consistencia = DadosSaaty(lamb, N)
    st.markdown(f"**Resultado da Verificação de Consistência:** {resultado_consistencia}")

    # Se for consistente, calcular o vetor de pesos (autovalores e autovetores)
    if "Consistente" in resultado_consistencia:
        l, v = VV(array_ahp)
        st.write("Autovalor (l):", l)
        st.write("Autovetor (v):", ' '.join(map(str, v)))

    # Pergunta ao usuário as comparações para as alternativas
    st.subheader("2. Comparação das Alternativas")

    try:
        # Criação da matriz de resultados para todas as alternativas ponderadas pelos critérios
        resultados_alternativas = np.zeros((num_alternativas, num_criterios))

        # Coleta comparações de preferências entre as alternativas para cada critério
        for crit_index, crit in enumerate(criterios):
            st.write(f"Comparação de alternativas para o critério: {crit}")
            matriz_alternativas = np.ones((num_alternativas, num_alternativas))

            for i in range(num_alternativas):
                for j in range(i + 1, num_alternativas):
                    valor_alternativa = st.number_input(f"O quão preferível é {alternativas[i]} é em relação à {alternativas[j]} para o critério {crit} (escala 1-9)", min_value=1, max_value=9)
                    matriz_alternativas[i, j] = valor_alternativa
                    matriz_alternativas[j, i] = 1 / valor_alternativa

            # Normalizar a matriz de alternativas
            df_matriz_alternativas = pd.DataFrame(matriz_alternativas, index=alternativas, columns=alternativas)
            normalizada_alternativas = NormalizingConsistency(df_matriz_alternativas)
            st.write(normalizada_alternativas)

            # Cálculo dos pesos das alternativas para este critério
            _, pesos_alternativas = VV(normalizada_alternativas.to_numpy())

            # Armazenar os pesos das alternativas ponderados pelo peso do critério
            resultados_alternativas[:, crit_index] = pesos_alternativas * v[crit_index]

        # Cálculo dos pesos finais (somatório das alternativas ponderadas pelos critérios)
        pesos_finais = np.sum(resultados_alternativas, axis=1)
        df_resultado = pd.DataFrame(pesos_finais, index=alternativas, columns=["Peso Final"])
        st.write(df_resultado)

       # Resultado final
        st.subheader("4. Resultado final")
        plt.figure(figsize=(27,8))  # largura e altura
        plt.title(titulo_pesquisa, fontsize=36, pad=40)
        ax = sns.barplot(x=df_resultado.index, y=df_resultado["Peso Final"], data=df_resultado, palette="viridis")

        # Aumentando o tamanho das legendas dos eixos
        # ax.set_xlabel("Alternativas", fontsize=18)  # Tamanho da fonte do eixo X
        ax.set_ylabel("Peso Final", fontsize=30)  # Tamanho da fonte do eixo Y
        # Aumentar o tamanho da fonte das legendas dos eixos
        ax.tick_params(axis='x', labelsize=30)  # Tamanho da fonte para os rótulos do eixo X
        ax.tick_params(axis='y', labelsize=30)  # Tamanho da fonte para os rótulos do eixo Y

        for p in ax.patches:
            height = p.get_height()
            ax.text(p.get_x() + p.get_width() / 2, height + 0.01, '{:1.2f}'.format(height), ha='center', fontsize=34)

        st.pyplot(plt)  

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar as comparações de alternativas: {e}")
