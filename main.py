import os
import pandas as pd
import re
from utils import extrair_varios_dados_linha
from relatorio import gerar_relatorio

# Caminho do arquivo de conversa
CAMINHO_CONVERSA = os.path.join("conversas", "Conversa do WhatsApp com Registro de Veículos Apreendidos.txt")
ARQUIVO_SAIDA_DADOS = "veiculos_apreendidos.xlsx"

def agrupar_mensagens(linhas):
    """
    Agrupa mensagens que pertencem à mesma entrada (o WhatsApp quebra quando são várias linhas).
    """
    agrupadas = []
    msg_atual = ""

    for linha in linhas:
        if re.match(r"^\d{2}/\d{2}/\d{4} \d{2}:\d{2} - ", linha):
            if msg_atual:
                agrupadas.append(msg_atual.strip())
            msg_atual = linha.strip()
        else:
            msg_atual += " " + linha.strip()

    if msg_atual:
        agrupadas.append(msg_atual.strip())

    return agrupadas

def quebrar_blocos_multiplos(texto):
    """
    Quebra uma linha longa contendo múltiplos registros colados.
    Retorna uma lista com blocos menores com padrão de registro.
    """
    padrao = re.compile(
        r"[A-Z0-9\-]{5,8},\s*[AMO],\s*\d{2}[-/]\d{2}[-/]\d{2,4},\s*[\d\-A-Za-z]+,\s*(?:PEL\s*)?[A-Z\. ]+",
        re.IGNORECASE
    )
    return padrao.findall(texto)


def extrair_registros(arquivo, salvar_ignoradas=False):
    registros = []
    ignoradas = []

    with open(arquivo, 'r', encoding='utf-8') as f:
        linhas = f.readlines()

    mensagens = agrupar_mensagens(linhas)

    padrao_mensagem = re.compile(r"^\d{2}/\d{2}/\d{4} \d{2}:\d{2} - .*?: (.*)")

    for mensagem in mensagens:
        match = padrao_mensagem.match(mensagem)
        if not match:
            continue

        conteudo = match.group(1).strip()
        reconhecido = False

        blocos = [conteudo]  # mesmo sem '\n', trata como um bloco
        for bloco in blocos:
            partes = quebrar_blocos_multiplos(bloco)
            for parte in partes:
                resultados = extrair_varios_dados_linha(parte)
                if resultados:
                    registros.extend(resultados)
                    reconhecido = True

        if not reconhecido:
            ignoradas.append(conteudo)

    # Salvar mensagens ignoradas
    if salvar_ignoradas and ignoradas:
        with open("mensagens_ignoradas.txt", "w", encoding="utf-8") as f:
            for msg in ignoradas:
                f.write(msg.strip() + "\n")
        print(f"[!] {len(ignoradas)} mensagens ignoradas salvas em mensagens_ignoradas.txt")

    return registros

def salvar_em_arquivos(registros, nome_base="veiculos_apreendidos"):
    df = pd.DataFrame(registros)

    # Salvar como Excel
    excel_path = f"{nome_base}.xlsx"
    df.to_excel(excel_path, index=False)

    # Salvar como CSV
    csv_path = f"{nome_base}.csv"
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')  # utf-8-sig para abrir bem no Excel

    print(f"[✓] Dados salvos em: {excel_path} e {csv_path}")
    print(f"[i] Total de veículos registrados: {len(df)}")
    return df


def mostrar_resumo(df):
    contagem = df['Pelotão'].value_counts()
    print("\n📊 Apreensões por pelotão:\n")
    print(contagem)
    print(f"\n🔢 Total geral: {len(df)}")

if __name__ == "__main__":
    if not os.path.exists(CAMINHO_CONVERSA):
        print(f"[!] Arquivo não encontrado: {CAMINHO_CONVERSA}")
    else:
        print("[→] Iniciando extração dos dados...\n")
        registros = extrair_registros(CAMINHO_CONVERSA, salvar_ignoradas=True)

        if registros:
            df = salvar_em_arquivos(registros)
            mostrar_resumo(df)
            print("\n[→] Gerando relatório...")
            gerar_relatorio()
        else:
            print("[!] Nenhum registro válido encontrado.")


