#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 10:56:07 2024

@author: rogerio

Os arquivos originais (XLSX) fornecidos foram ajustados para manter o padrão de formatação
Nenhum dado foi alterado, criado ou substituído
As informações incompletas devido a formatação das planilhas ou que não representavam
dados relativo aos custos foram excluídas

Padronização auxiliar foi criada para ajudar na análise das despesas
Foram criadas as Categorias e Subcategorias de cada despesa 
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# Caminho do arquivo .xlsx
file_path = '/home/rogerio/Documentos/ASN.Rocks/Projeto Marmitas/DADOS_MARMITAS_EM_ACAO/Custos.xlsx' 

# Ler todas as planilhas do arquivo .xlsx
xls = pd.ExcelFile(file_path)

# DataFrame para armazenar todas as observações de todas as planilhas
df_total = pd.DataFrame()

for sheet_name in xls.sheet_names:
        # Ler cada planilha
        df = pd.read_excel(xls, sheet_name=sheet_name)

        # Selecionar apenas as 6 primeiras colunas
        df = df.iloc[:, :6]
        
        # Converter os nomes das colunas para string e remover espaços
        df.columns = df.columns.astype(str).str.strip()  # Garante que os nomes das colunas estejam limpos

        # Concatenar o DataFrame da planilha atual ao DataFrame total
        df_total = pd.concat([df_total, df], ignore_index=True)
        
# Converter a coluna 'Valor' para numérico, ignorando erros (valores inválidos serão NaN)
df_total['Valor'] = pd.to_numeric(df_total['Valor'], errors='coerce')

# Converter a coluna de data (ajuste o nome da coluna conforme necessário)
df_total['Data'] = pd.to_datetime(df_total['Data'], errors='coerce')

# Criar colunas 'Ano' e 'Mes' a partir da coluna 'Data'
df_total['Ano'] = df_total['Data'].dt.year
df_total['Mes'] = df_total['Data'].dt.month

# Remover linhas onde 'Ano' ou 'Mes' são NaN (casos em que a conversão de data falhou)
df_total.dropna(subset=['Ano', 'Mes'], inplace=True)

# Agrupar por 'Ano' e 'Mes' e somar os valores da coluna 'Valor'
df_agrupado_mes_ano = df_total.groupby(['Ano', 'Mes'])['Valor'].sum().reset_index()

# Agrupar apenas por 'Ano' e somar os valores da coluna 'Valor'
df_agrupado_ano = df_total.groupby('Ano')['Valor'].sum().reset_index()

# Exibir os DataFrames agrupados
print("Sumarização por Ano e Mês:")
print(df_agrupado_mes_ano)

print("\nSumarização apenas por Ano:")
print(df_agrupado_ano)

# Salvar os DataFrames agrupados em arquivos CSV
df_agrupado_mes_ano.to_csv('sumarizacao_por_mes_ano.csv', index=False)
df_agrupado_ano.to_csv('sumarizacao_por_ano.csv', index=False)

# Criar um DataFrame 'df_descricao' com valores únicos da coluna 'descricao'
df_descricao = df_total[['Descrição']].drop_duplicates().reset_index(drop=True)

# Exibir o DataFrame 'df_descricao'
print(df_descricao)

# Salvar o DataFrame 'df_descricao' em um arquivo CSV
df_descricao.to_csv('descricao_unica.csv', index=False)

"""
PADRONIZACAO 
Classificação das despesas em categorias e subcategorias
Um arquivo XLSX foi criado contendo as descrições únicas e as classificações em
cateforia e subcategoria foram realizadas de forma manual 
#########################################################
"""
# Caminho do arquivo (.xlsx) com a padronização
file_path2 = '/home/rogerio/Documentos/ASN.Rocks/Projeto Marmitas/DADOS_MARMITAS_EM_ACAO/descricao_unica_padronizacao.xlsx'

# Ler a planilha do arquivo .xlsx para um DataFrame
df_custo_descricao = pd.read_excel(file_path2)

### criando o dataframe com as informações padronizadas
### fazer a junção (left join) dos dados com base na descrição
##############################################################
df_final = pd.merge(df_total, df_custo_descricao, on='Descrição', how='left')
df_final = df_final.drop(df_final.columns[6:13], axis=1)
df_custos_abt = df_final
#########################################################################
# gráfico das despesas mensais ao longo do tempo                        #
#########################################################################

