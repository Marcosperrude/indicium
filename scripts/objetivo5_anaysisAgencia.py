# -*- coding: utf-8 -*-
"""
Created on Sun Sep  7 19:27:43 2025

@author: Marcos.Perrude
"""

import os
import matplotlib.pyplot as plt
import pandas as pd
import os
import matplotlib.pyplot as plt
import pandas as pd

def analise_agencias(transacoes, outPath):

    # Análise dos ultimos 6 meses
    transacoes_6meses = transacoes[transacoes.index >= transacoes.index.max() - pd.DateOffset(months=6)]
    cont_agencia = transacoes_6meses.groupby('nome_agencia')['valor_transacao_abs'].count()
    cont_agencia = cont_agencia.sort_values(ascending=False)

    # Quantidade de transações por agencia
    plt.figure(figsize=(15, 6))
    plt.bar(cont_agencia.index, cont_agencia.values, color=[
        'orange' if i < 3 or i >= len(cont_agencia) - 3 else 'blue'
        for i in range(len(cont_agencia))
    ])
    plt.title("Quantidade de Transações por Agência")
    plt.xlabel("Agência")
    plt.ylabel("Número de Transações")
    plt.xticks(rotation=45)
    plt.grid(alpha=0.5)
    plt.tight_layout()
    plt.savefig(outPath + '/objetivo5_analysisAgencia/hist_quantidade_transacoes.png', dpi=500)


    # Valor médio de cada gencia
    cont_agencia = transacoes_6meses.groupby('nome_agencia')['valor_transacao_abs'].mean()
    cont_agencia = cont_agencia.sort_values(ascending=False)
    plt.figure(figsize=(15, 6))
    plt.bar(cont_agencia.index, cont_agencia.values, color=[
        'orange' if i < 3 or i >= len(cont_agencia) - 3 else 'blue'
        for i in range(len(cont_agencia))
    ])
    plt.title("Volume de Transações por Agência")
    plt.xlabel("Agência")
    plt.ylabel("Valor Médio (R$)")
    plt.xticks(rotation=45)
    plt.grid(alpha=0.5)
    plt.tight_layout()
    plt.savefig(outPath + '/objetivo5_analysisAgencia/hist_volume_transacoes.png', dpi=500)


    # Média valor média e contagem da quantidade de transaçõe spor agencias
    media_agencia = (transacoes_6meses.groupby('nome_agencia')['valor_transacao_abs']
                                      .count()
                                      .reindex(cont_agencia.index))
    fig, ax1 = plt.subplots(figsize=(12, 5))
    ax1.plot(cont_agencia.index, cont_agencia.values, color='blue', label='Quantidade')
    ax1.set(ylabel='Quantidade de Transações', xlabel='Agência',
            title='Quantidade e Valor Médio de Transações por Agência (Últimos 6 meses)')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(alpha=0.5)

    ax2 = ax1.twinx()
    ax2.plot(media_agencia.index, media_agencia.values, color='orange', label='Valor Médio (R$)')
    ax2.set_ylabel('Valor Médio (R$)', color='orange')

    fig.tight_layout()
    plt.savefig(outPath + '/objetivo5_analysisAgencia/hist_valormedio_transacoes.png', dpi=500)



    transacoes_6meses['mes_ano'] = transacoes_6meses.index.strftime('%Y-%m')

    for agencia in transacoes_6meses['nome_agencia'].unique():
        dados = transacoes_6meses[transacoes_6meses['nome_agencia'] == agencia]
        dados_mes = (dados.groupby('mes_ano')['valor_transacao_abs']
                          .agg(quantidade='count', valor_medio='mean')
                          .reset_index())

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(dados_mes['mes_ano'], dados_mes['quantidade'], 'o-', color='blue', label='Quantidade')
        ax.set(title=f'{agencia} - Últimos 6 meses', xlabel='Mês', ylabel='Quantidade')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(alpha=0.5)

        ax2 = ax.twinx()
        ax2.plot(dados_mes['mes_ano'], dados_mes['valor_medio'], 's-', color='orange', label='Valor Médio (R$)')
        ax2.set_ylabel('Valor Médio (R$)', color='orange')

        fig.tight_layout()
        plt.savefig(outPath + f'/objetivo5_analysisAgencia/valormediaXvolume_{agencia}.png', dpi=500)
