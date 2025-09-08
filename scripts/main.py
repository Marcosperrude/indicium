# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 20:13:56 2025

@author: Marcos.Perrude
"""

import os
import pandas as pd
from objetivo1_analysisPreliminares import analise_evolutiva_temporal ,analise_rentabilidade, analise_tendencia_agencia, analise_heatmap_agencia
from objetivo3_analysisStatistics import analise_fluxo_transacoes
from objetivo4_correlationStatistics import correlacao_dados_publicos
from objetivo5_anaysisAgencia import analise_agencias
#%%

# Reconhecer pasta do repositório
repoPath = os.path.dirname(os.getcwd())

# Definindo pasta de dados
dataPath = repoPath +'/inputs'
outPath = repoPath + '/outputs'


os.listdir(dataPath)
colaboradores  = pd.read_csv(dataPath + '\\colaboradores.csv', encoding = 'utf-8')
colaborador_agencia  = pd.read_csv(dataPath + '\\colaborador_agencia.csv', encoding = 'utf-8')
propostas_creditos = pd.read_csv(dataPath + '\\propostas_credito.csv',  encoding = 'utf-8')
agencias = pd.read_csv(dataPath + '\\agencias.csv',  encoding = 'utf-8')

identificacao = dict(zip(colaborador_agencia['cod_colaborador'], colaborador_agencia['cod_agencia']))
indentifcacao_nome = dict(zip(agencias['cod_agencia'], agencias['nome']))

# Identificando colaboradores e agenciais
colaboradores['agencia'] = colaboradores['cod_colaborador'].map(identificacao)
colaboradores['nome_agencia'] = colaboradores['agencia'].map(indentifcacao_nome)
# Identificando propostas 
propostas_creditos['agencia'] = propostas_creditos['cod_colaborador'].map(identificacao)
propostas_creditos['nome_agencia'] = propostas_creditos['agencia'].map(indentifcacao_nome)

propostas_creditos['data_entrada_proposta'] = pd.to_datetime(propostas_creditos['data_entrada_proposta'])
propostas_creditos = propostas_creditos.set_index("data_entrada_proposta")

propostas_creditos['ano'] = propostas_creditos.index.year

#%% Objetivo 1 - Análises preliminares

# Análise historica e temporal do potencial e das vendas aprovadas
analise_evolutiva_temporal(propostas_creditos, outPath)

# Análise de tendencia de cada agencia em cada ano
analise_tendencia_agencia(propostas_creditos, outPath)

#análise de predominancia de mercado de cada agencia e cada ano
analise_heatmap_agencia(propostas_creditos, outPath)

rentailidade = analise_rentabilidade(propostas_creditos, outPath)

#%% Objetivo 3  - Análise estatísticas com o uso de dimensão de datas

transacoes = pd.read_csv(dataPath + '/transacoes.csv', encoding= 'utf-8')

transacoes = analise_fluxo_transacoes(transacoes, outPath)
#%%Etapa 4 - Correlação com dados publico - Bitcoin e Ouro

# Análisando dados de bitcoin['BTC-USD'], Ouro[ 'GC=F'] 
ativos = ['BTC-USD', 'GC=F']
correlacao_dados_publicos(transacoes, ativos, outPath)

#%% Objetivo 5

contas = pd.read_csv(dataPath + '/contas.csv', encoding='utf-8')
transacoes['num_agencia'] = transacoes['num_conta'].map(dict(zip(contas['num_conta'], contas['cod_agencia'])))
transacoes['nome_agencia'] = transacoes['num_agencia'].map(indentifcacao_nome)

analise_agencias(transacoes, outPath)


#