# Agrupar os custos por Ano e Mes, somando os valores
df_despesas = df_final.groupby(['Ano', 'Mes'])['Valor'].sum().reset_index()

# Garantir que 'Ano' e 'Mes' estejam como inteiros
df_despesas['Ano'] = df_despesas['Ano'].astype(int)
df_despesas['Mes'] = df_despesas['Mes'].astype(int)

# Renomear as colunas 'Ano' e 'Mes' para 'year' e 'month' antes de criar a coluna 'Data'
df_despesas = df_despesas.rename(columns={'Ano': 'year', 'Mes': 'month'})

# Criar a coluna 'Data' usando 'year' e 'month'
df_despesas['Data'] = pd.to_datetime(df_despesas[['year', 'month']].assign(day=1))

# Ordenar os dados pela coluna 'Data' para garantir que estejam em ordem cronológica
df_despesas = df_despesas.sort_values('Data')

# Criar o gráfico
plt.figure(figsize=(12, 6))
plt.plot(df_despesas['Data'], df_despesas['Valor'], marker='o', linestyle='-')

# Configurações do gráfico
plt.title('Despesas ao longo do tempo')
plt.xlabel('Data')
plt.ylabel('Valor das Despesas')
plt.xticks(rotation=45)
plt.grid(True)

# Ajustar o layout para que o gráfico não fique cortado
plt.tight_layout()

# Exibir o gráfico
plt.show()


#########################################################################
# gráfico da categorias ao longo do tempo                               #
#########################################################################

# Agrupar os custos por id_categoria e data (usando Ano e Mes)
df_custos = df_final.groupby(['Ano', 'Mes', 'id_categoria', 'Categoria'])['Valor'].sum().reset_index()

# Garantir que 'Ano' e 'Mes' estejam como inteiros
df_custos['Ano'] = df_custos['Ano'].astype(int)
df_custos['Mes'] = df_custos['Mes'].astype(int)

# Renomear as colunas 'Ano' e 'Mes' para 'year' e 'month' antes de criar a coluna 'Data'
df_custos = df_custos.rename(columns={'Ano': 'year', 'Mes': 'month'})

# Criar a coluna 'Data' usando 'year' e 'month'
df_custos['Data'] = pd.to_datetime(df_custos[['year', 'month']].assign(day=1))

# Criar o gráfico
plt.figure(figsize=(12, 6))

# Fazer a plotagem para cada descrição de categoria
for descricao in df_custos['Categoria'].unique():
    df_categoria = df_custos[df_custos['Categoria'] == descricao]
    plt.plot(df_categoria['Data'], df_categoria['Valor'], marker='o', label=descricao)

# Configurações do gráfico
plt.title('Custos por Categoria ao longo do tempo')
plt.xlabel('Data')
plt.ylabel('Valor dos Custos')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(title='Categoria', bbox_to_anchor=(1.05, 1), loc='upper left')

# Exibir o gráfico
plt.tight_layout()
plt.show()

#########################################################################
# Analisando Custos Totais x (Salário + Aluguel)                        #
#########################################################################

# Agrupar os custos por id_categoria e data (usando Ano e Mes)
df_custos_totais = df_custos.groupby(['year', 'month'])['Valor'].sum().reset_index()
df_filtrado = df_custos[df_custos['Categoria'].isin(['Salário', 'Aluguel'])]
df_custos_salario_aluguel = df_filtrado.groupby(['year', 'month'])['Valor'].sum().reset_index()

df_custos_totais['data'] = pd.to_datetime(df_custos_totais[['year', 'month']].assign(day=1))
df_custos_salario_aluguel['data'] = pd.to_datetime(df_custos_salario_aluguel[['year', 'month']].assign(day=1))

# Inicia o gráfico de linhas
plt.figure(figsize=(10, 5))

# Plota as linhas para cada DataFrame
plt.plot(df_custos_totais['data'], df_custos_totais['Valor'], label='Custo Total', marker='o')
plt.plot(df_custos_salario_aluguel['data'], df_custos_salario_aluguel['Valor'], label='Salário + Aluguel', marker='s')

# Adiciona rótulos e título
plt.xlabel('Data')
plt.ylabel('Valor')
plt.title('Custos Totais x (Salário + Aluguel)')
plt.legend()

# Exibe o gráfico
plt.show()

# calcula o percentual correspondente dos custos com salario + aluguel 
# em relação ao custo total

