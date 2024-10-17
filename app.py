Continue o código para aplicar a função a função numpy.dot() para char a soma do produto da coluna Importância(%) com as demais alternativas 




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
