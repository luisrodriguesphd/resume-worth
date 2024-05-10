import os
from typing import Union
from resume_worth.utils.utils import set_secrets
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain.prompts import load_prompt
from functools import lru_cache
import transformers


transformers.logging.set_verbosity_error()


#@lru_cache(maxsize=None)
def load_text_generation_model(
        model_provider:str='groq',
        model_name:str='llama3-8b-8192', 
        model_kwargs:dict={},
        generate_kwargs:dict={
                'temperature': 0.4,
            },
    ):
    """Function to load a text generation model according to the provider."""

    print(f"-> Load {model_name} text generation model from {model_provider}")

    if model_provider=="huggingface":
        return load_hf_text_generation_model_to_langchain(model_name, model_kwargs, generate_kwargs)

    elif model_provider=="groq":
        set_secrets()
        return load_groq_text_generation_model_to_langchain(model_name, model_kwargs, generate_kwargs)
        
    else:
        raise Exception("Sorry, the code has no support for this provider yet.")


def load_groq_text_generation_model_to_langchain(
        model_name:str='llama3-8b-8192',
        model_kwargs:dict={
                'top_k': 50, 
                'top_p': 0.95, 
                'max_new_tokens': 1024,
            },
        generate_kwargs:dict={ 
                'temperature': 0.4,
            }
    ):
    """
    Function to load a text generation model hosted on Groq to be used in LangChain.
    More info, see: https://console.groq.com/docs/quickstart
    """

    groq_api_key = os.environ.get('GROQ_API_KEY', None)
    if groq_api_key is None:
        raise ValueError("GROQ_API_KEY is not set.")

    groq = ChatGroq(model_name=model_name, model_kwargs=model_kwargs, **generate_kwargs, groq_api_key=groq_api_key)
    
    return groq


def load_hf_text_generation_model_to_langchain(
        model_name:str='gpt2', 
        model_kwargs:dict={
                'trust_remote_code': True,
            },
        generate_kwargs:dict={
                'top_k': 50, 
                'top_p': 0.95, 
                'temperature': 0.4, 
                'max_new_tokens': 1024,
            }
    ):
    """
    Function to load a text generation model hosted on Hugging Face to be used in LangChain.
    More info, see: https://python.langchain.com/docs/integrations/llms/huggingface_pipelines/
    """

    tokenizer = AutoTokenizer.from_pretrained(model_name, **model_kwargs)
    model = AutoModelForCausalLM.from_pretrained(model_name, **model_kwargs)
    
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer,
            return_full_text=False, do_sample=True, 
            **generate_kwargs,
            num_beams=1, repetition_penalty=1.1, num_return_sequences=1,
        )
    
    hf = HuggingFacePipeline(pipeline=pipe)
    
    return hf


def create_langchain_prompt_template_for_m4_ai_models(user_prompt: str, promp_path:str=None):
    """Function to create a LangChain prompt template for M4-AI text generation models"""

    template = f"<|im_start|>user\n{user_prompt}<|im_end|>\n<|im_start|>assistant\n"
    prompt = PromptTemplate.from_template(template)

    if promp_path:
        prompt.save(promp_path)
    
    return prompt


@lru_cache(maxsize=None)
def load_langchain_prompt_template(promp_path: str):
    """Function to load a LangChain prompt template"""
    
    prompt = load_prompt(promp_path)
    
    return prompt


def create_langchain_chain(prompt: PromptTemplate, text_generation_model: Union[HuggingFacePipeline, ChatGroq]):
    """
    Create a chain by composing the text generation model with a LangChain prompt template.
    More info, see: https://python.langchain.com/docs/integrations/llms/huggingface_pipelines/
    """
    chain = prompt | text_generation_model
    return chain
