# -*- coding: utf-8 -*-
"""
Created on Sun Sep  7 13:49:34 2025

@author: Marcos.Perrude
"""

import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

def correlacao_dados_publicos (trasacoes, ativos, outPath):
    
    trasacoes_month = trasacoes['valor_transacao_abs'].resample('M').sum()
    # Baixando dados da API yfinance
    dados = yf.download(ativos, start='2010-01-01', end='2022-12-18')
    dados = dados.rename(columns={'BTC-USD':'BTC', 'GC=F':'Ouro'})
    dados = dados.loc[:, ('Close', 'BTC') : ('Close', 'Ouro')]
    dados.columns = dados.columns.droplevel(0)
    dados = dados.resample('M').mean()
    
    cct = pd.concat([trasacoes_month, dados], axis=1).dropna()
    
    cct['correlação_BTC'] = cct['valor_transacao_abs'].rolling(window=12).corr(cct['BTC']).fillna(0)
    cct['correlação_oURO'] = cct['valor_transacao_abs'].rolling(window=12).corr(cct['Ouro']).fillna(0)
    
    fig, ax = plt.subplots(figsize=(15, 7))
    ax.plot(cct.index, cct['correlação_BTC'].values, linewidth=2, color='blue', label='BTC')
    ax.plot(cct.index, cct['correlação_oURO'].values, linewidth=2, color='red', label='Ouro')
    ax.axhline(0, color="black", linewidth=1, linestyle="--", alpha=0.8)
    ax.set_title('Correlação Móvel Mensal - Volume de transções banco BanVic')
    ax.set_ylabel('Correlação', fontsize=12, fontweight='bold')
    ax.set_ylim(-1.5, 1.5)
    ax.grid(alpha=0.5)
    ax.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(outPath + "/objetivo4_correlationStatistics/correlacao_estatistica.png", dpi=500)
    plt.show()
