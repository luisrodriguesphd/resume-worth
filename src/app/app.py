import gradio as gr
from resume_worth.utils.utils import get_params
from resume_worth.pipelines.information_retrieval.pipeline import retrieve_top_job_vacancy_info


params = get_params()
APP_TITLE = params['APP_TITLE']
APP_DESCRIPTION = params['APP_DESCRIPTION']
JOB_TITLES = params['JOB_TITLES']
HOST = params['HOST']
PORT = params['PORT']


def salary_estimator(job_title, resume):

    salaries = retrieve_top_job_vacancy_info(job_title, resume)

    return salaries[0]


def run():
    # See details in https://www.gradio.app/docs/interface
    app = gr.Interface(
        fn=salary_estimator, 
        inputs=[
            gr.Radio(JOB_TITLES, label="Job Title"),
            gr.Textbox(label="Resume", lines=10)
        ],
        outputs=[
            gr.Textbox(label="Estimate Salary", lines=1)
        ],
        title=APP_TITLE,
        description=APP_DESCRIPTION,
        allow_flagging="never"
    )

    # Use share=True to create a public link to share. This share link expires in 72 hours.
    app.launch(server_name=HOST, server_port=int(PORT))


if __name__ == "__main__":
    run()
