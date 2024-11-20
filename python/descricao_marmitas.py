#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 10:56:07 2024

@author: rogerio
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import shapiro
from scipy.stats import levene
from scipy.stats import kruskal

# módulo para crição do script sql: converte dataframe em script de criação de tabela e registros 
import dataframe_to_sqltable as dftosql


# Caminho do arquivo .xlsx
file_path = '/home/rogerio/Documentos/ASN.Rocks/Projeto Marmitas/DADOS_MARMITAS_EM_ACAO/Descricao_Marmitas.xlsx'

# Ler a planilha do arquivo .xlsx diretamente para um DataFrame
df_descricao_marmitas = pd.read_excel(file_path)

# Converter a coluna 'Valor' para numérico, ignorando erros (valores inválidos serão NaN)
df_descricao_marmitas['qtd_marmitas'] = pd.to_numeric(df_descricao_marmitas['qtd_marmitas'], errors='coerce').astype('Int64')
df_descricao_marmitas['qtd_frango'] = pd.to_numeric(df_descricao_marmitas['qtd_frango'], errors='coerce')
df_descricao_marmitas['qtd_carne'] = pd.to_numeric(df_descricao_marmitas['qtd_carne'], errors='coerce')
df_descricao_marmitas['qtd_linguica'] = pd.to_numeric(df_descricao_marmitas['qtd_linguica'], errors='coerce')
df_descricao_marmitas['qtd_calabresa'] = pd.to_numeric(df_descricao_marmitas['qtd_calabresa'], errors='coerce')
df_descricao_marmitas['qtd_arroz'] = pd.to_numeric(df_descricao_marmitas['qtd_arroz'], errors='coerce')
df_descricao_marmitas['qtd_feijao'] = pd.to_numeric(df_descricao_marmitas['qtd_feijao'], errors='coerce')
df_descricao_marmitas['qtd_macarao'] = pd.to_numeric(df_descricao_marmitas['qtd_macarao'], errors='coerce')

# Converter a coluna de data (ajuste o nome da coluna conforme necessário)
df_descricao_marmitas['data'] = pd.to_datetime(df_descricao_marmitas['data'], errors='coerce')

# Criar colunas 'Ano' e 'Mes' a partir da coluna 'Data'
df_descricao_marmitas['ano'] = df_descricao_marmitas['data'].dt.year.astype('Int64')
df_descricao_marmitas['mes'] = df_descricao_marmitas['data'].dt.month.astype('Int64')

# Remover linhas onde 'Ano' ou 'Mes' são NaN (casos em que a conversão de data falhou)
df_descricao_marmitas.dropna(subset=['qtd_marmitas'], inplace=True)

# Agrupar por 'Ano' e 'Mes' e somar os valores da coluna 'Valor'
df_agrupado_mes_ano = df_descricao_marmitas.groupby(['ano', 'mes'])['qtd_marmitas'].sum().reset_index()

# Agrupar apenas por 'Ano' e somar os valores da coluna 'Valor'
df_agrupado_ano = df_descricao_marmitas.groupby('ano')['qtd_marmitas'].sum().reset_index()

# Exibir os DataFrames agrupados
print("Sumarização por Ano e Mês:")
print(df_agrupado_mes_ano)

print("\nSumarização apenas por Ano:")
print(df_agrupado_ano)

dftosql.cria_tabela_sql(df_descricao_marmitas, 'descricao_marmitas')

#########################################################################
# gráfico da produção de marmitas                                       #
#########################################################################

# Criar a coluna 'data' usando 'ano' e 'mes'
# Renomear as colunas 'Ano' e 'Mes' para 'year' e 'month' antes de criar a coluna 'Data'
df_agrupado_mes_ano = df_agrupado_mes_ano.rename(columns={'ano': 'year', 'mes': 'month'})
df_agrupado_mes_ano['data'] = pd.to_datetime(df_agrupado_mes_ano[['year', 'month']].assign(day=1))

# Ordenar os dados pela coluna 'Data' para garantir que estejam em ordem cronológica
df_agrupado_mes_ano = df_agrupado_mes_ano.sort_values('data')

# Criar o gráfico
plt.figure(figsize=(12, 6))
plt.plot(df_agrupado_mes_ano['data'], df_agrupado_mes_ano['qtd_marmitas'], marker='o', linestyle='-')

