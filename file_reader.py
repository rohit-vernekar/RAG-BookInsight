import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
import xml.etree.ElementTree as ET


def _read_epub(file_path: str) -> str:
    """
    Extracts text from an EPUB file

    Args:
        file_path (str): The path to the EPUB file.

    Returns:
        str: The extracted text.
    """
    book = epub.read_epub(file_path)
    text = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_body_content(), 'html.parser')
            text.append(soup.get_text())
    return '\n'.join(text)


def _read_pdf(file_path: str) -> str:
    """
    Extracts text from a PDF file

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: The extracted text.
    """
    reader = PdfReader(file_path)
    text = []
    for page in reader.pages:
        text.append(page.extract_text())
    return '\n'.join(text)


def _read_xml(file_path: str) -> str:
    """
    Extracts text from an XML file
    
    Args:
        file_path (str): The path to the XML file.

    Returns:
        str: The extracted text.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    def get_all_text(node: ET.Element) -> str:
        text = node.text if node.text else ""
        for child in node:
            text += get_all_text(child)
        return text.strip() + " "
    
    return get_all_text(root)


def read_file(file_path: str) -> str:
    """
    Reads text from a file based on its extension

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The extracted text.
    """
    file_extension = file_path.split('.')[-1].lower()
    if file_extension == 'epub':
        return _read_epub(file_path)
    elif file_extension == 'pdf':
        return _read_pdf(file_path)
    elif file_extension == 'xml':
        return _read_xml(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")
