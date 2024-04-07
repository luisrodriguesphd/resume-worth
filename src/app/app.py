import gradio as gr
from resume_worth.utils.utils import get_params
from resume_worth.pipelines.information_retrieval.pipeline import retrieve_top_job_vacancy_info


params = get_params()
app_config = params['app_config']
app_backend = params['app_backend']
app_frontend = params['app_frontend']


def salary_estimator(job_title: str, resume: str):

    if job_title is None:
        return app_frontend['messages']['job_title_not_found']

    if len(resume) < app_backend['min_resume_size']:
        return app_frontend['messages']['salary_not_found']
    
    salaries = retrieve_top_job_vacancy_info(job_title, resume)

    return salaries[0]


def run():
    # See details in https://www.gradio.app/docs/interface
    app = gr.Interface(
        fn=salary_estimator, 
        inputs=[
            gr.Radio(app_frontend['jobs'], label="Job Title"),
            gr.Textbox(label="Resume", lines=10)
        ],
        outputs=[
            gr.Textbox(label="Estimate Salary", lines=1)
        ],
        title=app_frontend['title'],
        description=app_frontend['description'],
        allow_flagging="never"
    )

    # Use share=True to create a public link to share. This share link expires in 72 hours.
    app.launch(server_name=app_config['host'], server_port=app_config['port'])


if __name__ == "__main__":
    run()
