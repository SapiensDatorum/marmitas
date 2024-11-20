#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 21:33:50 2024

@author: rogerio

Os arquivos originais (XLSX) fornecidos são lidos um a um para compor todas as
doações que foram realizadas desde o ínicio do projeto
Nenhum dado foi alterado, criado ou substituído
 
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# módulo para converter um dataframe em tabela para banco de dados relacinais
import dataframe_to_sqltable as dftosql 


# importando o dataframe de custos
#from script_custos import df_custos_alimentacao_agrupado

# Caminho do arquivo .xlsx
file_path = '/home/rogerio/Documentos/ASN.Rocks/Projeto Marmitas/DADOS_MARMITAS_EM_ACAO/Extrato_31'
file_type = '.xlsx'
# Ler as planilhas uma a uma para um DataFrame

df_doacoes = pd.DataFrame()  # Inicializa um DataFrame vazio

for j in range(2021, 2025):
    for i in range(1, 13):
        numero_formatado = "{:02d}".format(i)
        item = f"{file_path}_{numero_formatado}_{j}{file_type}"
            
        if (j == 2024 and i >= 10) or (j == 2021 and i < 5):
            print("nao processo")
            print(i, j)
        else:
            df = pd.read_excel(item)
            
            # Adiciona o mes e ano do arquivo para encontrar o problema
            df['mes_arq'] = i
            df['ano_arq'] = j
                        
            print(i, j)
            df_doacoes = pd.concat([df_doacoes, df], ignore_index=True)


"""

Campo Data nos arquivos xlsx não estão com o mesmo formato
==========================================================

Datas na coluna com diferentes formatos, a coluna de data não será utilizada
e a data de referência que será utilizada será pelo nome do arquivo

A linha abaixo deverá ser reescrita para criar a data como 01 + mes_arq + ano_arq 
como string e depois convertida em data.

"""
# Criar a coluna 'Data' a partir de 'mes_arq' e 'ano_arq'
df_doacoes['Data'] = pd.to_datetime('01-' + df_doacoes['mes_arq'].astype(str) + '-' + df_doacoes['ano_arq'].astype(str), format='%d-%m-%Y', errors='coerce')

# cria script sql da tabela doações
dftosql.cria_tabela_sql(df_doacoes, 'doacoes')

# boxplot dos valores das doações
#################################
# Calcular as estatísticas básicas
media = df_doacoes['Valor'].mean()
mediana = df_doacoes['Valor'].median()
moda = df_doacoes['Valor'].mode()
percentis = np.percentile(df_doacoes['Valor'], [25, 75])

# Criando o boxplot com escala logarítmica no eixo y
plt.figure(figsize=(8, 6))
plt.boxplot(df_doacoes['Valor'])
plt.yscale('log')  # Aplica a escala logarítmica no eixo y

# Adicionar as estatísticas no gráfico
plt.text(1.1, media, f"Média: {media:.2f}", verticalalignment='center', color='blue')
plt.text(1.1, mediana, f"Mediana: {mediana:.2f}", verticalalignment='center', color='green')
plt.text(1.1, percentis[0], f"25º percentil: {percentis[0]:.2f}", verticalalignment='center', color='purple')
plt.text(1.1, percentis[1], f"75º percentil: {percentis[1]:.2f}", verticalalignment='center', color='purple')

# Exibir o gráfico
plt.title('Distribuição de Valores das Doações')
plt.show()

# histograa dos valores das doações
###################################
plt.hist(df_doacoes['Valor'],50)
plt.yscale('log')  # Aplica a escala logarítmica no eixo y
plt.xscale('log')
plt.show()


# número de doadores distintos
num_doadores_unicos = df_doacoes['ID'].nunique()

# Frequência de doações e valor total doado por doador
df_tot_doacao_freq_por_doador = df_doacoes.groupby('ID').agg(
    total_doado=('Valor', 'sum'),
    contagem_doacoes=('Valor', 'count')
).reset_index()

# boxplot dos valores totais das doações por doador
###################################################
# Calcular as estatísticas básicas df_tot_doacao_freq_por_doador
media = df_tot_doacao_freq_por_doador['total_doado'].mean()
mediana = df_tot_doacao_freq_por_doador['total_doado'].median()
moda = df_tot_doacao_freq_por_doador['total_doado'].mode()
percentis = np.percentile(df_tot_doacao_freq_por_doador['total_doado'], [25, 75])

# Criando o boxplot com escala logarítmica no eixo y
plt.figure(figsize=(8, 6))
plt.boxplot(df_tot_doacao_freq_por_doador['total_doado'])
plt.yscale('log')  # Aplica a escala logarítmica no eixo y

# Adicionar as estatísticas no gráfico
plt.text(1.1, media, f"Média: {media:.2f}", verticalalignment='center', color='blue')
plt.text(1.1, mediana, f"Mediana: {mediana:.2f}", verticalalignment='center', color='green')
plt.text(1.1, percentis[0], f"25º percentil: {percentis[0]:.2f}", verticalalignment='center', color='purple')
plt.text(1.1, percentis[1], f"75º percentil: {percentis[1]:.2f}", verticalalignment='center', color='purple')

# Exibir o gráfico
plt.title('Distribuição dos Valores totais das Doações por Doador')
plt.show()

