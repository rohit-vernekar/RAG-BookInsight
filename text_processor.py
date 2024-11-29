from langchain.text_splitter import SpacyTextSplitter, RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List

from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from config import openai_config, query_config
from file_reader import read_file

from openai import OpenAI


def _split_text(text: str, chunk_size: int = 256, chunk_overlap: int = 20) -> List[Document]:
    """
    Splits text into smaller chunks

    Args:
        text (str): Text to split
        chunk_size (int, optional): Size of each chunk. Defaults to 256.
        chunk_overlap (int, optional): Overlap between chunks. Defaults to 20.

    Returns:
        List[Document]: List of documents
    """
    spacy_text_splitter = SpacyTextSplitter(pipeline="en_core_web_md")
    clean_text = " ".join(spacy_text_splitter.split_text(text))

    recr_text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap,
    )

    return recr_text_splitter.create_documents([clean_text])


def _prepare_query(documents: List[Document]) -> str:
    """
    Prepares the query for analysis.

    Args:
        documents (List[Document]): List of documents to analyze.

    Returns:
        str: The prepared query for analysis.
    """
    query = f"Analyze the theme of {query_config['query']}"
    embedding_model = OpenAIEmbeddings(model=openai_config["embedding_model"])
    vector_store = FAISS.from_documents(documents, embedding_model)
    
    similar_docs = vector_store.similarity_search(query, k=query_config["relevant_docs"])
    excerpts = [doc.page_content for doc in similar_docs]

    citations = "\n\n".join([f"- Relevant excerpt from document {i+1}: {excerpt}" for i, excerpt in enumerate(excerpts)])
    refined_query = (
        f"{query}. Use the following excerpts to support your analysis:\n\n{citations}\n\n"
        "In your response, clearly reference the lines from documents in quotes and make your analysis structured."
    )
    return refined_query


def _get_analysis(refined_query: str, number_of_files: int) -> str:
    """
    Gets the analysis of the query.

    Args:
        refined_query (str): The refined query for analysis.
        number_of_files (int): The number of files to analyze.

    Returns:
        str: The analysis of the query.
    """
    client = OpenAI()
    response = client.chat.completions.create(
        model=openai_config["model"],
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": refined_query},
        ],
        temperature=openai_config["temperature"],
        max_tokens=min(openai_config["max_output_tokens"], int(openai_config["context_window"]/(number_of_files * 2)))
    )
    analysis = response.choices[0].message.content
    return analysis


def analyze_text(file_path: str, number_of_files: int) -> str:
    """
    Analyzes a text file.

    Args:
        file_path (str): The path to the text file.
        number_of_files (int): The total number of files to analyze.

    Returns:
        str: The analysis of the text file.
    """
    model_context_window = openai_config["context_window"]
    chunk_size = int(model_context_window / (number_of_files * query_config["relevant_docs"] * 2))
    chunk_overlap = int(chunk_size / 10)

    print("Reading file...")
    text = read_file(file_path)
    print("Splitting text into chunks...")
    docs = _split_text(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    print("Preparing query...")
    refined_query = _prepare_query(docs)
    print("Getting analysis...")
    analysis = _get_analysis(refined_query, number_of_files)

    filename = file_path.split("/")[-1].split(".")[0]
    output_path = query_config["analysis_dir"] + "/" + filename + ".txt"
    print("Saving analysis to", output_path)
    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(analysis)

    return analysis  

    