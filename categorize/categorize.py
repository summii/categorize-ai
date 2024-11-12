import json
import urllib.parse
from models import TaxonomyEmbeddings
from .openai import get_completions_openai, get_embeddings_openai

taxonomy_type = "crumb"
taxonomy_source = "google"
openai_model = "text-embedding-ada-002"

def insert_taxonomy_embeddings_from_file(text_data):
    taxonomy_type = "crumb"
    taxonomy_source = "google"
    openai_model = "text-embedding-ada-002"
    print(f"text_data: {text_data}")

    embeddings = get_embeddings_openai(text_data)
    print(f"embedding: {embeddings}")
    if(embeddings):
        success, error = TaxonomyEmbeddings.put_embeddings(text_data, taxonomy_type, taxonomy_source, openai_model, embeddings)
        if(success):
            print(f"Successfully inserted {text_data} into taxonomy_embeddings")
            return True, None
        else:
            print(f"Failed to insert {text_data} into taxonomy_embeddings")
            return False, error
    else:
            print(f"Failed to get embedding for {text_data}")
            return False, error

def get_matching_categories(text_data):
    crumb = get_completions_openai(text_data)
    vector = get_embeddings_openai(crumb)

    results, error = TaxonomyEmbeddings.get_nearset_category(openai_model,taxonomy_source, vector)
    if results:
        print(f"results for {crumb} are {results}")
        return results
    else:
        print(f"error retrieving matches")
    return None
