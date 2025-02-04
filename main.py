from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel
from dotenv import load_dotenv

MASTER_CONN = connect_db()

def connect_db():
    load_dotenv()
    conn = psycopg2.connect(
        host=os.getenv('PSQL_HOST'),
        port=os.getenv('PSQL_PORT'),
        database=os.getenv('PSQL_DATABASE'),
        user=os.getenv('PSQL_USERNAME'),
        password=os.getenv('PSQL_PASSWORD')
    )
    return conn

app = FastAPI()

class Input(BaseModel):
    sire_name: str
    sire_yob: int
    dam_name: str
    dam_yob: int
    sex: str
    year_born: int
    
@app.post("/predict")
def predict(input: Input):
    return {"result": input}
