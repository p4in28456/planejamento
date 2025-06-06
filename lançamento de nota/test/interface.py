import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import re

def extrair_texto(pdf_path):
    try:
        with fitz.open(pdf_path) as doc:
            texto = ""
            for pagina in doc:
                texto += pagina.get_text("text")  # Obtém todo o texto da página
        return texto
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível ler o PDF:\n{e}")
        return ""

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
            resultados[chave] = resultado.group(1).lstrip('0').strip() if resultado.group(1) else "Não encontrado"
        else:
            resultados[chave] = "Não encontrado"
    
    return resultados

def buscar_palavras_chave_no_bloco(texto):
    palavras_chave_bloco = {
        "DESCRIÇÃO DO PRODUTO/SERVIÇO": r"DESCRIÇÃO DO PRODUTO/SERVIÇO\s*[:\-]?\s*(.*)",
        "VENCIMENTO": r"VENCIMENTO[\s\S]{0,30}?(\d{2}/\d{2}/\d{4})",
        "NOME/RAZÃO SOCIAL": r"NOME/RAZÃO SOCIAL\s*[:\-]?\s*(.*)"
    }

    resultados = {}

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


def abrir_pdf(resultado_texto):
    arquivo_pdf = filedialog.askopenfilename(filetypes=[["Arquivos PDF", "*.pdf"]])
    if not arquivo_pdf:
        return
    
    texto = extrair_texto(arquivo_pdf)
    
    if not texto:
        messagebox.showwarning("Aviso", "Não foi possível extrair texto do PDF.")
        return
    
    resultados_linhas = buscar_palavras_chave_em_linhas(texto)
    resultados_bloco = buscar_palavras_chave_no_bloco(texto)
    
    # Exibe os resultados na interface gráfica
    resultado_texto.delete(1.0, tk.END)
    
    # Resultados de palavras-chave em linhas
    resultado_texto.insert(tk.END, "Palavras-chave em linhas:\n")
    for chave, valor in resultados_linhas.items():
        resultado_texto.insert(tk.END, f"{chave}: {valor}\n")
    
    resultado_texto.insert(tk.END, "\n\n")
    
    # Resultados de palavras-chave no bloco
    resultado_texto.insert(tk.END, "Palavras-chave no bloco:\n")
    for chave, valor in resultados_bloco.items():
        resultado_texto.insert(tk.END, f"{chave}: {valor}\n")

# Criando a interface gráfica
janela = tk.Tk()
janela.title("Leitura de PDF e Busca por Palavras-chave")
janela.geometry("700x500")

# Botão para selecionar PDF
botao_abrir = tk.Button(janela, text="Selecionar PDF", command=lambda: abrir_pdf(resultado_texto))
botao_abrir.pack(pady=10)

# Área de texto para exibir os resultados
resultado_texto = scrolledtext.ScrolledText(janela, width=80, height=20)
resultado_texto.pack(pady=10)

# Executando a aplicação
janela.mainloop()
