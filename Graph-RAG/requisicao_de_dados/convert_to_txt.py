"""Percorre a árvore de diretórios e converte os arquivos PDF para TXT.
"""
import PyPDF2
import os

pdffile = open("/PROJETOS VSCODE/AED2/projeto_final/polls_chat_br/Graph-RAG/requisicao_de_dados/pdfs/RO/porto-velho/proposta-de-coronel-ronaldo-flores.pdf", "rb")
#("/home/mateus-lacerda/Área de trabalho/Estudo/VSCodeProjects/AEED2/Graph-RAG/pdfs/RO/nova-mamore/proposta-de-dr-alexandre-nogueira.pdf", "rb")

pdfreader = PyPDF2.PdfReader(pdffile)

x = len(pdfreader.pages)
"""
pageobj = pdfreader.pages[0]

text = pageobj.extract_text()

file1 = open("/home/mateus-lacerda/Área de trabalho/Estudo/VSCodeProjects/AEED2/Graph-RAG/pdfs/RO/nova-mamore/proposta-de-dr-alexandre-nogueira.txt", "a")
file1.writelines(text)"""

for i in range(x):
    pageobj = pdfreader.pages[i]

    text = pageobj.extract_text()

    file1 = open("/home/mateus-lacerda/Área de trabalho/Estudo/VSCodeProjects/AEED2/Graph-RAG/pdfs/RO/nova-mamore/proposta-de-dr-alexandre-nogueira.txt", "a")
    file1.writelines(text)


# Function to convert text file to UTF-8
def convert_to_utf8(input_file, output_file=None):
    # Determine output file name if not specified
    if output_file is None:
        base_name, ext = os.path.splitext(input_file)
        output_file = f"{base_name}_utf8{ext}"

    # Open and read the input file
    with open(input_file, 'r', encoding='ISO-8859-1') as f:
        content = f.read()

    # Write content to output file with UTF-8 encoding
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"File '{input_file}' converted to UTF-8 and saved as '{output_file}'.")

# Convert the text file to UTF-8
convert_to_utf8("/home/mateus-lacerda/Área de trabalho/Estudo/VSCodeProjects/AEED2/Graph-RAG/pdfs/RO/nova-mamore/proposta-de-dr-alexandre-nogueira.txt")

