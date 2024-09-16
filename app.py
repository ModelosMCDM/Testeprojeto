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
page_title= "TOTOTOTOTOO",
layout="wide",
initial_sidebar_state="expanded",  # Pode ser "auto", "expanded" ou "collapsed"
)


html_temp = """
<img src="https://www.casadamoeda.gov.br/portal/imgs/logo-cmb-4.png" 
         alt="Descrição da imagem"
         style="width: 250px; height: auto;">

<div style="text-align:center; background-color: #f0f0f0; border: 1px solid #ccc; padding: 10px;">
    <h3 style="color: black; margin-bottom: 10px;">Metodologia de apoio à decisão para manutenção inteligente, combinando abordagens multicritério</h3>
    <p style="color: black; margin-bottom: 10px;"">Projeto desenvolvido no Mestrado acadêmico em Engenharia de Produção | DEI - Departamento de Engenharia Industrial - 2023</p>
   
</div>

"""

st.markdown(html_temp, unsafe_allow_html=True)



# Criando as funções matemáticas
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


# Criando as funções para o AHP
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


def main():
    global desafioData, num_alternatives, alternative_names, num_criteria, criteria_names, desafioNormalAll  # Atribui a variável ao escopo global
    num_alternatives = int(input("Quantas alternativas você deseja avaliar? Inclua no mínimo 2 "))
    num_criteria = int(input("Quantos critérios você deseja usar na avaliação? "))

    # Nome dos critérios
    criteria_names = []
    for i in range(num_criteria):
        criteria_name = input(f"Informe o nome do critério {i + 1}: ")
        criteria_names.append(criteria_name)

    # Nome das alternativas
    alternative_names = []
    for i in range(num_alternatives):
        alternative_name = input(f"Informe o nome da alternativa {i + 1}: ")
        alternative_names.append(alternative_name)

    # Matriz de comparação par a par para critérios
    print("\nInsira as comparações par a par para os critérios:")
    matrix_criteria = get_comparison_matrix(num_criteria, criteria_names)
    desafioData = pd.DataFrame(matrix_criteria, index=criteria_names, columns=criteria_names)
    desafioData = desafioData.round(2)  # Arredondar para duas casas decimais

    print("\nMatriz de comparação em pares dos critérios:")
    print(desafioData)

    # Normaliza dados
    normalizandocriterio = NormalizingConsistency(desafioData)
    print("\nMatriz de comparação em pares dos critérios normalizada:")
    print(normalizandocriterio)

    # Teste de consistência
    print("\nTeste de consistência:")
    Consistencia1 = normalizandocriterio.to_numpy()
    l, v = VV(Consistencia1)
    print('Autovalor: %.2f' % l)
    print('Autovetor: ', np.round(v, 2))
    DadosSaaty(l, Consistencia1.shape[0])

    # Código para obter dados, criar e normalizar matrizes, etc
    TabelaPesoDosCriterios = NormalizingCritera(desafioData)
    desafioNormalAll.append(TabelaPesoDosCriterios)

    print("\nVetor de peso dos criterios:")
    print(TabelaPesoDosCriterios)

    # Gráfico de colunas dos valores normalizados dos critérios e MatrizdePeso
    plt.figure(figsize=(12, 6))  # largura e altura
    plt.title("Matriz de peso dos critérios", fontsize=20)

    # Plotando o gráfico com seaborn
    ax = sns.barplot(x=TabelaPesoDosCriterios.index, y='MatrizdePeso', data=TabelaPesoDosCriterios, legend=False)

    # Adicionando rótulos às barras
    for p in ax.patches:
        height = p.get_height()
        ax.text(p.get_x() + p.get_width() / 2, height, '{:.2f}'.format(height),
                ha='center', va='bottom', fontsize=10)

    plt.xlabel('Critérios', fontsize=12)
    plt.ylabel('Pesos', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()

15# Matriz de comparação par a par para alternativas para cada critério
alternativas_por_criterio = {}  # Dicionário para armazenar as tabelas
for i in range(num_criteria):
    criterio_nome = criteria_names[i]
    print(f"\nInsira a matriz de priorizações par a par de cada alternativa para o critério {i + 1} ({criterio_nome}):")
    DadosCriterio = get_comparison_matrix(num_alternatives, alternative_names)
    exibir_tabela_comparacao_alternativas(alternative_names, DadosCriterio, criterio_nome)
    # Processar a matriz de alternativas
    peso_criterio = processar_matriz_alternativas(DadosCriterio, criterio_nome)
    desafioNormalAll.append(peso_criterio)

# Finalizando a Matriz de Priorização de todas alternativas
matrizPriorizacaoAlternativas = finalizar_matriz_priorizacao_alternativas(desafioNormalAll, criteria_names, alternative_names)

# Calculando a soma ponderada para cada coluna (alternativa)
peso_dos_criterios = matrizPriorizacaoAlternativas['Peso dos Critérios'].values
soma_ponderada = {}

for alternativa in alternative_names:
    soma_ponderada[alternativa] = np.sum(matrizPriorizacaoAlternativas[alternativa].values * peso_dos_criterios)

# Adicionando a linha "soma" ao DataFrame
soma_ponderada_series = pd.Series(soma_ponderada, name='soma')
matrizPriorizacaoAlternativas = pd.concat([matrizPriorizacaoAlternativas, soma_ponderada_series.to_frame().T])

# Excluindo a coluna "Peso dos Critérios"
matrizPriorizacaoAlternativas = matrizPriorizacaoAlternativas.drop(columns=['Peso dos Critérios'])


# Exibindo a matriz atualizada
print(matrizPriorizacaoAlternativas)


#Descobrindo o tipo da variável
print(type(matrizPriorizacaoAlternativas))

# Convertendo a matriz para um array NumPy
matriz_np = np.array(matrizPriorizacaoAlternativas)

# Convertendo o array NumPy para um DataFrame
matriz_df = pd.DataFrame(matriz_np, columns=matrizPriorizacaoAlternativas.columns, index=matrizPriorizacaoAlternativas.index)

# Função para formatar valores com vírgulas
def format_with_comma(value):
    return f"{value:.6f}".replace('.', ',')

# Aplicando a formatação ao DataFrame
matriz_df_formatted = matriz_df.applymap(format_with_comma)

# Imprimindo o DataFrame final
print(matriz_df_formatted)

# Extraindo a última linha do DataFrame
ultima_linha = matriz_df_formatted.iloc[-1]

# Classificando os valores da última linha
ranking = ultima_linha.rank(ascending=False, method='min').astype(int)

# Transformando o ranking em um DataFrame
ranking_matriz_df_formatted = ranking.reset_index()
ranking_matriz_df_formatted.columns = ['Coluna', 'Ranking']
ranking_matriz_df_formatted = ranking_matriz_df_formatted.sort_values(by='Ranking')

print(ranking_matriz_df_formatted)

# prompt: ajuste para aparecer no ranking_matriz_df_formatted a coluna com o valor de ultima_linha ao lado na coluna Ranking

ranking_matriz_df_formatted['Valor'] = ultima_linha.values
print(ranking_matriz_df_formatted)

st.caption("Desenvolvido pela empregada Jaqueline Alves do Nascimento")
