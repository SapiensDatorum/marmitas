Código Python - análise exploratória 

custo.py - módulo que carrega os dados das despesas (arquivos XLSX), faz a limpeza e ajustes necessários para criar o dataframe principal a partir do qual serão construídos os gráficos para as análises

doacoes.py - módulo que carrega os dados das doações (arquivos XLSX), faz a limpeza e ajustes necessários para criar o dataframe principal a partir do qual serão construídos os gráficos para as análises

descricao_marmitas.py - módulo que carrega os dados operacionais (produção das marmitas - arquivos XLSX), faz a limpeza e ajustes necessários para criar o dataframe principal a partir do qual serão construídos os gráficos para as análises

dataframe_to_sqltable.py - módulo com uma única função para transformar um dataframe em uma tabela de banco de dados relacional. Gera o script sql de criação da tabela e os comandos de insert para popular a tabela.

main_marmitas.py - módulo principal utilizado para cruzar dados dos módulos custo, doacoes e descricao_marmitas. Gráficos e informações geradas neste módulo dependem diretamente dos dataframes criados nos outros módulos
