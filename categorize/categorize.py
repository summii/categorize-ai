import json
import urllib.parse
from models import TaxonomyEmbeddings
from services.redis_service import RedisService
from .openai import get_completions_openai, get_embeddings_openai

taxonomy_type = "crumb"
taxonomy_source = "google"
openai_model = "text-embedding-ada-002"
redis_service = RedisService()

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
    # Try to get the data from cache first
    cache_key = f"category_match:{text_data}"
    cached_results = redis_service.get_cache(cache_key)

    # Add debug logging
    print(f"\nRedis Debug:")
    print(f"Cache Key: {cache_key}")
    print(f"Cached Results: {cached_results}")
    if cached_results:
        print("Retrieved results from cache")
        return cached_results
    
    crumb = get_completions_openai(text_data)   
    vector = get_embeddings_openai(crumb)


    results, error = TaxonomyEmbeddings.get_nearset_category(openai_model,taxonomy_source, vector)
    if results:
        # Convert SQLAlchemy Row objects to serializable format
        serializable_results = [
            {
                'text_data': row[0],
                'cosine_similarity': float(row[1])  # Convert Decimal to float
            }
            for row in results
        ]
        
        # store in cache
        redis_service.set_cache(cache_key, serializable_results)
        print(f"Stored in Redis: {serializable_results}")
        return serializable_results
    else:
        print(f"error retrieving matches")
    return None
