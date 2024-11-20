#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 12:24:41 2024

@author: rogerio

Cria arquivo script para criação de tabela e respectivos registros 
no banco de dados (sql padrão) com base em um dataframe
Testado nos bancos PostgreSql e MySQL
"""
import pandas as pd



def cria_tabela_sql(df: pd.DataFrame, table_name: str) -> None:
    # Mapeamento de tipos de dados pandas para PostgreSQL
    dtype_mapping = {
        'Int64': 'INTEGER',
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
