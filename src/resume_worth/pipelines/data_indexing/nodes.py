import os
import json
from langchain.docstore.document import Document
from resume_worth.utils.utils import load_embedding_model
from langchain_community.vectorstores import Chroma


def parse_documents(file_dir: str):
    """Function to load and parse the job vacancy documents"""

    print("\n***** Loading Documents *****\n")

    # Get list of file names in ingestion folder
    file_names = [file for file in os.listdir(file_dir) if ".json" in file]

    # Load files and parse as documentss
    docs = []
    for file_name in file_names:
        file_path = os.path.join(file_dir, file_name)
        with open(file_path, "r") as f:
            file_content = json.load(f)

        page_content = file_content["description"]
        file_content.pop("description")

        metadata = file_content
        metadata['source'] = file_path

        doc = Document(page_content=page_content, metadata=metadata)

        docs.append(doc)

    print(f"-> Loaded {len(docs)} documents from {file_dir}")

    return docs


def index_documents(docs: list[Document], persist_directory: str, embedding_model: dict):
    """Function to embed and index the documents in Chroma vector database"""

    print("\n***** Indexing Data on a Vector Store *****\n")

    print(f"-> Load a pretrained text embedding model {embedding_model['model_name']}")

    # Load a pretrained text embedding model
    embedding_function = load_embedding_model(embedding_model['model_name'], embedding_model['model_kwargs'], embedding_model['encode_kwargs'])

    print(f"-> Embed documents and index in Chroma vector store")

    # Create text embeddings and store in a vector database Chroma. For more options, see: 
    #   https://python.langchain.com/docs/modules/data_connection/vectorstores/
    #   https://python.langchain.com/docs/integrations/vectorstores/chroma
    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embedding_function,
        persist_directory=persist_directory
    )

    print(f"-> Indexed {vectordb._collection.count()} documents")

    return vectordb
