# **RAG-BookInsight: Semantic Analysis & Thematic Reports**

This project automates the creation of a 5-paragraph book report by leveraging a language model (LLM) to ingest, analyze, and synthesize the content of multiple books. It centers on examining a specific query theme (such as social isolation), comparing how each book approaches the topic, and supporting the analysis with accurately cited excerpts from the texts.

---

## **Overview**

This project implements the following automated pipeline:  
1. **Ingestion**: Processes books in various formats (currently supporting PDF, XML, and ePub) and prepares the data for analysis.  
2. **Analysis**: Utilizes a Retrieval-Augmented Generation (RAG) framework to locate passages relevant to the query and employs a language model to analyze how the query's theme is explored in each book.  
3. **Comparison**: Compares the thematic perspectives of the books, identifying similarities and differences, while extracting key excerpts to substantiate claims.  
4. **Report Generation**: Creates a coherent 5-paragraph book report with a well-defined thesis, structured arguments, and a conclusion. All arguments are reinforced by citations from the source texts.  

The process is entirely automated, leveraging LLMs and supporting tools to eliminate the need for manual reading or writing.

---
## **Setup Instructions**  

### 1. **Clone the Repository**  

```bash  
git clone https://github.com/rohit-vernekar/RAG-BookInsight.git
cd RAG-BookInsight
```  

### 2. **Set Up a Virtual Environment**  

Ensure Python is installed (tested with Python 3.9.6).  

Create a virtual environment:  
```bash  
python -m venv venv  
```  

Activate the virtual environment:  
- On **Windows**:  
  ```bash  
  venv\Scripts\activate  
  ```  
- On **Mac/Linux**:  
  ```bash  
  source venv/bin/activate  
  ```  

### 3. **Install Dependencies**  

Install the required packages from [requirements.txt](requirements.txt) and download the `en_core_web_md` model needed by SpaCy:  
```bash  
pip install -r requirements.txt  
python -m spacy download en_core_web_md  
```  

### 4. **Set the OpenAI API Key**  

Update the [config.yml](config.yml) file with your OpenAI API key under the `openai_config` section:  

```yaml  
openai_config:  
  api_key: Your_OPENAI_API_KEY  
```  

### 5. **Configure Query Parameters**  

In the [config.yml](config.yml) file, configure the following parameters under `query_config`:  

- `query`: Specify the query for analysis (e.g., "Social Isolation").  
- `relevant_docs`: Set the number of relevant passages from a book to be used for analysis.  
- `input_files_dir`: Define the directory containing books to be processed.  
- `output_file`: Set the filename for the generated report.  
- `analysis_dir`: Specify the directory to save intermediate analysis files for each book, which will be used to generate the final report.  

---  

## **Design Choices**

### **1. Ingestion**  
The system supports ingesting books in multiple formats, including PDF, XML, and ePub. Plain text is extracted from these formats and split into smaller chunks to fit within the context length of GPT models. The chunk size is dynamically calculated based on:  
- The model’s context window  
- The number of books to process  
- The number of relevant passages to query  

This ensures efficient processing without exceeding token limits.  

### **2. Semantic Search with FAISS**  
Since books are too large to process within a single context window, **FAISS** is used to create a vector store of text embeddings. Relevant excerpts are retrieved based on semantic similarity to the query. The [text-embedding-3-small](https://platform.openai.com/docs/models/gpt-4#embeddings) model is used for embedding text chunks, offering a balance between performance and cost. For improved performance, this can be switched to [text-embedding-3-large](https://platform.openai.com/docs/models/gpt-4#embeddings).  

### **3. Language Model Selection**  
[**GPT-4o**](https://platform.openai.com/docs/models/gpt-4#gpt-4o) is selected for its exceptional contextual understanding and ability to generate structured and coherent outputs.  
  - **Context Window:** Configured to utilize 50% of the 128,000-token limit for optimal balance between input size and processing efficiency.  
  - **Temperature:** Set to 0.4 to produce consistent, probable results while maintaining some degree of variability.  


### **4. Prompt Engineering**  
- **Thematic Analysis Prompts:** Carefully designed to extract meaningful insights from the text, ensuring they reference specific excerpts for context.  
- **Report Generation Prompts:** Tailored to enforce a structured 5-paragraph format, including a clear thesis, well-supported arguments, and a concise conclusion.  

---  