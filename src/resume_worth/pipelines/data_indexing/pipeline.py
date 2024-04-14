"""
Data Indexing Pipeline

Indexing is the process of organizing data in a way that makes it more efficient to retrieve information later.

This pipeline indexes the job vacancy files on a library compose by a vector database and a embedding model.
"""


from resume_worth.utils.utils import get_params
from resume_worth.pipelines.data_indexing.nodes import parse_documents, index_documents


def parse_and_index_documents(ingestion_dir: str, embedding_dir: str, embedding_model: dict):

    # Stage 1 - Parse documents
    
    docs = parse_documents(ingestion_dir)

    # Stage 2 - Embedd and index documents

    vectordb = index_documents(docs, embedding_dir, embedding_model)

    vectordb.persist()


if __name__ == "__main__":

    # Get parameters

    params = get_params()
    ingestion_data_dir = params['ingestion_data_dir']
    embedding_dir = params['embedding_dir']
    embedding_model = params['embedding_model']

    # Run pipeline

    parse_and_index_documents(ingestion_data_dir, embedding_dir, embedding_model)
