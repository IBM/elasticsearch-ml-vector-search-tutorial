from PIL import Image
from imgbeddings import imgbeddings
from os import environ
import json
import requests
import sys


def generate(filename):
  #this function generates the embeddings for a single file
  ibed = imgbeddings()
  image = Image.open(filename)
  embedding = ibed.to_embeddings(image)
  return embedding[0]



#requires a file name to search for similarities
if len(sys.argv) != 2:
  print("syntax python3 search.py <filename>")
  sys.exit(1)  
filename = sys.argv[1]

#requires an env variable with the URL of the Elasticsearch instance
es_url = environ.get("ES_URL")
if not es_url:
  print("You must supply an ES_URL environment variable with details of your Elasticsearch deployment")
  sys.exit(2)

e = generate(filename).tolist()

q = {
  "knn": {
    "field": "embeddings",
    "query_vector": e,
    "k": 1,
    "num_candidates": 1
  },
  "fields":["desc", "file_path"],
   "_source": False
}

#this section generates an http request to the ES API to execute the search
headers = {'Content-Type': 'application/json'}
response = requests.get(es_url+'/birds/_search', data=json.dumps(q), headers=headers, verify=False)
print(json.dumps(response.json()))