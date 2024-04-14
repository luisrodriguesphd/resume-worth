import os
import yaml
from langchain_community.embeddings import HuggingFaceEmbeddings


def get_params():
    """
    Function to get the parameters.
    It load and parse the parameters from params.yml file.
    """

    params_path = os.path.join("conf", "params.yml")
    with open(params_path) as f:
        try:
            params = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise(e)
    
    for k, v in params.items():
        if "_dir" in k.lower():
            params[k] = os.path.join(*params[k])

    return params 


def load_embedding_model(model_name: str = "sentence-transformers/all-mpnet-base-v2", model_kwargs: dict={}, encode_kwargs: dict={}):
    """Load a pretrained text embedding model"""

    embedding_model = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
    )

    return embedding_model
