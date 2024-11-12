from models import BaseORM, Session

from sqlalchemy.sql import text
from sqlalchemy import Column, Integer, String, select, desc

from pgvector.sqlalchemy import Vector

class TaxonomyEmbeddings(BaseORM):
    __tablename__ = 'taxonomy_embeddings'
    id = Column(Integer, primary_key=True)
    text_data = Column(String, unique=True, nullable=False)
    taxonomy_type = Column(String(100), nullable=False)
    taxonomy_source = Column(String(100), nullable=False)
    openai_model = Column(String(100), nullable=False)
    embeddings = Column(Vector, nullable=False)

    @classmethod
    def put_embeddings(cls, text_data, taxonomy_type, taxonomy_source, openai_model, embedding):
        try:
            row = cls(text_data=text_data, taxonomy_type=taxonomy_type, taxonomy_source=taxonomy_source, openai_model=openai_model, embeddings=embedding)
            session = Session()
            session.add(row)
            session.commit()
            session.close()
            return True, None
        except Exception as e:
            session.rollback()
            return False, e

    @classmethod
    def get_nearset_category(cls, model, source, vector):
        try:
            session = Session()
            statement = text(""" 
            SELECT text_data, 1 - (embeddings <=> :vector) AS cosine_similarity
            FROM taxonomy_embeddings
            WHERE openai_model=:model
            AND taxonomy_source=:source
            ORDER BY cosine_similarity DESC
            LIMIT 5

            """)
            params = {
                'model': model,
                'source': source,
                'vector': str(vector)
            }

            result = session.execute(statement, params)
            session.close()
            return result.all(), None
        except Exception as e:
            return None, e