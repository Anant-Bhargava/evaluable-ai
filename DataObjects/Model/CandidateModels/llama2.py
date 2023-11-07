import requests
from DataObjects.ModelResponseObject import ModelResponseObject
from DataObjects.Model.CandidateModels.CandidateModel import CandidateModel
import uuid
import json


class llama2(CandidateModel):
    def __init__(self, name, key):
        self._model_name = name
        self._api_key = key
        self._response_list = None
    
    @property
    def model_name(self):
        return self._model_name

    @property
    def api_key(self):
        return self._api_key
    
    @property
    def response_list(self):
        return self._response_list
    
   
    def generate_response(self, input_list):
        response_list: ModelResponseObject =[]
        API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"
        headers = {"Authorization": "Bearer "+ self.api_key}
        
        for input_object in input_list:
            # Construct the query string as specified
            #query = f"{{\"inputs\": \"Who founded google?\"}}"
            query = f"{{\"inputs\": \"answer: {input_object.input_text} using the given context: {input_object.context}\"}}"
            query =json.loads(query)
            #print(query) #add exception for 400, and pass on 200. Check for blank response also
            response = requests.post(API_URL, headers=headers, json=query)
            response_id = uuid.uuid4()
            #print(response.json())
            #print(json.loads(response.content.decode("utf-8")))
            model_response_object = ModelResponseObject(response_id,response.json(),input_object,self)
            response_list.append(model_response_object)
        self._response_list=response_list
        return 
    