from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from config import DATABASE_URL
import os

"""
Creates a SQLAlchemy engine for connecting to the 'embeddings' database using the PostgreSQL driver and the specified connection details.
"""
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL, echo=False)

# with engine.connect() as conn:
#     conn = conn.execution_options(isolation_level="AUTOCOMMIT")
#     result = conn.execute(text("SELECT 1 FROM pg_database WHERE datname = 'embeddings';"))
#     exists = result.scalar()  # Check if any rows were returned
#     if not exists:
#         conn.execute(text("CREATE DATABASE embeddings;"))
#     else:
#         print("Database 'embeddings' already exists.")

Session = sessionmaker(bind=engine)
BaseORM = declarative_base()

from .taxonomy_embeddings import TaxonomyEmbeddings
