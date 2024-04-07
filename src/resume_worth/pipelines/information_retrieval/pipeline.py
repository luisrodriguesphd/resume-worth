"""
Information Retrieval Pipeline

This pipeline utilizes the user resume to first pull the most similar vacancy from the job database and then get its salary.
"""


from resume_worth.pipelines.information_retrieval.nodes import retrieve_top_job_vacancies, get_vacancy_salary, get_vacancy_url


def retrieve_top_job_vacancy_info(job_title: str, resume: str):

    # Stage 1 - Retrieve most similar jobs

    job_docs = retrieve_top_job_vacancies(job_title, resume, k=1)

    # Stage 2 - Get the salary for retrieved jobs

    salary, url = None, None
    if len(job_docs) > 0:
        salary = get_vacancy_salary(job_docs[0])
        url = get_vacancy_url(job_docs[0])
        
    return salary, url


if __name__ == "__main__":

    # EXAMPLE

    job_title = "machine learning engineer"
    resume = "I design, develop, and deploy machine learning models and algorithms for complex and unique datasets."
    k = 2

    salaries = retrieve_top_job_vacancy_info(job_title, resume, k)

    print(salaries)
