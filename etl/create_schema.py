from pickle import BYTEARRAY8
from sqlalchemy import *
from dotenv import load_dotenv
load_dotenv()
import os

database=os.environ['DB_NAME'] 
user=os.environ['DB_USER']
password=os.environ['DB_PASS']
host=os.environ['DB_HOST']

conn_str = f"postgresql://{user}:{password}@{host}/{database}"
engine = create_engine(conn_str)
connection = engine.connect()
metadata = MetaData()


first_tb = Table('correct_classification_test', metadata,
   Column('predicted', INT, nullable=True),
   Column('correct', INT, nullable=True),
   Column('image', LargeBinary, nullable=True),
)


metadata.create_all(engine)