df_comp_ct_salalu = pd.merge(df_custos_totais, df_custos_salario_aluguel, on='data', how='inner')
df_comp_ct_salalu['percentual'] = df_comp_ct_salalu.apply(lambda row: row['Valor_y'] * 100 / row['Valor_x'], axis=1)
print(df_comp_ct_salalu)
from tabulate import tabulate

# Seleciona apenas as colunas desejadas
df_selecionado = df_comp_ct_salalu[['year_x', 'month_x', 'percentual']]

# Exibe o DataFrame no formato tabular com linhas e colunas delimitadas
tabela_formatada = tabulate(df_selecionado, headers='keys', tablefmt='grid')
print(tabela_formatada)
print(df_selecionado['percentual'].describe())
#########################################################################
# gráfico das subcategorias da alimentação ao longo do tempo            #
#########################################################################

df_custos_alimentacao = df_final[df_final['id_categoria'] == 1]
# Agrupar os custos por  subcategoria e data (usando Ano e Mes)
df_custos_alimentacao_agrupado = df_custos_alimentacao.groupby(['Ano', 'Mes', 'Subcategoria'])['Valor'].sum().reset_index()

# Garantir que 'Ano' e 'Mes' estejam como inteiros
df_custos_alimentacao_agrupado['Ano'] = df_custos_alimentacao_agrupado['Ano'].astype(int)
df_custos_alimentacao_agrupado['Mes'] = df_custos_alimentacao_agrupado['Mes'].astype(int)

# Renomear as colunas 'Ano' e 'Mes' para 'year' e 'month' antes de criar a coluna 'Data'
df_custos_alimentacao_agrupado = df_custos_alimentacao_agrupado.rename(columns={'Ano': 'year', 'Mes': 'month'})

# Criar a coluna 'Data' usando 'year' e 'month'
df_custos_alimentacao_agrupado['Data'] = pd.to_datetime(df_custos_alimentacao_agrupado[['year', 'month']].assign(day=1))

# Criar o gráfico
plt.figure(figsize=(12, 6))

# Fazer a plotagem para cada Subcategoria da Alimentação
for subcategoria in df_custos_alimentacao_agrupado['Subcategoria'].unique():
    df_subcategoria = df_custos_alimentacao_agrupado[df_custos_alimentacao_agrupado['Subcategoria'] == subcategoria]
    plt.plot(df_subcategoria['Data'], df_subcategoria['Valor'], marker='o', label=subcategoria)

# Configurações do gráfico
plt.title('Alimentação: Valores das Subcategorias ao longo do tempo')
plt.xlabel('Data')
plt.ylabel('Valor')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(title='Subcategoria', bbox_to_anchor=(1.05, 1), loc='upper left')

# Exibir o gráfico
plt.tight_layout()
plt.show()


#########################################################################
# gráfico das subcategorias dos descartáveis ao longo do tempo          #
#########################################################################

df_custos_descartaveis = df_final[df_final['id_categoria'] == 3]
# Agrupar os custos por  subcategoria e data (usando Ano e Mes)
df_custos_descartaveis_agrupado = df_custos_descartaveis.groupby(['Ano', 'Mes', 'Subcategoria'])['Valor'].sum().reset_index()

# Garantir que 'Ano' e 'Mes' estejam como inteiros
df_custos_descartaveis_agrupado['Ano'] = df_custos_descartaveis_agrupado['Ano'].astype(int)
df_custos_descartaveis_agrupado['Mes'] = df_custos_descartaveis_agrupado['Mes'].astype(int)

# Renomear as colunas 'Ano' e 'Mes' para 'year' e 'month' antes de criar a coluna 'Data'
df_custos_descartaveis_agrupado = df_custos_descartaveis_agrupado.rename(columns={'Ano': 'year', 'Mes': 'month'})

# Criar a coluna 'Data' usando 'year' e 'month'
df_custos_descartaveis_agrupado['Data'] = pd.to_datetime(df_custos_descartaveis_agrupado[['year', 'month']].assign(day=1))

# Criar o gráfico
plt.figure(figsize=(12, 6))

# Fazer a plotagem para cada Subcategoria dos descartáveis
for subcategoria in df_custos_descartaveis_agrupado['Subcategoria'].unique():
    df_subcategoria = df_custos_descartaveis_agrupado[df_custos_descartaveis_agrupado['Subcategoria'] == subcategoria]
    plt.plot(df_subcategoria['Data'], df_subcategoria['Valor'], marker='o', label=subcategoria)

