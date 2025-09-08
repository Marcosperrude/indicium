# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 10:16:19 2025

@author: Marcos.Perrude
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Cores para os gráficos
CORES = ['Azul Escuro','Verde Escuro','Vermelho',  'Amarelo','Roxo',
         'Verde Água','Laranja','Azul Médio', 'Verde Claro','Roxo Claro']

# Nesta função busquei analisar a evolução temporal dos dados
def analise_evolutiva_temporal(propostas_creditos, outPath):
    fig, axes = plt.subplots(3, 1, figsize=(20, 18))
    soma_diaria = propostas_creditos['valor_financiamento'].resample('D').sum() / 1000000
    soma_diaria_aprovado = propostas_creditos[propostas_creditos[
        'status_proposta'] == 'Aprovada']['valor_financiamento'].resample('D').sum() / 1000000
    axes[0].plot(soma_diaria.index, soma_diaria.values, color=CORES[0],
                 linewidth=1, label='Total Financiado')
    axes[0].fill_between(soma_diaria.index, soma_diaria.values,
                         alpha=0.5, color=CORES[0])
    axes[0].plot(soma_diaria_aprovado.index, soma_diaria_aprovado.values,
                 color=CORES[1], linewidth=1, label='Total Aprovado')
    axes[0].fill_between(soma_diaria_aprovado.index, 
                         soma_diaria_aprovado.values, alpha=0.5, color=CORES[1])
    axes[0].set_title('Evolução Diária: Total x Aprovado')
    axes[0].set_ylabel('Milhões (R$)')
    axes[0].legend(loc='lower right')
    axes[0].grid(True, alpha=0.3)

    soma_mensal = propostas_creditos['valor_financiamento'].resample('M').sum() / 1000000
    soma_mensal_aprovado = propostas_creditos[propostas_creditos['status_proposta'] == 'Aprovada']['valor_financiamento'].resample('M').sum() / 1e6
    axes[1].plot(soma_mensal.index, soma_mensal.values,
                 color=CORES[0], linewidth=1, label='Total Financiado')
    axes[1].fill_between(soma_mensal.index, soma_mensal.values, 
                         alpha=0.5, color=CORES[0])
    axes[1].plot(soma_mensal_aprovado.index, soma_mensal_aprovado.values, 
                 color=CORES[1], linewidth=1, label='Total Aprovado')
    axes[1].fill_between(soma_mensal_aprovado.index,
                         soma_mensal_aprovado.values, alpha=0.5, color=CORES[1])
    axes[1].set_title('Evolução Mensal: Total x Aprovado')
    axes[1].set_ylabel('Milhões (R$)')
    axes[1].legend(loc='lower right')
    axes[1].grid(True, alpha=0.3)

    soma_anual = propostas_creditos['valor_financiamento'].resample('Y').sum() / 1000000
    soma_anual_aprovado = propostas_creditos[propostas_creditos[
        'status_proposta'] == 'Aprovada']['valor_financiamento'].resample('Y').sum() / 1000000
    axes[2].plot(soma_anual.index, soma_anual.values, color=CORES[0],
                 linewidth=1, label='Total Financiado')
    axes[2].fill_between(soma_anual.index, soma_anual.values, alpha=0.3, color=CORES[0])
    axes[2].plot(soma_anual_aprovado.index, soma_anual_aprovado.values,
                 color=CORES[1], linewidth=1, label='Total Aprovado')
    axes[2].fill_between(soma_anual_aprovado.index, soma_anual_aprovado.values, alpha=0.3, color=CORES[1])
    axes[2].set_title('Evolução Anual: Total x Aprovado')
    axes[2].set_ylabel('Milhões (R$)')
    axes[2].legend(loc='lower right')
    axes[2].grid(True, alpha=0.5)

    plt.tight_layout()
    plt.savefig(outPath + '/objetivo1_analysisPreliminares/analise_evolutiva_temporal.png', dpi=500)

    return fig
#%%

