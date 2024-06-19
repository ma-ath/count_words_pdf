from pathlib import Path
from tika import parser

def pdf_to_string(file_path: Path):
    try:
        text = parser.from_file(str(file_path.absolute()))['content']
        assert(text is not None)
        return text
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def save_string_to_file(text, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(text)

if __name__ == '__main__':
    word = input("Qual palavra deseja contar? ")
    # Ler lista de todos os PDFs
    directory = '.'
    all_pdf_text = []

    print("Lendo arquivos...")
    for file_path in Path(directory).glob('*.pdf'):
        # print(f"Lendo {file_path}")
        all_pdf_text.append(pdf_to_string(file_path))

    print(f"Li {len(all_pdf_text)} arquivos")
    all_pdf_text = '\n'.join(all_pdf_text)

    save_string_to_file(all_pdf_text, "TODOS_OS_ARQUIVOS.txt")

    # Count number of words
    number_of_occurences = all_pdf_text.lower().count(word.lower())
    print(f"Contei a palavra {word} {number_of_occurences} vezes")