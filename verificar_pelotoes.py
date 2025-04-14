import pandas as pd
import os

ARQUIVO = 'veiculos_apreendidos.xlsx'

def contar_por_pelotao(arquivo=ARQUIVO):
    if not os.path.exists(arquivo):
        print(f"[!] Arquivo não encontrado: {arquivo}")
        return

    df = pd.read_excel(arquivo)

    # Agrupamento por pelotão
    contagem = df['Pelotão'].value_counts().sort_index()

    # Total geral
    total = contagem.sum()

    print("\n📊 Apreensões por pelotão:\n")
    print(contagem)
    print("\n🔢 Total geral de apreensões:", total)

if __name__ == "__main__":
    contar_por_pelotao()
