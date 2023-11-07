import requests
from DataObjects.EvaluationObject import EvaluationObject
from DataObjects.Model.EvaluateModels.EvaluateModel import EvaluateModel
import uuid
import json

from DataObjects.ModelResponseObject import ModelResponseObject


class gpt4(EvaluateModel):
    def __init__(self, name, key):
        self._model_name = name
        self._api_key = key
    
    @property
    def model_name(self):
        return self._model_name

    @property
    def api_key(self):
        return self._api_key
    
    def generate_evaluation(self, evaluation_objects):
        evaluations = []

        for evaluation_object in evaluation_objects:
            # Extracting the input, context, and responses from the provided object
            input_text = evaluation_object.input_text
            context = evaluation_object.context
            responses = evaluation_object.responses

            # Constructing the evaluation prompt
            prompt = f"Given the input: '{input_text}' and the context: '{context}', evaluate the following responses:\n\n"
            for idx, response_obj in enumerate(responses, start=1):
                response_text = response_obj._response_text
                prompt += f"Response {idx}: {response_text}\n"

            # Adding instructions for the evaluation at the end of the prompt
            prompt += """\nPlease evaluate each response for accuracy, relevance, and coherence. Give a score for each response for accuracy, relevance and coherence on a grade of 1 to 10 and then a final score for each response out of 10 based on 60 percent accuracy, 20 percent relevance and 20 percent coherence in the following json format  
            Score:{
            "Accuracy": 5,
            "Relevance": 5,
            "Coherence": 5,
            "Overall": 5
            } Only give json back in output
            """

            # Define the headers and data to send in the POST request
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f"Bearer {self.api_key}",  # Replace with your actual API key
            }
            print(self.api_key)
            data = {
                'model': 'gpt-3.5-turbo',  # or the latest available model
                'messages': [
                    {
                        "role": "user",
                        "content":prompt
                    }
                ],
                'temperature': 0.2,  # Adjust as needed for creativity vs. precision
                'max_tokens': 2000,  # Adjust as needed based on expected length of evaluation
            }

            # Sending the prompt to the OpenAI API for evaluation
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, data=json.dumps(data))

            # Check if the request was successful
            if response.status_code == 200:
                # Append the evaluated text to the evaluations list
                evaluations.append(response.json()['choices'][0]['text'].strip())
            else:
                # If the call failed, append the error to the evaluations list
                evaluations.append(f"Error: {response.status_code}, {response.text}")

        return evaluations
        