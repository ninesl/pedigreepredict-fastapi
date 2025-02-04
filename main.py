'''
Script responsible for HTTP requests to the ML pedigree microservice
usage: `fastapi {dev}/{run} repos/py-pedigree-connect/main.py`
remeber to check host:8000/docs and /redoc
'''

import os
import psycopg2
from fastapi import FastAPI
# from typing import Union
from pydantic import BaseModel
from dotenv import load_dotenv
from predict import PedigreePredictor, PedigreeDataLoader, PedigreeFetcher


def connect_db():
    '''connect to the db based on .env'''
    load_dotenv()
    conn = psycopg2.connect(
        host=os.getenv('PSQL_HOST'),
        port=os.getenv('PSQL_PORT'),
        database=os.getenv('PSQL_DATABASE'),
        user=os.getenv('PSQL_USERNAME'),
        password=os.getenv('PSQL_PASSWORD')
    )
    return conn


fetcher = PedigreeFetcher(conn=connect_db())
loader = PedigreeDataLoader(fetcher=fetcher)
predictor = PedigreePredictor()
app = FastAPI()


class Input(BaseModel):
    '''auto serialzes into JSON automagically. input is for predictions'''
    sire_name: str
    sire_yob: int
    dam_name: str
    dam_yob: int
    sex: str
    year_born: int


@app.post("/predict")
def predict(data: Input):
    '''pass in input, get giant JSON blob back'''
    global fetcher
    # input_data = loader.build_input_dict(data) #explicity declare this.

    for sex in ['Male', 'Female', 'Gelding']:
        data.sex = sex
        input_data = loader.build_input_dict(data)
        predictions = predictor.predict(input_data)

        print(f"\n\033[1m{sex.upper()}\nby {input_args.sire_name}, out of {input_args.dam_name}")
        print_predictions(predictions)
        print("-" * 80)
    fetcher.print_pedigree_details(input_data)
    print("\n" * 10)
    return {"result": data}
