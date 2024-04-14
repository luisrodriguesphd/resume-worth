import os
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_core.prompts import PromptTemplate
from langchain.prompts import load_prompt
from functools import lru_cache
import transformers


transformers.logging.set_verbosity_error()


@lru_cache(maxsize=None)
def load_hf_text_generation_model_to_langchain(model_id:str='gpt2', top_k:int=50, top_p:float=0.95, temperature:float=0.4, max_new_tokens:int=1024):
    """
    Function to load a text generation model hosted on Hugging Face to se used in LangChain.
    More info, see: https://python.langchain.com/docs/integrations/llms/huggingface_pipelines/
    """

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id)
    
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, 
            return_full_text=False, do_sample=True, 
            top_p=top_p, top_k=top_k, temperature=temperature, max_new_tokens=max_new_tokens, 
            num_beams=1, repetition_penalty=1.1, num_return_sequences=1
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


def create_langchain_chain(prompt: PromptTemplate, hf_text_generation: HuggingFacePipeline):
    """
    Create a chain by composing the HF text generation model with a LangChain prompt template.
    More info, see: https://python.langchain.com/docs/integrations/llms/huggingface_pipelines/
    """
    chain = prompt | hf_text_generation
    return chain