# Configurações do gráfico
plt.title('Descartáveis: Valores das Subcategorias ao longo do tempo')
plt.xlabel('Data')
plt.ylabel('Valor')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(title='Subcategoria', bbox_to_anchor=(1.05, 1), loc='upper left')

# Exibir o gráfico
plt.tight_layout()
plt.show()

#########################################################################
# gráfico das subcategorias de transporte ao longo do tempo             #
#########################################################################

df_custos_transporte = df_final[df_final['id_categoria'] == 9]
# Agrupar os custos por  subcategoria e data (usando Ano e Mes)
df_custos_transporte_agrupado = df_custos_transporte.groupby(['Ano', 'Mes', 'Subcategoria'])['Valor'].sum().reset_index()

# Garantir que 'Ano' e 'Mes' estejam como inteiros
df_custos_transporte_agrupado['Ano'] = df_custos_transporte_agrupado['Ano'].astype(int)
df_custos_transporte_agrupado['Mes'] = df_custos_transporte_agrupado['Mes'].astype(int)

# Renomear as colunas 'Ano' e 'Mes' para 'year' e 'month' antes de criar a coluna 'Data'
df_custos_transporte_agrupado = df_custos_transporte_agrupado.rename(columns={'Ano': 'year', 'Mes': 'month'})

# Criar a coluna 'Data' usando 'year' e 'month'
df_custos_transporte_agrupado['Data'] = pd.to_datetime(df_custos_transporte_agrupado[['year', 'month']].assign(day=1))

# Criar o gráfico
plt.figure(figsize=(12, 6))

# Fazer a plotagem para cada Subcategoria de Transporte
for subcategoria in df_custos_transporte_agrupado['Subcategoria'].unique():
    df_subcategoria = df_custos_transporte_agrupado[df_custos_transporte_agrupado['Subcategoria'] == subcategoria]
    plt.plot(df_subcategoria['Data'], df_subcategoria['Valor'], marker='o', label=subcategoria)

# Configurações do gráfico
plt.title('Transporte: Valores das Subcategorias ao longo do tempo')
plt.xlabel('Data')
plt.ylabel('Valor')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(title='Subcategoria', bbox_to_anchor=(1.05, 1), loc='upper left')

# Exibir o gráfico
plt.tight_layout()
plt.show()

#########################################################################
# gráfico das subcategorias outros ao longo do tempo             #
#########################################################################

df_custos_outros = df_final[df_final['id_categoria'] == 6]
# Agrupar os custos por  subcategoria e data (usando Ano e Mes)
df_custos_outros_agrupado = df_custos_outros.groupby(['Ano', 'Mes', 'Subcategoria'])['Valor'].sum().reset_index()

# Garantir que 'Ano' e 'Mes' estejam como inteiros
df_custos_outros_agrupado['Ano'] = df_custos_outros_agrupado['Ano'].astype(int)
df_custos_outros_agrupado['Mes'] = df_custos_outros_agrupado['Mes'].astype(int)

# Renomear as colunas 'Ano' e 'Mes' para 'year' e 'month' antes de criar a coluna 'Data'
df_custos_outros_agrupado = df_custos_outros_agrupado.rename(columns={'Ano': 'year', 'Mes': 'month'})

# Criar a coluna 'Data' usando 'year' e 'month'
df_custos_outros_agrupado['Data'] = pd.to_datetime(df_custos_outros_agrupado[['year', 'month']].assign(day=1))

# Criar o gráfico
plt.figure(figsize=(12, 6))

# Fazer a plotagem para cada Subcategoria de Transporte
for subcategoria in df_custos_outros_agrupado['Subcategoria'].unique():
    df_subcategoria = df_custos_outros_agrupado[df_custos_outros_agrupado['Subcategoria'] == subcategoria]
    plt.plot(df_subcategoria['Data'], df_subcategoria['Valor'], marker='o', label=subcategoria)

# Configurações do gráfico
plt.title('Outros: Valores das Subcategorias ao longo do tempo')
plt.xlabel('Data')
plt.ylabel('Valor')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(title='Subcategoria', bbox_to_anchor=(1.05, 1), loc='upper left')

# Exibir o gráfico
plt.tight_layout()
plt.show()


#########################################################################
# gráficos boxplots por categoria                                       #
#########################################################################

# Ajustar o tamanho da figura
plt.figure(figsize=(12, 8))

