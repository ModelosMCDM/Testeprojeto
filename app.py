import sys
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="darkgrid")
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
    <p style="color: black; margin-bottom: 10px;"">Código fonte, devidamente patenteado no INPI </p>
    <p style="color: black; margin-bottom: 10px;"">Todos os cálculos dos métodos irão funcionar automaticamente</p>
</div>

"""

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

#Para o calculo do grafico
def calcular_importancia(df_normalizada):
    # Calcula o total das linhas
    total_linhas = df_normalizada.sum(axis=1)
    
    # Calcula a importância percentual de cada critério
    importancia = (total_linhas / total_linhas.sum()) * 100
    
    # Adiciona as novas colunas na matriz
    df_normalizada['Total das Linhas'] = total_linhas
    df_normalizada['Importância (%)'] = importancia
    
    return df_normalizada

# Adicionando estilo customizado para o campo de entrada
st.markdown(
    """
    <style>
    /* Estilizando o campo de entrada de texto */
    .stTextInput > div > div > input {
        background-color: #F0F8FF; /* Cor de fundo do campo de texto */
        color: #000000; /* Cor do texto inserido */
    }
    </style>
    """,
    unsafe_allow_html=True
)

#######INICIO#####
st.markdown(html_temp, unsafe_allow_html=True)

# Pergunta ao usuário o número de critérios e alternativas
st.markdown("<h3 style='text-align: center; background-color: #6495ED;'> Estrutura hierárquica </h3>", unsafe_allow_html=True)

st.subheader("1 - Alimentando o sistema")

# Exibindo o texto em negrito acima do campo de entrada
st.markdown("<strong>Inicie informando qual a decisão a ser tomada</strong>", unsafe_allow_html=True)
titulo_pesquisa = st.text_input("Digite aqui o título da pesquisa")


num_alternativas = st.number_input("Quantas alternativas serão analisadas?", min_value=2, step=1)
st.write(f"Você selecionou {num_alternativas} alternativas.")

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
    st.markdown("Matriz de comparação dos pesos gerada", unsafe_allow_html=True)
    df_matriz_comparacao = pd.DataFrame(matriz_comparacao_criterios, index=criterios, columns=criterios)
    st.write(df_matriz_comparacao)

    # Normalizando a matriz de comparação
    #st.subheader("1.1 - Normalizando a Matriz de Comparação")
    normalizada = NormalizingConsistency(df_matriz_comparacao)
    #st.write(normalizada)

    # Fazer uma cópia da matriz normalizada para uso posterior
    normalizada_copia = normalizada.copy()

        # Aplicando a função na matriz normalizada
    df_com_importancia = calcular_importancia(normalizada_copia)

    # Exibindo a nova matriz com as colunas adicionais
    st.subheader("1.2 - Matriz normalizada com somatório dos pesos e Grau de Importância de Cada Critério - Matriz de Pesos")
    st.write(df_com_importancia)

    # Tamanho da figura
    plt.figure(figsize=(27, 8))
    ax = sns.barplot(x=df_com_importancia.index, y=df_com_importancia['Importância (%)'], palette="Spectral")
    plt.title("Importância de Cada Critério", fontsize=36, pad=45)

    ax.set_xlabel("Critérios", fontsize=18)
    ax.set_ylabel("Importância (%)", fontsize=18)

    # Ajustando o tamanho dos rótulos dos eixos
    ax.tick_params(axis='x', labelsize=30)
    ax.tick_params(axis='y', labelsize=30)

    # Exibindo os valores de importância no topo de cada barra
    for p in ax.patches:
        height = p.get_height()
        ax.text(p.get_x() + p.get_width() / 2., height + 0.5, '{:1.2f}'.format(height), ha="center", fontsize=34)
    
    # Exibir o gráfico
    st.pyplot(plt) 

    
    # Cálculo de consistência
    st.subheader("1.3 - Verificação de Consistência")
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

#################aqui
# Pergunta ao usuário as comparações para as alternativas
st.subheader("2. Comparação das Alternativas - Preencha a matriz de priorização")

# Lista para armazenar o peso final de cada alternativa para cada critério
pesos_finais_por_criterio = pd.DataFrame()

try:
    # Criação da matriz de resultados para todas as alternativas ponderadas pelos critérios
    resultados_alternativas = np.zeros((num_alternativas, num_criterios))

    # Coleta comparações de preferências entre as alternativas para cada critério
    for crit_index, crit in enumerate(criterios):
        st.write(f"Comparação de alternativas para o critério: {crit}")
        matriz_alternativas = np.ones((num_alternativas, num_alternativas))  # A diagonal principal é sempre 1 (comparação do critério com ele mesmo)

        for i in range(num_alternativas):
            for j in range(i + 1, num_alternativas):
                valor_alternativa = st.number_input(f"O quão preferível é {alternativas[i]} em relação à {alternativas[j]} para o critério {crit} (escala 1-9)", min_value=1, max_value=9)
                matriz_alternativas[i, j] = valor_alternativa
                matriz_alternativas[j, i] = 1 / valor_alternativa  # Simetria inversa

        # Exibe a matriz de comparação
        df_matriz_alternativas = pd.DataFrame(matriz_alternativas, index=alternativas, columns=alternativas)
        st.write(f"Matriz de Comparação para o Critério {crit}")
        st.write(df_matriz_alternativas)

        # Normalizar a matriz de alternativas
        normalizada_alternativas = NormalizingConsistency(df_matriz_alternativas)  # Normaliza e verifica consistência
        
        # Calcular a média dos valores dos critérios para cada alternativa
        normalizada_alternativas['Peso Final'] = normalizada_alternativas.mean(axis=1)
        
        # Exibir a matriz com a nova coluna de médias
        st.write(f"Matriz Normalizada para o Critério {crit} com a coluna de médias")
        st.write(normalizada_alternativas)
        
        # Armazenar os pesos finais de cada critério em um DataFrame
        pesos_finais_por_criterio[crit] = normalizada_alternativas['Peso Final']

        # Cálculo dos pesos das alternativas para este critério
        _, pesos_alternativas = VV(normalizada_alternativas.drop(columns=['Peso Final']).to_numpy())

        # Armazenar os pesos das alternativas ponderados pelo peso do critério
        resultados_alternativas[:, crit_index] = pesos_alternativas * v[crit_index]
        
        # Cálculo dos pesos finais (somatório das alternativas ponderadas pelos critérios)
        pesos_finais = np.sum(resultados_alternativas, axis=1)
        
        # Adicionar apenas a coluna 'Peso Final' ao DataFrame final de resultados
        df_resultado = pd.DataFrame(normalizada_alternativas['Peso Final'], index=alternativas, columns=["Peso Final"])
        
        # Exibir o DataFrame final apenas com a coluna de médias dos critérios
        st.write(df_resultado)

    # Criar uma cópia de df_com_importancia apenas com a coluna "Importância (%)"
    df_priorizacao_alternativas = df_com_importancia[['Importância (%)']].copy()

    # Adicionar ao df_priorizacao_alternativas as colunas das alternativas com os valores de Peso Final de cada critério
    for alt in alternativas:
        df_priorizacao_alternativas[alt] = pesos_finais_por_criterio.loc[alt]

    # Exibir o DataFrame final atualizado
    st.write("Matriz Final com as Alternativas e Pesos Finais")
    st.write(df_priorizacao_alternativas)
    
except Exception as e:
    st.error(f"Ocorreu um erro: {e}")
    #######AQUI
    # Função para aplicar o equivalente a SOMARPRODUTO
    def somarproduto(df):
        # Multiplica a coluna "Importância (%)" por cada coluna de alternativa
        return (df['Importância (%)'].values[:, np.newaxis] * df.drop(columns=['Importância (%)']).values).sum(axis=0)
    
    # Criar uma cópia de df_priorizacao_alternativas apenas com a coluna "Importância (%)" e as alternativas
    df_priorizacao_alternativas = df_com_importancia[['Importância (%)']].copy()
    
    # Adicionar ao df_priorizacao_alternativas as colunas das alternativas com os valores de Peso Final de cada critério
    for alt in alternativas:
        df_priorizacao_alternativas[alt] = pesos_finais_por_criterio.loc[alt]
    
    # Aplica a função de somar produto para calcular o peso final de cada alternativa
    pesos_finais_alternativas = somarproduto(df_priorizacao_alternativas)
    
    # Exibir o DataFrame final atualizado com os pesos finais
    df_resultado_final = pd.DataFrame(pesos_finais_alternativas, index=alternativas, columns=["Peso Final"])
    st.write("Matriz Final com os Pesos Finais das Alternativas")
    st.write(df_resultado_final)



   #######AQUI
    
    # Resultado final - gráfico
    st.subheader("4. Resultado final")
    st.subheader("produto da matriz de peso e matriz dos critérios")
    plt.figure(figsize=(27,8))  # largura e altura
    plt.title(f"Ranking para problema de: {titulo_pesquisa}", fontsize=36, pad=45)
    ax = sns.barplot(x=df_resultado.index, y=df_resultado["Peso Final"], data=df_resultado, palette="viridis")

    # Aumentando o tamanho das legendas dos eixos
    ax.set_ylabel("Peso Final", fontsize=30)  # Tamanho da fonte do eixo Y
    ax.tick_params(axis='x', labelsize=30)  # Tamanho da fonte para os rótulos do eixo X
    ax.tick_params(axis='y', labelsize=30)  # Tamanho da fonte para os rótulos do eixo Y

    for p in ax.patches:
        height = p.get_height()
        ax.text(p.get_x() + p.get_width() / 2, height + 0.01, '{:1.2f}'.format(height), ha='center', fontsize=34)

    st.pyplot(plt)

except Exception as e:
    st.error(f"Ocorreu um erro ao processar as comparações de alternativas: {e}")

