# Continuação do código principal
                    st.pyplot(plt.gcf())

                    # Comparação par a par das alternativas para cada critério
                    desafioNormalAll = [{'MatrizdePeso': TabelaPesoDosCriterios['MatrizdePeso']}]
                    
                    for crit in criteria_names:
                        st.subheader(f"Matriz de Comparação das Alternativas para o Critério {crit}:")
                        matrix_alternatives = get_comparison_matrix(num_alternatives, alternative_names, f"matrix_alternatives_{crit}")
                        df_alternatives = pd.DataFrame(matrix_alternatives, index=alternative_names, columns=alternative_names)
                        
                        # Normalização e cálculo do peso para as alternativas por critério
                        normalizandoAlternativas = NormalizingConsistency(df_alternatives)
                        st.write(f"Matriz de Comparação Normalizada das Alternativas para o Critério {crit}:")
                        st.write(normalizandoAlternativas)
                        l, v = VV(normalizandoAlternativas.to_numpy())
                        cr_alt = DadosSaaty(l, normalizandoAlternativas.shape[0])
                        st.write(f"Índice de Consistência para {crit}: {cr_alt:.2f}")
                        if cr_alt > 0.1:
                            st.warning(f"A matriz de alternativas para o critério {crit} é inconsistente!")
                        else:
                            st.success(f"A matriz de alternativas para o critério {crit} é consistente!")
                        
                        # Calculando o peso das alternativas para o critério específico
                        TabelaPesoDasAlternativas = NormalizingCritera(df_alternatives)
                        desafioNormalAll.append({'MatrizdePeso': TabelaPesoDasAlternativas['MatrizdePeso']})
                        st.write(f"Vetor de Peso das Alternativas para o Critério {crit}:")
                        st.write(TabelaPesoDasAlternativas)
                        
                        # Gráfico do peso das alternativas para cada critério
                        st.subheader(f"Gráfico de Peso das Alternativas para o Critério {crit}")
                        plt.figure(figsize=(10, 5))
                        ax = sns.barplot(x=TabelaPesoDasAlternativas.index, y=TabelaPesoDasAlternativas['MatrizdePeso'])
                        plt.xticks(rotation=45)
                        st.pyplot(plt.gcf())

                    # Gerando a matriz de priorização final para todas as alternativas
                    st.subheader("Matriz de Priorização de Todas as Alternativas")
                    matrizPriorizacaoAlternativas = finalizar_matriz_priorizacao_alternativas(desafioNormalAll, criteria_names, alternative_names)
                    st.write(matrizPriorizacaoAlternativas)

if __name__ == "__main__":
    main()
