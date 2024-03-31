"""
Data Indexing Pipeline

Indexing is the process of organizing data in a way that makes it more efficient to retrieve information later.

This pipeline indexes the job vacancy files on a library compose by a database, vector database and embedding model.
"""

import os
import json
from llmware.library import Library
from llmware.status import Status
from llmware.models import ModelCatalog
from llmware.configs import LLMWareConfig


def setup_library(library_name):

    print("\n***** Seting up Library *****\n")

    #   Step 1 - Create library which is the main 'organizing construct' in llmware
    print ("Step 1: Creating library: {}".format(library_name))

    library = Library().create_new_library(library_name)

    #   Step 2 - Check the main info for the created library
    print (f"Step 2: Checking info of library {library_name}")

    dabatabse = LLMWareConfig().get_active_db()
    print(f"Database - {dabatabse}")

    vector_db = LLMWareConfig().get_vector_db()
    print(f"Vector database - {vector_db}")

    library_path = library.library_main_path
    print(f"Library path - {library_path}")

    embedding_record = library.get_embedding_status()
    print("Embedding record - ")
    print(json.dumps(embedding_record, indent=4))


def install_vector_embeddings(library_name, embedding_model_name):

    print("\n***** Installing an Embedding on a Library *****\n")

    library = Library().load_library(library_name)
    vector_db = LLMWareConfig().get_vector_db()

    #   Step 1 - Installing the Embedding model
    print(f"Step 1: Installing the Embedding model {embedding_model_name}")

    library.install_new_embedding(embedding_model_name=embedding_model_name, vector_db=vector_db, batch_size=100, use_gpu=False)

    #   Step 2 - Check the library embedding status/info
    print (f"Step 2: Checking the library embedding status")

    #   note: for using llmware as part of a larger application, you can check the real-time status by polling Status()
    #   --both the EmbeddingHandler and Parsers write to Status() at intervals while processing
    embedding_status = Status().get_embedding_status(library_name, embedding_model_name)
    print("Substep 1: Embeddings Complete - Status() check at end of embedding - ", embedding_status)

    #   lets take a look at the library embedding status again at the end to confirm embeddings were created
    embedding_record = library.get_embedding_status()
    print("Substep 2:  embedding record - ")
    print(json.dumps(embedding_record, indent=4))


def index_data(library_name, ingestion_folder_path):

    print("\n***** Indexing Data on a Library *****\n")

    library = Library().load_library(library_name)

    #   Step 1 - point ".add_files" method to the folder with the documents
    #   this method is the key ingestion method - parses, text chunks and indexes all files in folder
    #       --will automatically route to correct parser based on file extension
    #       --supported file extensions:  .pdf, .pptx, .docx, .xlsx, .csv, .md, .txt, .json, .wav, and .zip, .jpg, .png
    print (f"Step 1: loading, parsing and indexing files from {ingestion_folder_path}")

    library.add_files(ingestion_folder_path)

    #   use .add_files as many times as needed to build up your library, and/or create different libraries for
    #   different knowledge bases
    #   now, your library is ready to go and you can start to use the library for running queries

    #   Step 2 - Checking the card of the library 
    print (f"Step 2: Checking the card of the library {library_name}")

    updated_library_card = library.get_library_card()
    doc_count = updated_library_card["documents"]
    block_count = updated_library_card["blocks"]
    print(f"Updated library card - documents - {doc_count} - blocks - {block_count}:")
    print(json.dumps(updated_library_card, indent=4))


if __name__ == "__main__":

    #   Paths

    print("HOME:",  os.environ.get("HOME"))
    print("CWD:",  os.getcwd())
    #LLMWareConfig().set_home("/code")
    #LLMWareConfig().set_llmware_path_name("llmware_data")+
    #library_folder_path = os.path.join("data", "03_embedded")
    #os.mkdir(library_folder_path)
    #LLMWareConfig().set_home(library_folder_path)


    #   Config

    dabatabse = "sqlite"
    vector_db = "faiss"
    LLMWareConfig().set_active_db(dabatabse)
    LLMWareConfig().set_vector_db(vector_db)
    # debug_mode options -
    #       0 - default - shows status manager (useful in large parsing jobs) and errors will be displayed
    #       2 - file name only - shows file name being parsed, and errors only
    LLMWareConfig().set_config("debug_mode", 0)


    #   Stage 1 - Create a new library
    
    library_name = "job_vacancies"
    
    setup_library(library_name)


    #   Stage 2 - Install embedding model
    
    #   to see a list of the embedding models supported, uncomment the line below and print the list
    #   embedding_models = ModelCatalog().list_embedding_models()
    #   for i, models in enumerate(embedding_models):
    #       print("embedding models: ", i, models)
    embedding_model_name = "mini-lm-sbert"  #  very popular and fast sentence transformer
    #   note: if you want to swap out "mini-lm-sbert" for Open AI 'text-embedding-ada-002', uncomment these lines:
    #   embedding_model = "text-embedding-ada-002"
    #   os.environ["USER_MANAGED_OPENAI_API_KEY"] = "<insert-your-openai-api-key>"
    install_vector_embeddings(library_name, embedding_model_name)


    #   Stage 3 - Index data
    
    ingestion_folder_path = os.path.join("data", "02_processed")

    index_data(library_name, ingestion_folder_path)
