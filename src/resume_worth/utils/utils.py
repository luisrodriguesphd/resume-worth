import os
import yaml
from langchain_community.embeddings import HuggingFaceEmbeddings


def get_params():
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


def load_embedding_model(model_name: str = "sentence-transformers/all-mpnet-base-v2"):
    """ Load a pretrained text embedding model"""

    embedding_model = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': False}
    )

    return embedding_model
