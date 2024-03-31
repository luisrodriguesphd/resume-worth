"""
Information Retrieval Pipeline

This pipeline utilizes the user resume to first pull the most similar vacancy from the job database and then get its salary.
"""

import os
from llmware.configs import LLMWareConfig
from llmware.library import Library
from llmware.retrieval import Query
import re


#   Config

dabatabse = "sqlite"
vector_db = "faiss"
LLMWareConfig().set_active_db(dabatabse)
LLMWareConfig().set_vector_db(vector_db)


def retrieve_top_job_vacancies(library_name, job_title, resume, max_retrieved_chunks=3, display_steps=False):

    if display_steps: print("\n***** Retrieving Information *****\n")

    library = Library().load_library(library_name)

    #   Step 1 - Filter vacancies by the job title
    if display_steps: print (f"Step 1: Filter vacancies by the job title {job_title}")
    
    query = f"JOB TITLE: {job_title}"

    text_query_results = Query(library).text_query(query, exact_mode=False, results_only=False)

    if display_steps:
        filtered_files = text_query_results['file_source']
        print("Filtered file sample:", filtered_files[:5])

    #   Step 2 - Retrieve top most similar vacancies
    if display_steps: print (f"Step 2: Retrieve top most similar vacancies")

    query = resume
    doc_filter = {"file_source": text_query_results['file_source']}
    semantic_query_results = Query(library).semantic_query_with_document_filter(query=query, filter_dict=doc_filter, result_count=max_retrieved_chunks, results_only=False)
    
    if display_steps:
        retrieved_files = semantic_query_results['file_source']
        print("Retrieved file sample:", retrieved_files[:5])

    file_source = semantic_query_results['file_source']

    return file_source, text_query_results, semantic_query_results


def get_vacancy_salary(ingestion_folder_path, file_name, display_steps=False):


    if display_steps: print("\n***** Getting Salary for a Job Vacancy *****\n")

    #   Step 1 - Filter vacancies by the job title
    if display_steps: print (f"Step 1: Open the file {file_name} and extract the salary")

    file_path = os.path.join(ingestion_folder_path, file_name)
    with open(file_path, "r") as f:
        lines = f.readlines()
    for line in lines:
        m = re.search("SALARY:(.*)$", line)
        try:
            salary = m.group(0).split("SALARY: ")[1]
            return salary
        except:
            pass 


if __name__ == "__main__":


    # EXAMPLE

    display_steps = True

    #   Stage 1 - Retrieve most similar job vacancy
    
    library_name = "job_vacancies"
    job_title = "Senior Data Analyst"
    resume = "Mainly focuses on analyzing the conversion rate data of Salesperson, compare the data as well as present the optimization proposal. Integrate the result of data analysis."
    max_retrieved_chunks = 1

    file_source, _, _ = retrieve_top_job_vacancies(library_name, job_title, resume, max_retrieved_chunks, display_steps=display_steps)

    if len(file_source) == 0:
        print("Not found a suitable job vacancy.")
        
    else:
        #   Stage 2 - Get the job vacancy salary
        
        ingestion_folder_path = os.path.join("data", "02_processed")

        salary = get_vacancy_salary(ingestion_folder_path, file_name=file_source[0], display_steps=display_steps)
        
        print(salary)

    