# boxplot das frequencias das doações por doador
################################################
# Calcular as estatísticas básicas df_tot_doacao_freq_por_doador
media = df_tot_doacao_freq_por_doador['contagem_doacoes'].mean()
mediana = df_tot_doacao_freq_por_doador['contagem_doacoes'].median()
moda = df_tot_doacao_freq_por_doador['contagem_doacoes'].mode()
percentis = np.percentile(df_tot_doacao_freq_por_doador['contagem_doacoes'], [25, 75])

# Criando o boxplot
plt.figure(figsize=(8, 6))
plt.boxplot(df_tot_doacao_freq_por_doador['contagem_doacoes'])
#plt.yscale('log')  # Aplica a escala logarítmica no eixo y

# Adicionar as estatísticas no gráfico
plt.text(1.1, media, f"Média: {media:.2f}", verticalalignment='center', color='blue')
plt.text(1.1, mediana, f"Mediana: {mediana:.2f}", verticalalignment='center', color='green')
plt.text(1.1, percentis[0], f"25º percentil: {percentis[0]:.2f}", verticalalignment='center', color='purple')
plt.text(1.1, percentis[1], f"75º percentil: {percentis[1]:.2f}", verticalalignment='center', color='purple')

# Exibir o gráfico
plt.title('Distribuição das Frequencias de Doações por Doador')
plt.show()

# gráfico de densidade de doações por doador
# histograa dos valores das doações
############################################
plt.title('Densidade de Doações por Doadores')
plt.hist(df_tot_doacao_freq_por_doador['contagem_doacoes'])
# Adicionando nomes aos eixos
plt.xlabel('Frequência de Doações')
plt.ylabel('Número de Doadores')
plt.grid(True)
plt.show()

# gráfico de densidade de doações por doador
# histograa dos valores das doações
############################################
plt.title('Densidade de Doações por Valor')
plt.hist(df_tot_doacao_freq_por_doador['total_doado'])
plt.xlabel('Valor Total da Doação')
plt.ylabel('Número de Doadores')
plt.grid(True)
plt.show()

# gráfico de distribuição frequencia doacoes x valor total doado por doador
# histograa dos valores das doações
############################################
df_aux = df_tot_doacao_freq_por_doador.groupby('contagem_doacoes').agg(
    total_doado=('total_doado', 'sum'),
).reset_index()
plt.title('Frequencia doações x valor total doado')
plt.scatter(df_aux['contagem_doacoes'],df_aux['total_doado'], c='blue')
# Adicionando o grid
plt.grid(True)

# Adicionando nomes aos eixos
plt.xlabel('Frequência de Doações')
plt.ylabel('Valor Total Doado')
plt.show()


# Criando um gráfico de barras
plt.bar(df_aux['contagem_doacoes'], df_aux['total_doado'], color='blue')

# Adicionando o título e os rótulos dos eixos
plt.title('Distribuição frequencia doacoes x valor total doado')
plt.xlabel('Número de Doações')
plt.ylabel('Valor Total Doado')

# Adicionando o grid
plt.grid(axis='y')  # Adicionando grid apenas no eixo y para melhor visualização

plt.show()

"""
# Agrupar os doadores / Identificar grupos de doadores
######################################################
"""
from sklearn.cluster import KMeans

# Supondo que seus dados já estão em um DataFrame chamado df_tot_doacao_freq_por_doador

# Selecionando as features numéricas para o clustering
X = df_tot_doacao_freq_por_doador[['total_doado', 'contagem_doacoes']]

# Método do cotovelo para encontrar o número ideal de clusters
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)

plt.plot(range(1, 11), wcss)
plt.title('Método do Cotovelo')
plt.xlabel('Número de clusters')
plt.ylabel('WCSS')
plt.show()

# Criando 3 clusters
kmeans = KMeans(n_clusters=3, init='k-means++', random_state=42)
y_kmeans = kmeans.fit_predict(X)

# Adicionando a coluna de cluster ao DataFrame original
df_tot_doacao_freq_por_doador['cluster'] = y_kmeans

# Supondo que você tenha um DataFrame com as features e o rótulo do cluster
plt.scatter(df_tot_doacao_freq_por_doador['total_doado'], df_tot_doacao_freq_por_doador['contagem_doacoes'], c=df_tot_doacao_freq_por_doador['cluster'], cmap='rainbow')
plt.xlabel('Total doado')
plt.ylabel('Frequência de doações')
plt.title('Clusters de Doadores')
plt.grid(True)
plt.show()

'''
Dividindo o grupo de doadores em dois
Ponto de corte frequencia de doação = 33
'''
# Criando uma nova coluna para categorizar os doadores
df_tot_doacao_freq_por_doador['grupo_doacoes'] = pd.cut(df_tot_doacao_freq_por_doador['contagem_doacoes'], bins=[-np.inf, 33, np.inf], labels=['<33', '>=33'])

# Agrupando por 'grupo_doacoes' e calculando a soma de 'total_doado'
df_grupo_doadores_freq33 = df_tot_doacao_freq_por_doador.groupby('grupo_doacoes')['total_doado'].sum()

# Criando o gráfico de barras
ax = df_grupo_doadores_freq33.plot(kind='bar')
plt.title('Total de doações - Grupo de Doadores: corte frequencia = 33')
plt.xlabel('Grupo de Doadores')
plt.ylabel('Total Doado')
plt.xticks(rotation=0)  # Para evitar rotação dos rótulos do eixo x
# Adicionando os valores totais acima de cada barra
for p in ax.patches:
    ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center',fontsize=12)
plt.show()























