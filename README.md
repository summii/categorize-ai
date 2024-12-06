# Categorize AI

A FastAPI application that uses OpenAI to generate and match category taxonomies for given text inputs.

## Features

- Generate category breadcrumbs using OpenAI
- Store and match embeddings using pgvector
- Redis caching for improved performance
- RESTful API endpoints
- Swagger documentation

## Prerequisites

- Python 3.9+
- PostgreSQL with pgvector extension
- Redis
- OpenAI API key

## Local Development Setup

1. **Clone the repository**
2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
3. **Set up environment variables**
    create a .env file and add the following:   
    ```bash
    OPENAI_API_KEY=<your-openai-api-key>  
    REDIS_HOST=<your-redis-host>
    REDIS_PORT=<your-redis-port>
    REDIS_DB=<your-redis-db>
    REDIS_EXPIRE_TIME=<your-redis-expire-time>
    ```

4. **Run the application**
    ```bash
    uvicorn main:app --reload
    ```
5. **Run tests**
    ```bash
    pytest
    ```
The API will be available at `http://127.0.0.1:8000`

## API Documentation

Once the application is running, you can access:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Available Endpoints

- `GET /`: Root endpoint
- `GET /health`: Health check
- `POST /categorize`: Generate categories for given text
- `GET /redis-monitor`: Monitor Redis cache status

## Running Tests