from PIL import Image
from imgbeddings import imgbeddings
from elasticsearch import Elasticsearch
from os import listdir, environ
from os.path import isfile, join
import hashlib

es_url = environ.get("ES_URL")
if not es_url:
  print("You must supply an ES_URL environment variable with details of your Elasticsearch deployment")
  exit()

es = Elasticsearch(es_url, verify_certs=False)

request_body = {
  'mappings': {
	  'properties': {
	    'embeddings': {'dims':768, 'type': 'dense_vector','similarity':'cosine', 'index':True},
      'desc': {'type': 'text'} 
	  }
  }
}
try:
  print("creating index...")
  es.indices.create(index = 'images', body = request_body)
except Exception as e: 
  print(e)
  # except:
  print("Error creating.. probably already there")



def create_id(filepath):
  h = hashlib.new('sha256')
  h.update(filepath.encode()) 
  return h.hexdigest()

def generate(filename):
  ibed = imgbeddings()
  image = Image.open(filename)
  embedding = ibed.to_embeddings(image)
  #print(len(embedding))
  return embedding[0]

mypath = "./images"

for d in listdir(mypath):
  images_dir= join(mypath,d)
  print (images_dir)
  for f in listdir(images_dir):
    file_path=join(images_dir, f)
    print (file_path)
    file_id = create_id(file_path)
    try:
      if not es.exists(index="images", id=file_id):
        try:
          print("Generating embeddings...")
          e = generate(file_path)
          doc = {"embeddings": e, "desc":d, "file_path": file_path}
          print("Uploading ", file_id)
          es.create(index="images",id=file_id, document=doc)
        except:
          print("error generating embeddings or uploading... skipping")
      else:
        print("Doc already exists in index... skipping")
    except:
      print("Some other problem... trying to continue...")  
