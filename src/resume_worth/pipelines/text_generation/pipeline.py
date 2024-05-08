"""
Text Generation Pipeline

This pipeline utilizes an LLM to explain why the retrieved job vacancy is a good fit for the user's resume.
"""


import os
from resume_worth.utils.utils import get_params
from resume_worth.pipelines.text_generation.nodes import load_hf_text_generation_model_to_langchain, load_langchain_prompt_template, create_langchain_chain


params = get_params()
generative_model = params['generative_model']
prompt_dir = params['prompt_dir']
promp_file = params['promp_file']


def generate_explanation_why_resume_for_a_job(resume: str, job: str):

    # Stage 1 - [cacheable] Load text generation model

    text_generation_model = load_hf_text_generation_model_to_langchain(generative_model['model_name'], generative_model['model_kwargs'], generative_model['generate_kwargs'])

    # Stage 2 - [cacheable] Load text generation model
    
    promp_path = os.path.join(prompt_dir, promp_file)
    prompt_template = load_langchain_prompt_template(promp_path)

    # Stage 3 - Create a chain by composing the prompt and model
    
    text_generation_chain = create_langchain_chain(prompt_template, text_generation_model)

    # Stage 4 - Generate the answer by involking the create chain

    answer = text_generation_chain.invoke({"resume": resume, "job": job})

    return answer


if __name__ == "__main__":

    # EXAMPLE

    resume =  """Luis Antonio Rodrigues is an accomplished data scientist and machine learning engineer with over eight years of experience in developing innovative machine learning products and services. He holds a BSc in Mathematics, an MSc, and a PhD in Mechanical Engineering from the University of Campinas, one of the most renowned universities in Latin America. Luis's expertise spans across various domains including Natural Language Processing (NLP), Recommender Systems, Marketing and CRM, and Time-Series Forecasting, with significant contributions across Banking, Consumer Packaged Goods, Retail, and Telecommunications industries.
    Currently serving as a Principal Data Scientist at DEUS, an AI firm dedicated to human-centered solutions, Luis plays a crucial role in the development of a cutting-edge Retrieval-Augmented Generation (RAG) solution. His responsibilities include improving the knowledge-to-text module, optimizing information retrieval for efficiency and precision, and enhancing text generation for real-time accuracy,  showcasing his skills in RAG, IR, LLM, NLP, and several tools and platforms. Additionally, he has contributed as a Data Architect in designing a medallion architecture for a Databricks lakehouse on AWS.
    Previously, Luis held the position of Principal Data Consultant at Aubay Portugal, where he led an NLP project for Banco de Portugal, focusing on AI services such as summarization, information extraction, complaint text classification, and financial sentiment analysis. At CI&T, as Lead Data Scientist, he was instrumental in developing a recommender system for Nestlé, resulting in a 6% sales increase. During his time at Propz, he developed a recommender system for Carrefour, which boosted revenue by 3%.
    His earlier roles include a researcher at I.Systems, focusing on water distribution systems, and at the University of Campinas, where his work centered on system and control theory. Luis's proficiency is further demonstrated by his certifications in MLOps with Azure Machine Learning, TensorFlow 2.0, and Python for Time Series Data Analysis. Luis combines his deep technical knowledge with strong communication skills to lead teams and projects towards achieving significant business impacts."""

    job = """Design, develop, and deploy machine learning models and algorithms for complex and unique datasets, using various techniques such as mathematical modeling, scikit-learn, NLP, CNN, RNN, DL, RL, Transformers, GAN, LLM, RAG
    Collaborate with cross-functional teams to extract insights, identify business opportunities and provide data-driven recommendations
    Stay up-to-date with the latest machine learning and AI techniques and tools
    Communicate complex technical concepts to non-technical stakeholders in an easy-to-understand manner
    Bachelor's degree or higher in Computer Science, Mathematics, Statistics, Actuarial Science, Informatics, Information Science or related fields
    Strong analytical skills and attention to detail
    Participation in Kaggle, Mathematics Olympiad or similar competitions is a plus
    Excellent programming skills in Python, R, Java, or C++\nFamiliar with ML frameworks such as Tensorflow, Keras, PyTorch, MLFlow, AutoML, TensorRT, CUDA
    Excellent communication and collaboration skills\nExperience with designing, training, and deploying machine learning models
    Customer centric and committed to deliver the best AI results to customers"""

    answer = generate_explanation_why_resume_for_a_job(resume, job)

    print(answer)
