
"""     Fast Start Example #5 - RAG with Semantic Query

    This example illustrates the most common RAG retrieval pattern, which is using a semantic query, e.g.,
    a natural language query, as the basis for retrieving relevant text chunks, and then using as
    the context material in a prompt to ask the same question to a LLM.

    In this example, we will show the following:

    1.  Create library and install embeddings (feel free to skip / substitute a library created in an earlier step).
    2.  Ask a general semantic query to the entire library collection.
    3.  Select the most relevant results by document.
    4.  Loop through all of the documents - packaging the context and asking our questions to the LLM.

"""


import os
from llmware.library import Library
from llmware.retrieval import Query
from llmware.setup import Setup
from llmware.status import Status
from llmware.prompts import Prompt
from llmware.configs import LLMWareConfig


def semantic_rag (library_name, embedding_model_name, llm_model_name):

    """ Illustrates the use of semantic embedding vectors in a RAG workflow
        --self-contained example - will be duplicative with some of the steps taken in other examples """

    # Step 1 - Create library which is the main 'organizing construct' in llmware
    print ("\nupdate: Step 1 - Creating library: {}".format(library_name))

    library = Library().create_new_library(library_name)

    # Step 2 - Pull down the sample files from S3 through the .load_sample_files() command
    #   --note: if you need to refresh the sample files, set 'over_write=True'
    print ("update: Step 2 - Downloading Sample Files")

    sample_files_path = Setup().load_sample_files(over_write=False)
    contracts_path = os.path.join(sample_files_path, "Agreements")

    # Step 3 - point ".add_files" method to the folder of documents that was just created
    #   this method parses all of the documents, text chunks, and captures in MongoDB
    print("update: Step 3 - Parsing and Text Indexing Files")

    library.add_files(input_folder_path=contracts_path)

    # Step 4 - Install the embeddings
    print("\nupdate: Step 4 - Generating Embeddings in {} db - with Model- {}".format(vector_db, embedding_model))

    library.install_new_embedding(embedding_model_name=embedding_model_name, vector_db=vector_db)

    # RAG steps start here ...

    print("\nupdate: Loading model for LLM inference - ", llm_model_name)

    prompter = Prompt().load_model(llm_model_name)

    query = "what is the executive's base annual salary"

    #   key step: run semantic query against the library and get all of the top results
    results = Query(library).semantic_query(query, result_count=50, embedding_distance_threshold=1.0)

    #   if you want to look at 'results', uncomment the two lines below
    #   for i, res in enumerate(results):
    #       print("update: ", i, res["file_source"], res["distance"], res["text"])

    for i, contract in enumerate(os.listdir(contracts_path)):

        qr = []

        if contract != ".DS_Store":

            print("\nContract Name: ", i, contract)

            #   we will look through the list of semantic query results, and pull the top results for each file
            for j, entries in enumerate(results):

                library_fn = entries["file_source"]
                if os.sep in library_fn:
                    # handles difference in windows file formats vs. mac / linux
                    library_fn = library_fn.split(os.sep)[-1]

                if library_fn == contract:
                    print("Top Retrieval: ", j, entries["distance"], entries["text"])
                    qr.append(entries)

            #   we will add the query results to the prompt
            source = prompter.add_source_query_results(query_results=qr)

            #   run the prompt
            response = prompter.prompt_with_source(query, prompt_name="default_with_context", temperature=0.3)

            #   note: prompt_with_resource returns a list of dictionary responses
            #   -- depending upon the size of the source context, it may call the llm several times
            #   -- each dict entry represents 1 call to the LLM

            for resp in response:
                if "llm_response" in resp:
                    print("\nupdate: llm answer - ", resp["llm_response"])

            # start fresh for next document
            prompter.clear_source_materials()

    return 0


if __name__ == "__main__":

    LLMWareConfig().set_active_db("sqlite")

    #   for this example, we will use an embedding model that has been 'fine-tuned' for contracts
    embedding_model = "industry-bert-contracts"

    #   note: "faiss" is being used for fast start / no set-up required - we would recommend installing
    #   a proper vector db for greater scalability and performance
    vector_db = "faiss"

    # pick any name for the library
    lib_name = "example5_library"

    example_models = ["llmware/bling-1b-0.1", "llmware/bling-tiny-llama-v0", "llmware/dragon-yi-6b-gguf"]

    # use local cpu model
    llm_model_name = example_models[0]

    #   to swap in a gpt-4 openai model - uncomment these two lines
    #   llm_model_name = "gpt-4"
    #   os.environ["USER_MANAGED_OPENAI_API_KEY"] = "<insert-your-openai-key>"

    semantic_rag(lib_name, embedding_model, llm_model_name)



