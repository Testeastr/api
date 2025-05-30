import subprocess
import json
import os
import re

CAMINHO_BANCO = "api_imoveis/data/banco_fake.json"

def extrair_texto_com_pdtotext(pdf_path, caminho_pdftotext):
    arquivo_saida = "saida_temp.txt"
    subprocess.run([caminho_pdftotext, pdf_path, arquivo_saida], check=True)
    with open(arquivo_saida, 'r', encoding='utf-8') as f:
        texto = f.read()
    os.remove(arquivo_saida)
    return texto

def to_float(valor_str):
    try:
        return float(valor_str.replace('.', '').replace(',', '.'))
    except:
        return None

def processar_texto_em_dados(texto):
    # ID e Endereço
    contrato_match = re.search(r"Contrato\s+([\d\-/]+)\s*-\s*(.+)", texto)
    id_contrato = contrato_match.group(1).strip() if contrato_match else None
    endereco = contrato_match.group(2).strip() if contrato_match else None

    # Locatário (CPF ou CNPJ)
    locatario_match = re.search(r"Locat[aá]rio\s+(.+?)\s+(?:CNPJ|CPF)", texto, re.DOTALL)
    locatario = locatario_match.group(1).strip() if locatario_match else None

    # Aluguel
    aluguel_match = re.search(r"Aluguel\s*[-–]?\s*.*?(\d{1,3}(?:\.\d{3})*,\d{2})", texto)
    valor_aluguel = to_float(aluguel_match.group(1)) if aluguel_match else None

    # Taxa Administração
    taxa_adm_match = re.search(r"Taxa Administração\s*[-–]?\s*(-?\d{1,3}(?:\.\d{3})*,\d{2})", texto)
    taxa_administracao = to_float(taxa_adm_match.group(1)) if taxa_adm_match else None

    # Total para repasse
    total_repasse_match = re.search(r"Total para repasse\s*(\d{1,3}(?:\.\d{3})*,\d{2})", texto)
    total_para_repasse = to_float(total_repasse_match.group(1)) if total_repasse_match else None

    # Pagamento realizado
    pagamento_realizado = "Pagamento Ainda não realizado" not in texto

    # Ignora blocos incompletos
    if not id_contrato or (not valor_aluguel and not taxa_administracao and not total_para_repasse):
        return None

    return {
        "id": id_contrato,
        "endereco": endereco,
        "locatario": locatario,
        "valor_aluguel": valor_aluguel,
        "taxa_administracao": taxa_administracao,
        "total_para_repasse": total_para_repasse,
        "pagamento_realizado": pagamento_realizado
    }

def extrair_imoveis_do_texto(texto):
    blocos = re.split(r"(?=Contrato\s+[\d\-/]+)", texto)
    imoveis = []

    for bloco in blocos:
        bloco = bloco.strip()
        if not bloco:
            continue
        dados = processar_texto_em_dados(bloco)
        if dados:
            imoveis.append(dados)
    return imoveis

def salvar_em_banco_fake(novo_dado, caminho=CAMINHO_BANCO):
    if not os.path.exists(caminho):
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump([], f)

    with open(caminho, 'r', encoding='utf-8') as f:
        dados = json.load(f)

    if not isinstance(dados, list):
        dados = []

    dados.append(novo_dado)

    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def extrair_e_salvar_todos(pdf_path, caminho_pdftotext):
    texto = extrair_texto_com_pdtotext(pdf_path, caminho_pdftotext)
    print("=== Texto extraído do PDF ===")
    print(texto)
    imoveis = extrair_imoveis_do_texto(texto)
    print("=== Dados extraídos dos imóveis ===")
    print(json.dumps(imoveis, indent=2, ensure_ascii=False))

    for imovel in imoveis:
        salvar_em_banco_fake(imovel)

    print(f"{len(imoveis)} imóveis salvos no arquivo JSON: {CAMINHO_BANCO}")
    return imoveis

if __name__ == "__main__":
    caminho_pdf = r"C:\Users\Eduarda.Amorim\Desktop\API\PDF Welby.pdf"
    caminho_pdftotext = r"C:\Users\Eduarda.Amorim\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin\pdftotext.exe"

    if not os.path.exists(caminho_pdf):
        print(f"Arquivo PDF não encontrado: {caminho_pdf}")
    elif not os.path.exists(caminho_pdftotext):
        print(f"Executável pdftotext não encontrado: {caminho_pdftotext}")
    else:
        extrair_e_salvar_todos(caminho_pdf, caminho_pdftotext)
