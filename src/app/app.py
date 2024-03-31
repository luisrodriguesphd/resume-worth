import os
import gradio as gr
from resume_worth.pipelines.information_retrieval.information_retrieval import retrieve_top_job_vacancies, get_vacancy_salary


APP_TITLE = "ResumeWorth"

APP_DESCRIPTION = """Discover Your Market Value!

Unlock the true value of your experience with ResumeWorth. 

Simply enter your job title, upload your resume, and let our advanced AI analyze your professional background. 
In moments, you'll receive an estimated salary, tailored to your unique skills and experience. 
"""
# Empower your job search with insights that put you a step ahead.

job_titles = ["Data Engineer", "Data Scientist", "Data Analyst", "Machine Learning Engineer"]

PORT = 7860

def salary_estimator(job_title, resume):

    library_name = "job_vacancies"
    max_retrieved_chunks = 1

    file_source, _, _ = retrieve_top_job_vacancies(library_name, job_title, resume, max_retrieved_chunks)
    
    if len(file_source) == 0:
        return "Not found a suitable job vacancy." 

    ingestion_folder_path = os.path.join("data", "02_processed")

    salary = get_vacancy_salary(ingestion_folder_path, file_name=file_source[0])

    return salary


def run():
    # See details in https://www.gradio.app/docs/interface
    app = gr.Interface(
        fn=salary_estimator, 
        inputs=[
            gr.Radio(job_titles, label="Job Title"),
            gr.Textbox(label="Resume", lines=6)
        ],
        outputs=[
            gr.Textbox(label="Estimate Salary", lines=3)
        ],
        title=APP_TITLE,
        description=APP_DESCRIPTION,
        allow_flagging="never"
    )

    # app.launch(share=True) lets you create a public link to share with your team or friends. This share link expires in 72 hours.
    # For free permanent hosting and GPU upgrades, run `gradio deploy` from Terminal to deploy to Spaces (https://huggingface.co/spaces)
    app.launch(server_name='0.0.0.0', server_port=int(PORT))

if __name__ == "__main__":
    run()