# Configurações do gráfico
plt.title('Produção de Marmitas ao longo do tempo')
plt.xlabel('Data')
plt.ylabel('Quantidade de Marmitas')
plt.xticks(rotation=45)
plt.grid(True)

# Ajustar o layout para que o gráfico não fique cortado
plt.tight_layout()

# Exibir o gráfico
plt.show()

'''
Plotar gráfico de marmitas produzidas ao longo do tempo (mes/ano) com o total
de produtos utilizados

 Agrupar o total de produtos utilizados
 
'''
# Agrupando por mês e ano e calculando as somas
df_marmitas_agrupado_mes_ano_qtd_marmitas_qtd_produtos = (
    df_descricao_marmitas
    .fillna(0)  # Substituir valores NaN por 0 para evitar problemas na soma
    .assign(qtd_produtos=lambda df: 9*(df['qtd_frango'] + df['qtd_carne'] + df['qtd_calabresa'] + df['qtd_linguica'] + df['qtd_arroz'] + df['qtd_feijao'] + df['qtd_macarao']))
    .groupby(['ano', 'mes'])
    .agg(
        total_marmitas=('qtd_marmitas', 'sum'),
        total_produtos=('qtd_produtos', 'sum')
    )
    .reset_index()
)
df_marmitas_agrupado_mes_ano_qtd_marmitas_qtd_produtos = df_marmitas_agrupado_mes_ano_qtd_marmitas_qtd_produtos.sort_values(by=['ano', 'mes'])

# gráfico de linhas
# Criando uma coluna para o eixo X como combinação de ano e mês
df_marmitas_agrupado_mes_ano_qtd_marmitas_qtd_produtos['ano_mes'] = (
    df_marmitas_agrupado_mes_ano_qtd_marmitas_qtd_produtos['ano'].astype(str) + '-' +
    df_marmitas_agrupado_mes_ano_qtd_marmitas_qtd_produtos['mes'].astype(str).str.zfill(2)
)

# Ordenando os dados pelo eixo X
df_marmitas_agrupado_mes_ano_qtd_marmitas_qtd_produtos = df_marmitas_agrupado_mes_ano_qtd_marmitas_qtd_produtos.sort_values(by=['ano', 'mes'])

# Plotando o gráfico
plt.figure(figsize=(12, 6))
plt.plot(
    df_marmitas_agrupado_mes_ano_qtd_marmitas_qtd_produtos['ano_mes'],
    df_marmitas_agrupado_mes_ano_qtd_marmitas_qtd_produtos['total_marmitas'],
    label='09 * Qtd Marmitas',
    marker='o'
)
plt.plot(
    df_marmitas_agrupado_mes_ano_qtd_marmitas_qtd_produtos['ano_mes'],
    df_marmitas_agrupado_mes_ano_qtd_marmitas_qtd_produtos['total_produtos'],
    label='Qtd Produtos',
    marker='o'
)

# Configurando o gráfico
plt.xticks(rotation=45, ha='right')
plt.title('Quantidade de Marmitas e Produtos por Ano e Mês')
plt.xlabel('Ano-Mês')
plt.ylabel('Quantidade')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

'''
Boxplot das marmitas por produto usado
'''
# Criar o boxplot usando o Seaborn
df_descricao_marmitas_frango    = df_descricao_marmitas[df_descricao_marmitas['qtd_frango']>0]
df_descricao_marmitas_carne     = df_descricao_marmitas[df_descricao_marmitas['qtd_carne']>0]
df_descricao_marmitas_linguica  = df_descricao_marmitas[df_descricao_marmitas['qtd_linguica']>0]
df_descricao_marmitas_calabresa = df_descricao_marmitas[df_descricao_marmitas['qtd_calabresa']>0]
df_descricao_marmitas_arroz     = df_descricao_marmitas[df_descricao_marmitas['qtd_arroz']>0]
df_descricao_marmitas_feijao    = df_descricao_marmitas[df_descricao_marmitas['qtd_feijao']>0]
df_descricao_marmitas_macarao  = df_descricao_marmitas[df_descricao_marmitas['qtd_macarao']>0]

