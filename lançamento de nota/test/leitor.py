import fitz
import re

def extrair_texto(pdf_path):
    with fitz.open(pdf_path) as doc:
        texto = ""
        for pagina in doc:
            texto += pagina.get_text("text")
    return texto

def buscar_palavras_chave_em_linhas(texto):
    palavras_chave_linhas = {
        "Nota Fiscal": r"\b(?:Nº|Número)\s*[:\-]?\s*(\d+)",
        "SÉRIE": r"\bSÉRIE\s*(\d+)",
        "Filial": r"\bFL\s*(\d+)",
        "DATA DE SAÍDA/ENTRADA": r"\b(?:DATA DE SAÍDA/ENTRADA|Data de Saída)\s*[:\-]?\s*(\d{2}/\d{2}/\d{4})",
        "VALOR TOTAL DA NOTA": r"\b(?:VALOR TOTAL DA NOTA|Valor Total)\s*[:\-]?\s*([\d,\.]+)"
    }
    
    resultados = {}
    for chave, padrao in palavras_chave_linhas.items():
        resultado = re.search(padrao, texto, re.IGNORECASE)
        if resultado:
            resultados[chave] = resultado.group(1).lstrip('0').strip()
        else:
            resultados[chave] = "Não encontrado"
    
    return resultados

def buscar_palavras_chave_no_bloco(texto):
    palavras_chave_bloco = {
        "DESCRIÇÃO DO PRODUTO/SERVIÇO": r"DESCRIÇÃO DO PRODUTO/SERVIÇO\s*\n([\s\S]*?)\n(?:VENCIMENTO|NOME/RAZÃO SOCIAL)",
        "VENCIMENTO": r"VENCIMENTO[\s\S]{0,30}?(\d{2}/\d{2}/\d{4})",
        "NOME/RAZÃO SOCIAL": r"NOME/RAZÃO SOCIAL\s*[:\-]?\s*(?:\d{5,}-)?\s*([A-Z\s]+)"
    }

    resultados = {}
    for chave, padrao in palavras_chave_bloco.items():
        resultado = re.search(padrao, texto, re.IGNORECASE)
        if resultado:
            valor = resultado.group(1).strip()
            if chave == "NOME/RAZÃO SOCIAL":
                if "CASSOL MATERIAIS DE CONSTRUCAO LTD" in valor:
                    resultados[chave] = "CASSOL MATERIAIS DE CONSTRUCAO LTD"
                elif "CASSOLOG TRANSPORTES RODOVIARIOS LTDA" in valor:
                    resultados[chave] = "CASSOLOG TRANSPORTES RODOVIARIOS LTDA"
                else:
                    resultados[chave] = valor
            else:
                resultados[chave] = valor
        else:
            resultados[chave] = "Não encontrado"

    return resultados
