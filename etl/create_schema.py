from sqlalchemy import *
from dotenv import load_dotenv
load_dotenv()

database=os.environ['DB_NAME'], user=os.environ['DB_USER'], password=os.environ['DB_PASS'],host=os.environ['DB_HOST']

conn_str = f"postgresql://{user}:{password}@{host}/{database}"
engine = create_engine(conn_str)
connection = engine.connect()
metadata = MetaData()


first_tb = Table('correct_classification', metadata,
   Column('id', BIGINT, primary_key=True),
   Column('isbn10', TEXT, nullable=True),
   Column('title', TEXT, nullable=True),
   Column('subtitle', TEXT, nullable=True),
   Column('authors', TEXT, nullable=True),
   Column('categories', TEXT, nullable=True),
   Column('thumbnail', TEXT, nullable=True),
   Column('description', TEXT, nullable=True),
   Column('published_year', FLOAT, nullable=True),
   Column('average_rating', FLOAT, nullable=True),
   Column('num_pages', FLOAT, nullable=True),
   Column('ratings_count', FLOAT, nullable=True),
)


metadata.create_all(engine)
import os
path = os.getcwd()