def analise_tendencia_agencia(propostas_creditos, outPath):
    agencia_ano_status = propostas_creditos.groupby(
        ['nome_agencia', 'ano', 'status_proposta'])[
            'valor_financiamento'].sum().unstack(fill_value=0)

    fig, axes = plt.subplots(2, 5, figsize=(20, 10))
    axes = axes.flatten()
    
    for i, agencia in enumerate(agencia_ano_status.index.levels[0]):
        ax = axes[i]
        dados_agencia = agencia_ano_status.loc[agencia]
        anos = dados_agencia.index
        
        bottom = np.zeros(len(anos))
        for j, status in enumerate(dados_agencia.columns):
            valores = dados_agencia[status].values / 1000000
            ax.bar(anos, valores, bottom=bottom, label=status,
                   color=CORES[j % len(CORES)], alpha=0.8, edgecolor='white', linewidth=0.5)
            bottom += valores
        
        x = np.arange(len(anos))
        coef_apr = np.polyfit(x, dados_agencia['Aprovada'].values / 1000000, 1)[0]
        tendencia_apr = np.mean(dados_agencia['Aprovada'].values / 1000000) + coef_apr * (x - np.mean(x))
        ax.plot(anos, tendencia_apr, color='darkgreen',
                linewidth=2,label='Tendência Aprovados')
        
        outros_status = [col for col in dados_agencia.columns if col != 'Aprovada']
        valores_outros = dados_agencia[outros_status].sum(axis=1).values / 1000000
        coef_out = np.polyfit(x, valores_outros, 1)[0]
        tendencia_out = np.mean(valores_outros) + coef_out * (x - np.mean(x))
        ax.plot(anos, tendencia_out, color='darkred', linewidth=2, label='Tendência Outros')
        
        ax.set_title(f'Agência {agencia}')
        ax.set_ylabel('Valor (Milhões R$)')
        ax.grid(alpha=0.5, axis='y')
        ax.tick_params(axis='x', rotation=45)
    
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, title='Status', loc='center right', bbox_to_anchor=(0.98, 0.5))
    fig.suptitle('Análise de Tendência - Proposta de Crédico por Agência')
    plt.tight_layout()
    plt.subplots_adjust(top=0.93, right=0.85)
    plt.savefig(outPath + '/analysisPreliminares/analise_tendencia_agencia.png', dpi=500)
    return fig
#%%

def analise_heatmap_agencia(propostas_creditos, outPath):
    vendas_aprovadas = propostas_creditos[propostas_creditos['status_proposta'] == 'Aprovada']
    fluxo_agencia_anual = (vendas_aprovadas.groupby('nome_agencia')[
        'valor_financiamento'].resample('Y').sum() / 1000000).unstack()
    
    fig, ax = plt.subplots(figsize=(15, 8))
    n_bins = int(np.ceil(fluxo_agencia_anual.values.max() / 0.4))
    bounds = np.arange(0, n_bins * 0.4 + 0.1, 0.4)
    
    im = ax.imshow(fluxo_agencia_anual.values, cmap='YlOrRd',
                   norm=mcolors.BoundaryNorm(bounds, 256), aspect='auto')
    
    ax.set_xticks(range(len(fluxo_agencia_anual.columns)))
    ax.set_xticklabels([col.strftime('%Y') for col in fluxo_agencia_anual.columns], 
                       rotation=45, ha='right')
    ax.set_yticks(range(len(fluxo_agencia_anual.index)))
    ax.set_yticklabels(fluxo_agencia_anual.index)
    
    ax.set_title('Heatmap de Valor Financiado Aprovado por Agência')
    ax.set_xlabel('Ano')
    ax.set_ylabel('Agência')
    
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Valor Financiado (Milhões R$)')
    cbar.set_ticks(bounds)
    
    plt.tight_layout()
    plt.savefig(outPath + '/analysisPreliminares/analise_heatmap_agencia.png', dpi=500)
    return fig

#%%
def analise_rentabilidade(propostas_creditos, outPath):
    soma_mensal_aprovado = (propostas_creditos[propostas_creditos['status_proposta'] == 'Aprovada']
                            .resample('M')['valor_financiamento'].sum()/1000000)
    desvio = soma_mensal_aprovado / soma_mensal_aprovado.mean()
    desvio_anual = desvio.resample('Y').mean()
    
    fig, ax = plt.subplots(figsize=(15, 6))
    (desvio - 1).plot(ax=ax, linewidth=1, color=CORES[0], alpha=1, label="Mensal")
    (desvio_anual - 1).plot(ax=ax, linewidth=1, color=CORES[1], alpha=0.8, label="Anual (média)")
    ax.axhline(0, color="gray", linewidth=1, linestyle="--", alpha=0.7)
    
    ax.set_title('Rentabilidade de Financiamentos Aprovados')
    ax.set_xlabel('Ano')
    ax.set_ylabel('Rentabilidade (Desvio)')
    ax.grid(alpha=0.5)
    ax.legend(loc='lower right')
    
    plt.tight_layout()
    plt.savefig(outPath + '/analysisPreliminares/analise_rentabilidade.png', dpi=500)
    plt.show()
    
    tabela = pd.DataFrame({
        "Período": ["Último Mês", "Últimos 3 Meses", "Últimos 6 Meses", "Últimos 12 Meses"],
        "Rentabilidade Acumulada (%)": [
            (desvio.iloc[-1] - 1) * 100,
            (desvio.iloc[-3:].mean() - 1) * 100,
            (desvio.iloc[-6:].mean() - 1) * 100,
            (desvio.iloc[-12:].mean() - 1) * 100
        ]
    })
    return tabela

