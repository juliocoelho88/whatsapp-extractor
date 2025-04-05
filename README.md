# 🛠️ WhatsApp Veículos Extractor

Script em Python para extrair registros de veículos apreendidos a partir de conversas exportadas do WhatsApp, validando os dados e gerando uma planilha `.xlsx` com relatórios por pelotão e tipo de veículo.

---

## 🚀 Funcionalidades

- 📄 Lê mensagens no formato: `PLACA, TIPO, DATA(dd-mm-YYYY), RE, PELOTÃO`
- 🔍 Valida os dados: placa, tipo (A/M/O), data, RE (6 dígitos), pelotão
- 📊 Gera uma planilha Excel (`veiculos_apreendidos.xlsx`)
- 📈 Cria relatório com contagem por pelotão e tipo (`relatorio_apreensoes.xlsx`)
- ✅ Código modular com boas práticas e pronto para expansão

---

## 📁 Estrutura do Projeto

whatsapp-extractor/ ├── conversas/ │ └── exemplo.txt ├── main.py # Extração e geração da planilha ├── utils.py # Funções auxiliares e validações ├── relatorio.py # Gera relatório agrupado por tipo e pelotão ├── requirements.txt # Bibliotecas utilizadas ├── .gitignore └── README.md


---

## 📥 Como Usar

1. Clone o repositório:

```bash
git clone https://github.com/SEU_USUARIO/whatsapp-veiculos-extractor.git
cd whatsapp-veiculos-extractor

pip install -r requirements.txt

python main.py

python relatorio.py

ABC1234, A, 05-04-2025, 123456, RPMA
XYZ7890, M, 04-04-2025, 654321, INTAB

📦 Bibliotecas utilizadas
pandas

openpyxl (para exportar .xlsx)

datetime

re (expressões regulares)

📸 Exemplo de Saída
Pelotão	A	M	O	Total
RPMA	2	1	0	3
REM	0	1	1	2
TOTAL GERAL	2	2	1	5