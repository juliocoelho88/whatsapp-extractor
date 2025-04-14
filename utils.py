import re
from datetime import datetime

# Tipos permitidos
TIPOS_VALIDOS = ['A', 'M', 'O']

# Pelotões válidos
PELOTOES_VALIDOS = [
    'A', 'B', 'C', 'D', 'REM', 'REV',
    'RPMA', 'RPMC', 'INTAB', 'INTCD'
]


def validar_placa(placa: str) -> bool:
    """Valida se a placa tem formato aceitável."""
    return bool(re.fullmatch(r'[A-Z0-9\-]{5,8}', placa.upper()))


def validar_tipo(tipo: str) -> bool:
    """Valida o tipo do veículo: A, M ou O."""
    return tipo.upper() in TIPOS_VALIDOS


def normalizar_data(data_str: str) -> str:
    """Converte data para o formato dd-mm-YYYY"""
    for fmt in ("%d-%m-%Y", "%d/%m/%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(data_str.strip(), fmt).strftime("%d-%m-%Y")
        except ValueError:
            continue
    return None


def validar_re(re_str: str) -> bool:
    """Valida se o RE tem ao menos 6 caracteres alfanuméricos"""
    return bool(re.fullmatch(r'[\d\-A-Za-z]{6,}', re_str.strip()))


def normalizar_pelotao(pelotao: str) -> str:
    """Remove espaços, ponto e prefixo 'PEL' e valida contra a lista"""
    pelotao = pelotao.upper().replace('.', '').replace(' ', '').strip()

    if pelotao.startswith("PEL"):
        pelotao = pelotao[3:]

    return pelotao if pelotao in PELOTOES_VALIDOS else None


def extrair_varios_dados_linha(texto: str):
    """
    Extrai todos os conjuntos de dados encontrados em uma linha.
    Retorna uma lista de dicionários.
    """
    padrao = re.compile(
        r"([A-Z0-9\-]{5,8}),\s*([AMO]),\s*(\d{2}[-/]\d{2}[-/]\d{2,4}),\s*([\d\-A-Za-z]+),\s*(?:PEL\s*)?([A-Z\. ]+)",
        re.IGNORECASE
    )

    resultados = []
    matches = padrao.findall(texto)

    for match in matches:
        placa, tipo, data, re_str, pelotao = match
        data_formatada = normalizar_data(data)
        pelotao_corrigido = normalizar_pelotao(pelotao)

        if (
                validar_placa(placa) and
                validar_tipo(tipo) and
                data_formatada and
                validar_re(re_str) and
                pelotao_corrigido
        ):
            resultados.append({
                'Placa': placa.upper(),
                'Tipo': tipo.upper(),
                'Data': data_formatada,
                'RE': re_str.strip(),
                'Pelotão': pelotao_corrigido
            })

    return resultados
