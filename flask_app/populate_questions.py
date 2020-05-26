from pymongo import MongoClient
import pandas
from pandas.io import json as pjson
import os

db_host=os.environ['MONGODB_HOST']
db_name=os.environ['MONGODB_NAME']
db_url = 'mongodb://'+db_host+':27017'


client = MongoClient(db_url)
db = client[db_name]
question_db = db["questions"]

######
# insert questions flat structure to the mongo DB
######

## clean all the previous questions and insert again
question_db.delete_many({})

loc = "/app/flask_app/Questions_v1.xlsx"
excel_data_df = pandas.read_excel(loc, sheet_name='Questions')
json_str = excel_data_df.to_json(orient='records')
question_db.insert_many(pjson.loads(json_str))