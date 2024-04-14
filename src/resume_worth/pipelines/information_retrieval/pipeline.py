"""
Information Retrieval Pipeline

This pipeline utilizes the user resume to first pull the most similar vacancy from the job database and then get its salary.
"""


from resume_worth.pipelines.information_retrieval.nodes import retrieve_top_job_vacancies, get_vacancy_salary, get_vacancy_url, get_vacancy_description


def retrieve_top_job_vacancy_info(job_title: str, resume: str):

    # Stage 1 - Retrieve the most similar job

    job_docs = retrieve_top_job_vacancies(job_title, resume, k=1)
    top_job_doc = None
    if len(job_docs) > 0:
        top_job_doc = job_docs[0]

    # Stage 2 - Get the salary for retrieved job

    salary, url, description = None, None, None
    if top_job_doc is not None:
        salary = get_vacancy_salary(top_job_doc)
        url = get_vacancy_url(top_job_doc)
        description = get_vacancy_description(top_job_doc)
        
    return salary, url, description


if __name__ == "__main__":

    # EXAMPLE

    job_title = "machine learning engineer"
    resume = "I design, develop, and deploy machine learning models and algorithms for complex and unique datasets."

    salary, url, description = retrieve_top_job_vacancy_info(job_title, resume)

    print("salary:", salary)
    print("job url:", url)
    print("job description:", description)
    