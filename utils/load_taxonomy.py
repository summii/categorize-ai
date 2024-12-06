import sys
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from categorize.openai import get_completions_openai, get_embeddings_openai
from models import TaxonomyEmbeddings

def insert_taxonomy_embeddings_from_file(text_data):
    try:
        taxonomy_type = "crumb"
        taxonomy_source = "google"
        openai_model = "text-embedding-ada-002"
        print(f"Processing text_data: {text_data}")

        embeddings = get_embeddings_openai(text_data)
        if embeddings is None:
            logger.error("Failed to get embeddings from OpenAI")
            return False, "Failed to get embeddings from OpenAI"

        # logger.info(f"Got embeddings of length: {len(embeddings)}")

        try:
            success, error = TaxonomyEmbeddings.put_embeddings(
                text_data, 
                taxonomy_type, 
                taxonomy_source, 
                openai_model, 
                embeddings
            )
            
            if success:
                logger.info(f"Successfully inserted: {text_data}")
                return True, None
            else:
                logger.error(f"Database insertion failed: {error}")
                return False, error
                
        except Exception as e:
            logger.error(f"Error during database insertion: {str(e)}")
            return False, str(e)

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return False, str(e)

if __name__ == "__main__":

    with open('data/taxonomy.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            insert_taxonomy_embeddings_from_file(line)

    #         total = len(lines)
    #         success_count = 0
            
    #         logger.info(f"Found {total} categories to process")
            
    #         for i, line in enumerate(lines, 1):
    #             line = line.strip()
    #             if not line:  # Skip empty lines
    #                 continue
                    
    #             logger.info(f"Processing {i}/{total}: {line}")
    #             success, error = insert_taxonomy_embeddings_from_file(line)
                
    #             if success:
    #                 success_count += 1
    #             else:
    #                 logger.error(f"Failed to process '{line}': {error}")
                    
    #         logger.info(f"\nCompleted: {success_count} out of {total} categories inserted successfully")
            
    # except Exception as e:
    #     logger.error(f"Error reading file: {str(e)}")