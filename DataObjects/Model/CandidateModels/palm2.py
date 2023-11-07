import requests
from DataObjects.Model.CandidateModels.CandidateModel import CandidateModel


class palm2(CandidateModel):
    def __init__(self, name, key):
        self._model_name = name
        self._api_key = key
    
    @property
    def model_name(self):
        return self._model_name

    @property
    def api_key(self):
        return self._api_key
    
   
    def generate_query(input_list):
        query_list = []
        for input_object in input_list:
            # Construct the query string as specified
            query  = f'''{{
                "prompt": {{
                    "text": "{input_object['input']}"
                }},
                "temperature": 1.0,
                "candidateCount": 2
            }}'''
            query_list.append(query)
        return query_list


    def generate_response(self, input_list):
        response_list =[]
        API_URL = "https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText?key="+ self.api_key
        headers = {"Content-Type": "application/json"}
        query_list= self.generate_query(input_list)
        for query in query_list:
            response = requests.post(API_URL, headers=headers, json=query)
            response_list.append(response.json())
        return response_list