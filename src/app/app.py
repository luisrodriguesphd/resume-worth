import os
import gradio as gr
from resume_worth.utils.utils import get_params, get_text_from_pdf
from resume_worth.pipelines.information_retrieval.pipeline import retrieve_top_job_vacancy_info
from resume_worth.pipelines.text_generation.pipeline import generate_explanation_why_resume_for_a_job


params = get_params()
app_config = params['app_config']
app_backend = params['app_backend']
app_frontend = params['app_frontend']


def salary_estimator(sources:str, job_title: str, resume_path: str, explanation_flag: bool):

    salary_range, job_url, explanation = '', '', ''

    if job_title is None:
        salary_range = app_frontend['messages']['job_title_not_found']
        return salary_range, job_url, explanation

    if resume_path is None:
        salary_range = app_frontend['messages']['resume_file_not_found']
        return salary_range, job_url, explanation

    resume = get_text_from_pdf(resume_path)

    if len(resume) < app_backend['min_resume_size']:
        salary_range = app_frontend['messages']['too_short_resume']
    
    else:
        salary_range, job_url, job_description = retrieve_top_job_vacancy_info(job_title, resume)

        if salary_range is None:
            salary_range = app_frontend['messages']['salary_not_found']
        
        if job_url is None:
            job_url = app_frontend['messages']['active_job_not_found']
        
        if (explanation_flag) and (job_description is not None):
            explanation = generate_explanation_why_resume_for_a_job(resume, job_description)

    return salary_range, job_url, explanation


# See details in https://www.gradio.app/docs/interface
demo = gr.Interface(
    fn=salary_estimator, 
    inputs=[
        gr.Radio(app_frontend['sources'], value=app_frontend['sources'][0], label="Sources", info="More sources will be added later!"),
        gr.Dropdown(app_frontend['jobs'], label="Job Title", info="More jobs will be added later!"),
        gr.File(file_count='single', file_types=['.pdf'], label="Resume PDF File", show_label=True),
        gr.Checkbox(value=False, label="Enable the resume-job match explanation feature", info="It takes approximately 5 minutes to run if enabled")
    ],
    outputs=[
        gr.Textbox(label="Salary Range Estimation", lines=1),
        gr.Textbox(label="Suitable Job Vacancy Sample", lines=3),
        gr.Textbox(label="Why the Resume and the Job Match", lines=16),
    ],
    examples=[
        [
            app_frontend['examples'][1]["source"], 
            app_frontend['examples'][1]["job_title"], 
            os.path.join(*app_frontend['examples'][1]["resume_path"]),
            app_frontend['examples'][1]["explanation_flag"], 
        ],
    ],
    title=app_frontend['title'],
    description=app_frontend['description'],
    allow_flagging="never",
)


if __name__ == "__main__":
    # To see changes in real-time, instead of the python command, use: gradio src\app\app.py
    # Use share=True to create a public link to share. This share link expires in 72 hours.
    demo.launch(share=False, server_name=app_config['host'], server_port=app_config['port'])

