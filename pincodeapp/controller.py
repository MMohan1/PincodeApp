

"""from elasticsearch import Elasticsearch
import pprint
import re
import string

es = Elasticsearch()

def my_strip(x):
    
    for i in x:
        if i in string.punctuation:
            x = x.replace(i,'')
    print x        
    return x


def auto_complete(key):

    query = {
   "size": 10,
      "query": {
      "match": {
         "job title":
        {
         "query":my_strip(key),
         "operator":"and",
      
         
         },
         
           },
      }}

    

    res = es.search(index="iam_doing",body=query)

    result = []

    for i in range(len(res['hits']['hits'])):
        each_res = {"job_id": res['hits']['hits'][i]['_source']["job id"],
                    "title": res['hits']['hits'][i]['_source']["job title"]
                    }
        

        result.append(each_res)

    return result"""
from pymongo import MongoClient
import csv

mongo_client = MongoClient()
db = mongo_client.pincode


def insertCsvtoMongo():
    if 'India_details' not in db.collection_names():
        with open('all_india_pin_code.csv') as f:
            records = csv.DictReader(f)
            db.India_details.insert(records)
            return
    else:
        return


def sendResult(parms):
    record = db.India_details.find(
        {"$or": [{'pincode': '504293'}, {'officename': ''}]}, {"_id": 0})
    out_put = [rec for rec in record]
    return out_put

if __name__ == "__main__":
    insertCsvtoMongo()