# Criar o boxplot usando o Seaborn
sns.boxplot(data=df_final, x='Categoria', y='Valor', showmeans=True, meanprops={"marker": "o", "markerfacecolor": "red", "markeredgecolor": "black", "markersize": 7})

# Adicionar a mediana, média, quartis e bigodes como texto nos gráficos
for i, category in enumerate(df_final['Categoria'].unique()):
    # Obter os valores da categoria
    category_values = df_final[df_final['Categoria'] == category]['Valor']

    # Calcular os quartis e a mediana
    Q1 = np.percentile(category_values, 25)
    Q2 = np.median(category_values)  # Mediana
    Q3 = np.percentile(category_values, 75)
    mean = np.mean(category_values)
    IQR = Q3 - Q1
    lower_whisker = Q1 - 1.5 * IQR
    upper_whisker = Q3 + 1.5 * IQR

    # Adicionar texto indicando os valores dos quartis, média e bigodes
    plt.text(i, Q1, f'Q1={Q1:.2f}', ha='center', va='top', fontsize=8, color='blue')
    plt.text(i, Q2, f'Mediana={Q2:.2f}', ha='center', va='top', fontsize=8, color='green')
    plt.text(i, Q3, f'Q3={Q3:.2f}', ha='center', va='bottom', fontsize=8, color='blue')
    plt.text(i, mean, f'Média={mean:.2f}', ha='center', va='bottom', fontsize=8, color='red')
    #plt.text(i, lower_whisker, f'Lower={lower_whisker:.2f}', ha='center', va='top', fontsize=8, color='purple')
    #plt.text(i, upper_whisker, f'Upper={upper_whisker:.2f}', ha='center', va='bottom', fontsize=8, color='purple')

# Ajustar o título e os rótulos dos eixos
plt.title('Boxplot dos Valores por Categoria')
plt.xlabel('Categoria')
plt.ylabel('Valor')
plt.xticks(rotation=45)

# Exibir o gráfico
plt.tight_layout()
plt.show()

"""
Função para criação das tabelas 
Converte um dataframe em scrip sql (cria a tabela e os registros)

"""
def create_table_with_inserts_sql(df: pd.DataFrame, table_name: str) -> None:
    # Mapeamento de tipos de dados pandas para PostgreSQL
    dtype_mapping = {
        'int64': 'INTEGER',
        'float64': 'FLOAT',
        'object': 'TEXT',
        'bool': 'BOOLEAN',
        'datetime64[ns]': 'TIMESTAMP',
    }

    # Início do script de criação da tabela
    sql_script = f"CREATE TABLE {table_name} (\n"

    # Iterar pelas colunas do dataframe e criar os campos da tabela
    for col in df.columns:
        # Obter o tipo de dado da coluna
        col_type = str(df[col].dtype)
        # Mapear o tipo de dado para um tipo PostgreSQL
        sql_type = dtype_mapping.get(col_type, 'TEXT')  # Padrão para TEXT caso não encontre o tipo
        # Adicionar a definição da coluna ao script
        sql_script += f"    {col} {sql_type},\n"

    # Remover a última vírgula e adicionar o fechamento do comando SQL
    sql_script = sql_script.rstrip(",\n") + "\n);\n\n"

    # Adicionar os comandos INSERT para cada linha do DataFrame
    for index, row in df.iterrows():
        # Preparar os valores para o comando INSERT
        values = []
        for col in df.columns:
            value = row[col]
            # Verificar se o valor é nulo e tratar adequadamente
            if pd.isnull(value):
                values.append('NULL')
            elif isinstance(value, str):
                # Escapar aspas simples em strings
                escaped_value = value.replace("'", "''")
                values.append(f"'{escaped_value}'")
            elif isinstance(value, (int, float, bool)):
                values.append(str(value))
            elif isinstance(value, pd.Timestamp):
                # Formatando datetime para PostgreSQL
                values.append(f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'")
            else:
                values.append(f"'{str(value)}'")

        # Construir o comando INSERT
        values_str = ", ".join(values)
        sql_script += f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({values_str});\n"

    # Salvar o script em um arquivo com o nome da tabela
    file_name = f"{table_name}.sql"
    with open(file_name, 'w') as file:
        file.write(sql_script)

    print(f"Script SQL com tabela e inserts gerado e salvo em {file_name}")


# Cria a tabela de padronização das categoria

create_table_with_inserts_sql(df_custo_descricao, 'custo_descricao')

create_table_with_inserts_sql(df_final, 'custos')
