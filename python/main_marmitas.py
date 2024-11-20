#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 10:01:04 2024

@author: rogerio

Programa principal, as análises cruzadas serão realizados neste módulo

Os módulos extratos.py, descricao_marmitas.py e custos.py realizam respectivamente 
as análises exploratórias dos dados das doações, dados operacionais de produção 
das marmitas e despesas do projeto

O cruzamento dos dados e composição das observações em uma ABT é construída neste
módulo importando os dataframes que possuem as observações de cada módulo (conjunto
                                                                           de dados) 
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# importação do módulo de custos
from custos import df_custos_abt, df_custos_alimentacao_agrupado

# importação do módulo de extratos
from doacoes import df_doacoes

# importação do módulo de descrição das marmitas
from descricao_marmitas import df_descricao_marmitas, df_agrupado_mes_ano


"""

Calculando a correlação entre as despesas com alimentação (Valor) e a produção de
marmitas (qtd_marmitas)

Valor: dataframe df_custos_alimentacao_agrupado (valor das despesas com alimentação)
qtd_marmitas: dataframe df_agrupado_mes_ano
"""
# filtrando as informações da subcategoria mercado
df_filtrado = df_custos_alimentacao_agrupado[df_custos_alimentacao_agrupado['Subcategoria'] == 'Mercado']
# Criar a coluna 'data' usando 'ano' e 'mes'
# Renomear as colunas 'Ano' e 'Mes' para 'year' e 'month' antes de criar a coluna 'Data'
df_agrupado_mes_ano = df_agrupado_mes_ano.rename(columns={'Ano': 'year', 'Mes': 'month'})
# criando a variável data
df_agrupado_mes_ano['data'] = pd.to_datetime(df_agrupado_mes_ano[['year', 'month']].assign(day=1))
# fazendo um merge com inner join para garantir o mesmo número de observações para a correlação
df_resultado = pd.merge(df_filtrado, df_agrupado_mes_ano, on=['year', 'month'], how='inner')
# calculando a correlação entre o Valor das despesas e a quantidade de marmitas
correlacao = df_resultado['Valor'].corr(df_resultado['qtd_marmitas'])
print(correlacao)

"""

Gráfico de receitas x despesas com linha de saldo e linha de saldo acumulado

receitas: estão no dataframe df_doacoes
despesas: estão no dataframe df_custos_abt
"""

# Calculando a diferença entre receitas e despesas
# Agrupar os dataframes de doações e de custos por mes e ano

# doações: Criar colunas 'Ano' e 'Mes' a partir da coluna 'Data'
df_doacoes['Ano'] = df_doacoes['Data'].dt.year
df_doacoes['Mes'] = df_doacoes['Data'].dt.month

# doações: Agrupar por 'Ano' e 'Mes' e somar os valores da coluna 'Valor'
df_doacoes_agrupado_mes_ano = df_doacoes.groupby(['Ano', 'Mes'])['Valor'].sum().reset_index()

# custos: Agrupar por 'Ano' e 'Mes' e somar os valores da coluna 'Valor'
df_custos_agrupado_mes_ano = df_custos_abt.groupby(['Ano', 'Mes'])['Valor'].sum().reset_index()

# Unir os dataframes de doações e custos por 'Ano' e 'Mes'
df_receitas_despesas = pd.merge(df_doacoes_agrupado_mes_ano, df_custos_agrupado_mes_ano, on=['Ano', 'Mes'], how='outer', suffixes=('_doacoes', '_custos'))
df_receitas_despesas .fillna(0, inplace=True)
# Calcular a diferença entre as colunas 'Valor' das doações e dos custos
df_receitas_despesas['saldo_mesano'] = df_receitas_despesas['Valor_doacoes'] - df_receitas_despesas['Valor_custos']

# Calcular o saldo acumulado, considerando que o saldo de cada mês depende do saldo do mês anterior mais o saldo_mensal
df_receitas_despesas['saldo_acumulado'] = df_receitas_despesas['saldo_mesano'].cumsum()

# Visualizar o resultado
print(df_receitas_despesas)

# plotando o gráfico

# Criar a variável 'periodos' formatada como 'MM-AAAA'
periodos = df_receitas_despesas['Mes'].astype(int).astype(str).str.zfill(2) + '-' + df_receitas_despesas['Ano'].astype(int).astype(str)

# Configurando o gráfico
fig, ax = plt.subplots(figsize=(10, 6))
receitas = df_receitas_despesas['Valor_doacoes']
despesas = -df_receitas_despesas['Valor_custos']  # Negativar despesas para aparecerem abaixo do eixo x
diferenca = df_receitas_despesas['saldo_mesano']
saldoAcum = df_receitas_despesas['saldo_acumulado']

# Plotando as receitas como barras acima do eixo x
ax.bar(periodos, receitas, color='green', label='Receitas')

# Plotando as despesas como barras abaixo do eixo x
ax.bar(periodos, despesas, color='red', label='Despesas')

# Plotando a linha da diferença
ax.plot(periodos, diferenca, color='blue', marker='o', linestyle='-', linewidth=2, label='Diferença')

# Plotando a linha do saldo acumulado
ax.plot(periodos, saldoAcum, color='orange', marker='o', linestyle='-', linewidth=2, label='Saldo Acumulado')

# Adicionando título e legendas
ax.set_title('Receitas e Despesas ao longo do tempo')
ax.set_xlabel('Período')
ax.set_ylabel('Valor (R$)')
ax.axhline(0, color='black', linewidth=1)  # Linha do eixo x
ax.legend()


# Definindo os ticks do eixo x a cada 4 períodos
step = 4
ax.set_xticks(np.arange(0, len(periodos), step))
ax.set_xticklabels(periodos[::step], rotation=45, fontsize=10)

# Exibindo o gráfico
plt.tight_layout()  # Ajusta o layout para evitar sobreposição
plt.show()

"""
# boxplot dos valores das diferenças
####################################
"""

# Calcular as estatísticas básicas
media = diferenca.mean()
mediana = diferenca.median()
moda = diferenca.mode()
percentis = np.percentile(diferenca, [25, 75])

# Criando o boxplot com escala logarítmica no eixo y
plt.figure(figsize=(8, 6))
plt.boxplot(diferenca)
#plt.yscale('log')  # Aplica a escala logarítmica no eixo y

# Adicionar as estatísticas no gráfico
plt.text(1.1, media, f"Média: {media:.2f}", verticalalignment='center', color='blue')
plt.text(1.1, mediana, f"Mediana: {mediana:.2f}", verticalalignment='center', color='green')
plt.text(1.1, percentis[0], f"25º percentil: {percentis[0]:.2f}", verticalalignment='center', color='purple')
plt.text(1.1, percentis[1], f"75º percentil: {percentis[1]:.2f}", verticalalignment='center', color='purple')

# Exibir o gráfico
plt.title('Distribuição das Diferenças')
plt.show()
