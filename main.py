import sys
import csv
from categorize import openai, categorize
from fastapi import FastAPI
from pydantic import BaseModel

class Product(BaseModel):
    name: str = "Atom LT Hoody Mens"
    description: str = "Light, versatile synthetically insulated hoody works as a midlayer and standalone. Atom Series: Synthetic insulated midlayers. | LT: Lightweight."
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Atom LT Hoody Mens",
                "description": "Light, versatile synthetically insulated hoody works as a midlayer and standalone. Atom Series: Synthetic insulated midlayers. | LT: Lightweight."
            }
        }

app = FastAPI(
    title="Product Categorization API",
    description="API for categorizing products based on their name and description",
    version="1.0.0"
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Categorize AI API",
        "version": "1.0.0",
        "status": "active"
    }

# --- Health check
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "OK"}

@app.post("/categorize",tags=["Categorization"],summary="Categorize a product",description="Takes a product name and description and returns matching categories")
async def categorize_product(product: Product):
    """
    Categorize a product based on its name and description.
    
    Args:
        product (Product): Product object containing name and description
        
    Returns:
        dict: Dictionary containing list of matching categories
    """
    text = product.name + ' ' + product.description
    crumb_data = categorize.get_matching_categories(text)
    
    # Convert crumb_data to a list if it's not already
    if not isinstance(crumb_data, list):
        crumb_data = list(crumb_data)
    
    # Ensure the response is a simple dictionary with JSON-serializable values
    return {
        "categories": [str(item) for item in crumb_data]
    }
@app.get("/redis-monitor")
async def monitor_redis():
    """Monitor Redis keys and values"""
    try:
        # Get all keys
        all_keys = redis_service.redis_client.keys("category*")
        
        # Create a dictionary of key-value pairs
        redis_data = {}
        for key in all_keys:
            value = redis_service.get_cache(key)
            ttl = redis_service.redis_client.ttl(key)
            redis_data[key] = {
                "value": value,
                "ttl": ttl
            }
        
        return {
            "status": "success",
            "total_keys": len(all_keys),
            "data": redis_data
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# if __name__ == "__main__":
#     with open('data/test.csv', 'r') as f:
#         reader = csv.reader(f)
#         headers = next(reader)
#         name_idx = headers.index('product_name')
#         description_idx = headers.index('product_description')
#         for row in reader:
#             name = row[name_idx]
#             description = row[description_idx]
#             text = name + ' '  + description
#             crumb_data = categorize.get_matching_categories(text)
