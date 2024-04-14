import os
import json
from resume_worth.utils.utils import get_params, load_embedding_model
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document


params = get_params()
embedding_dir = params['embedding_dir']
embedding_model_name = params['embedding_model_name']
ingestion_metadata_dir = params['ingestion_metadata_dir']

# Create a retriever based on the created vector db with the text embeddings
# See: https://python.langchain.com/docs/integrations/vectorstores/chroma
embedding_function = load_embedding_model(embedding_model_name)
vectordb = Chroma(persist_directory=embedding_dir, embedding_function=embedding_function)


# Get list of file names in ingestion folder
file_name = os.listdir(ingestion_metadata_dir)[0]
file_path = os.path.join(ingestion_metadata_dir, file_name)
with open(file_path, "r") as f:
    job_vacancy_metadata = json.load(f)


def retrieve_top_job_vacancies(job_title: str, resume: str, k: int=3):
    """Function to retrieve the most similar job vacancies to a resume"""

    # For complex queries, use MongoDB-like operators:
    #   $gt, $gte, $lt, $lte, $ne, $eq, $in, $nin
    # See: https://www.mongodb.com/docs/manual/reference/operator/query/
    retriever = vectordb.as_retriever(
        search_type='similarity',
        search_kwargs={
            'k': k,
            'filter': {"job_title": {"$in": job_vacancy_metadata[job_title.lower()]}}
        },
    )

    # Retrieve top vacancies with the job title
    job_docs = retriever.get_relevant_documents(resume)

    # Retrive additional job vacancies if necessary
    k_retrieved = len(job_docs)
    if k_retrieved < k:
        job_docs.extend(vectordb.similarity_search(resume, k=(k-k_retrieved)))

    return job_docs


def get_vacancy_salary(doc: Document):
    """Function to get the salary of a job vacancy"""

    salary = doc.metadata["salary"] 

    return salary


def get_vacancy_description(doc: Document):
    """Function to get the description of a job vacancy"""

    description = doc.page_content

    return description


def get_vacancy_url(doc: Document):
    """Function to get the URL of a job vacancy"""

    job_id = doc.metadata["id"] 

    # Move this information as a metadata of the job
    url = f'https://www.jobstreet.com.my/job/{job_id}'

    return url