data = {'Frango': df_descricao_marmitas_frango['qtd_marmitas'], 
        'Carne': df_descricao_marmitas_carne['qtd_marmitas'],
        'Linguiça': df_descricao_marmitas_linguica['qtd_marmitas'],
        'Calabresa': df_descricao_marmitas_calabresa['qtd_marmitas'],
        'Arroz': df_descricao_marmitas_arroz['qtd_marmitas'],
        'Feijão': df_descricao_marmitas_feijao['qtd_marmitas'],
        'Macarão': df_descricao_marmitas_macarao['qtd_marmitas']
        }

df_aux = pd.DataFrame(data)
# Ajustar o tamanho da figura
plt.figure(figsize=(12, 8))
ax = sns.boxplot(data=df_aux)
ax.set_ylim(0, None)  # Define limites no eixo y
ax.set_title('Boxplot')  # Define o título
ax.set_ylabel('Valores')  # Define rótulo do eixo y

# Adicionar a mediana, média, quartis e bigodes como texto nos gráficos

# Obter os valores do frango
category_values = df_descricao_marmitas_frango['qtd_marmitas']

# Calcular os quartis e a mediana
Q1 = np.percentile(category_values, 25)
Q2 = np.median(category_values)  # Mediana
Q3 = np.percentile(category_values, 75)
mean = np.mean(category_values)

x_pos = 0
# Adicionar texto indicando os valores dos quartis, média e bigodes
ax.text(x_pos, Q1, f'Q1={Q1:.2f}', ha='center', va='top', fontsize=8, color='blue')
ax.text(x_pos, Q2, f'Mediana={Q2:.2f}', ha='center', va='top', fontsize=8, color='green')
ax.text(x_pos, Q3, f'Q3={Q3:.2f}', ha='center', va='bottom', fontsize=8, color='blue')
ax.text(x_pos, mean, f'Média={mean:.2f}', ha='center', va='bottom', fontsize=8, color='red')

# Obter os valores da carne
category_values = df_descricao_marmitas_carne['qtd_marmitas']

# Calcular os quartis e a mediana
Q1 = np.percentile(category_values, 25)
Q2 = np.median(category_values)  # Mediana
Q3 = np.percentile(category_values, 75)
mean = np.mean(category_values)

x_pos = 1
# Adicionar texto indicando os valores dos quartis, média e bigodes
ax.text(x_pos, Q1, f'Q1={Q1:.2f}', ha='center', va='top', fontsize=8, color='blue')
ax.text(x_pos, Q2, f'Mediana={Q2:.2f}', ha='center', va='top', fontsize=8, color='green')
ax.text(x_pos, Q3, f'Q3={Q3:.2f}', ha='center', va='bottom', fontsize=8, color='blue')
ax.text(x_pos, mean, f'Média={mean:.2f}', ha='center', va='bottom', fontsize=8, color='red')

# Obter os valores da linguica
category_values = df_descricao_marmitas_linguica['qtd_marmitas']

# Calcular os quartis e a mediana
Q1 = np.percentile(category_values, 25)
Q2 = np.median(category_values)  # Mediana
Q3 = np.percentile(category_values, 75)
mean = np.mean(category_values)

x_pos = 2
# Adicionar texto indicando os valores dos quartis, média e bigodes
ax.text(x_pos, Q1, f'Q1={Q1:.2f}', ha='center', va='top', fontsize=8, color='blue')
ax.text(x_pos, Q2, f'Mediana={Q2:.2f}', ha='center', va='top', fontsize=8, color='green')
ax.text(x_pos, Q3, f'Q3={Q3:.2f}', ha='center', va='bottom', fontsize=8, color='blue')
ax.text(x_pos, mean, f'Média={mean:.2f}', ha='center', va='bottom', fontsize=8, color='red')

# Obter os valores da calabresa
category_values = df_descricao_marmitas_calabresa['qtd_marmitas']

# Calcular os quartis e a mediana
Q1 = np.percentile(category_values, 25)
Q2 = np.median(category_values)  # Mediana
Q3 = np.percentile(category_values, 75)
mean = np.mean(category_values)

