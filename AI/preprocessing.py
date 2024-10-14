# Install NLTK Data
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from unstructured.partition.pdf import partition_pdf

def read_pdf_text_and_tables(filename):


    elements = partition_pdf("example-docs/layout-parser-paper-fast.pdf", infer_table_structure=True, strategy="fast")

    tables = [el for el in elements if el.category == "Table"]
    for table in tables:
        print(table.text)

    texts = [el for el in elements if el.category == "Text"]

    for text in texts:
        print(text.text)

    return table, text



if __name__ == '__main__':

        filename="~/Documents/test.pdf"
        read_pdf_text_and_tables(filename=filename)