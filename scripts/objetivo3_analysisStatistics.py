# -*- coding: utf-8 -*-
"""
Created on Sun Sep  7 13:33:49 2025

@author: Marcos.Perrude
"""
import pandas as pd
import matplotlib.pyplot as plt
def analise_fluxo_transacoes (trasacoes,outPath):
   
    # Retirada de microsegundos e UTC
    trasacoes["data_transacao"] = (
    trasacoes["data_transacao"]
    .astype(str)
    .str.split(".").str[0]
    .str.replace(" UTC", "", regex=False))

    # Transformar em datetime e deixar como index
    trasacoes["data_transacao"] = pd.to_datetime(trasacoes["data_transacao"])
    trasacoes = trasacoes.set_index("data_transacao")
    
    # Nome do dia da semana em português (mais direto que mapear manualmente)
    trasacoes["dia_semana"] = trasacoes.index.day_name(locale="pt_BR")
    
    # Métrica 1 – quantidade de transações por dia da semana
    qtd_semana = trasacoes.groupby("dia_semana").size()
    print("Maior qtd. de transações:", qtd_semana.idxmax(), qtd_semana.max())
    # Métrica 1 – volume médio por dia da semana
    trasacoes["valor_transacao_abs"] = trasacoes["valor_transacao"].abs()
    vol_semana = trasacoes.groupby("dia_semana")["valor_transacao_abs"].mean()
    print("Maior volume médio diário:", vol_semana.idxmax(), vol_semana.max())
    
    # Métrica 2 – volume médio por mês par vs. ímpar
    trasacoes["mes"] = trasacoes.index.month
    vol_multiplo2 = trasacoes.groupby(trasacoes["mes"] % 2 == 0)["valor_transacao_abs"].mean()
    print(f'Volume de transaçções em meses multiplo de 2 : {vol_multiplo2.iloc[1]} e não multiplo de 2 {vol_multiplo2.iloc[0]}')
    
    # Métrica 3 – volume médio por trimestre
    vol_trim = trasacoes.groupby(trasacoes.index.quarter)["valor_transacao_abs"].mean()
    print("Maior volume trimestral:", vol_trim.idxmax(), vol_trim.max())
    
    # Métrica 4 – volume médio por hora
    vol_hora = trasacoes.groupby(trasacoes.index.hour)["valor_transacao_abs"].mean()
    
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.plot(vol_hora.index, vol_hora.values, linewidth=2, color="blue", label="Média horária")
    ax.fill_between(vol_hora.index, vol_hora.values, alpha=0.3, color="blue")
    ax.set_title("Média de Volume de Transações Horárias")
    ax.set_xlabel("Hora do Dia")
    ax.set_ylabel("Volume (R$)")
    ax.legend(loc="lower right")
    ax.grid(alpha=0.5)
    plt.tight_layout()
    fig.savefig(outPath + "/objetivo3_analysisStatistics/vol_horaria.png", dpi=500)
    plt.show()
    
    return trasacoes
     