x_pos = 3
# Adicionar texto indicando os valores dos quartis, média e bigodes
ax.text(x_pos, Q1, f'Q1={Q1:.2f}', ha='center', va='top', fontsize=8, color='blue')
ax.text(x_pos, Q2, f'Mediana={Q2:.2f}', ha='center', va='top', fontsize=8, color='green')
ax.text(x_pos, Q3, f'Q3={Q3:.2f}', ha='center', va='bottom', fontsize=8, color='blue')
ax.text(x_pos, mean, f'Média={mean:.2f}', ha='center', va='bottom', fontsize=8, color='red')

'''
# Iterar sobre cada boxplot e acessar whiskers
lines = ax.lines  # Todos os elementos gráficos das linhas do boxplot
for i in range(4):
    # Cada boxplot tem 2 whiskers: índices são 2*i e 2*i + 1
    lower_whisker = lines[2 * i].get_ydata()[1]  # Whisker inferior
    upper_whisker = lines[2 * i + 1].get_ydata()[1]  # Whisker superior
    
    # Exibir valores
    print(f"Categoria {chr(65 + i)}:")
    print(f"  Lower whisker: {lower_whisker}")
    print(f"  Upper whisker: {upper_whisker}")
    
    # Adicionar como texto no gráfico
    ax.text(i, lower_whisker, f'Lower={lower_whisker:.2f}', ha='center', va='top', fontsize=8, color='purple')
    ax.text(i, upper_whisker, f'Upper={upper_whisker:.2f}', ha='center', va='bottom', fontsize=8, color='purple')
'''

plt.show()

'''
ANOVA (1 fator) - exige homogeneidade de variâncias e normalidade das amostras 
para ser aplicado. Comparação de K médias. 

Verificar se a média de produção é a mesma para todos os produtos. 
H0 = µ1 = µ2 = µ3 = ... = µk 
H1 = pelo menos uma é diferente 
'''

'''
Verificando a normalidade - teste de shapiro-wilk
H0 = Os dados da amostra vêm de uma distribuição Normal 
H1 = Os dados da amostra não vêm de uma distribuição Normal
'''
vlrs_frango    = df_descricao_marmitas_frango['qtd_marmitas']
vlrs_carne     = df_descricao_marmitas_carne['qtd_marmitas']
vlrs_calabresa = df_descricao_marmitas_calabresa['qtd_marmitas']
vlrs_linguica   = df_descricao_marmitas_linguica['qtd_marmitas']

p_value = shapiro(vlrs_frango)
print(f"P-valor: {p_value[1]:.4f}")
p_value = shapiro(vlrs_carne)
print(f"P-valor: {p_value[1]:.4f}")
p_value = shapiro(vlrs_calabresa)
print(f"P-valor: {p_value[1]:.4f}")
p_value = shapiro(vlrs_linguica)
print(f"P-valor: {p_value[1]:.4f}")

'''
===========================================
Os dados não seguem uma distribuição normal
===========================================
Não podemos usar o ANOVA para verificar se a média de produção é a mesma
para todos os produtos

De qualquer modo, para conhecimento vamos verificar a homogeneidade
-------------------------------------------------------------------
Verificando a homogeneidade - teste de Levene
H0: As variâncias dos grupos são homogêneas 
H1: Pelo menos uma das variâncias dos grupos é diferente
'''
#dados = {"frango": vlrs_frango, "carne": vlrs_carne, "calabresa": vlrs_calabresa, "linguica": vlrs_linguica}
stat, p_value = levene(vlrs_frango,vlrs_carne,vlrs_calabresa,vlrs_linguica)
print(p_value)                             

# p-value > 0.05, não rejeitamos H0, ou seja, as variâncias dos grupos são homogêneas

'''
Como não posso utilizar um teste paramétrico, pois as amostras não seguem uma
distribuição normal

Vamos usar um teste não paramétrico: Kruskal-Wallis 
'''
# Aplicando o teste de Kruskal-Wallis
stat, p_value = kruskal(vlrs_frango,vlrs_carne,vlrs_calabresa,vlrs_linguica)
print(p_value)

'''
Calcular a correção entre qtd de marmitas produzida e qtd total de produtos usados

 1 - Calcular o total de produtos usados no dia
 2 - Calcular a correlação 

'''


'''
Clusterização do cardápio
'''


'''
Verificar a média de marmitas produzidas em cardápios com carne x frango x calabrea x ...
 
'''


