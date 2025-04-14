import pandas as pd
import os

ARQUIVO_ENTRADA = 'veiculos_apreendidos.xlsx'
ARQUIVO_SAIDA = 'relatorio_apreensoes.xlsx'

def gerar_relatorio(entrada=ARQUIVO_ENTRADA, saida=ARQUIVO_SAIDA):
    if not os.path.exists(entrada):
        print(f"[!] Arquivo de entrada não encontrado: {entrada}")
        return

    # Carrega os dados
    df = pd.read_excel(entrada)

    if df.empty:
        print("[!] Planilha de entrada está vazia.")
        return

    # Cria tabela dinâmica
    tabela = pd.pivot_table(
        df,
        values='Placa',
        index='Pelotão',
        columns='Tipo',
        aggfunc='count',
        fill_value=0
    )

    # Adiciona total por pelotão
    tabela['Total'] = tabela.sum(axis=1)

    # Adiciona linha de total geral
    total_geral = pd.DataFrame(tabela.sum()).T
    total_geral.index = ['TOTAL GERAL']

    # Junta a tabela final
    resultado = pd.concat([tabela, total_geral])

    # Salva no Excel
    resultado.to_excel(saida)
    print(f"[✓] Relatório salvo com sucesso: {saida}")

if __name__ == '__main__':
    gerar_relatorio()
