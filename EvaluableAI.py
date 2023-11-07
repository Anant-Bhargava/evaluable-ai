import csv
import json
import os
from DataObjects.EvaluationObject import EvaluationObject

from DataObjects.Model.CandidateModels.llama2 import llama2
from DataObjects.Model.CandidateModels.mistral import mistral
from DataObjects.InputObject import InputObject
from DataObjects.Model.EvaluateModels.gpt4 import gpt4


class EvaluableAI:

    def __init__(self, config_file='model_env_config.json'):
            self.api_keys = {}
            self.evaluator_models =[]
            self.candidate_models =[]
            self.evaluation_objects=[]
            self.input_object:InputObject = None
            self.create_input_objects_from_csv("input_data.csv")
            self.load_api_keys(config_file)
            self.load_models()
            self.run_candidate_models()
            self.create_evaluation_objects()
            self.run_evaluation_models()

            
    
    def create_input_objects_from_csv(self,csv_filepath):
        input_objects_list :InputObject = []

        # Open the CSV file and read it
        with open(csv_filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            # Iterate over the rows in the CSV file
            for row in reader:
                # Create an InputObject from the data in the current row
                row_object = InputObject(input_text=row['instruction'], context=row['context'])
                input_objects_list.append(row_object)
            self.input_object= input_objects_list

        return 

    


    def load_api_keys(self, config_file):
        # Read the JSON configuration file
        try:
            with open(config_file, 'r') as file:
                config = json.load(file)
            # Get API keys from environment variables
            for model in config['models']:
                name = model['name']
                env_var_name = model.get('environment_variable_name')
                if env_var_name:
                    # Retrieve API key from environment variable
                    self.api_keys[name] = os.getenv(env_var_name, default=None)
                else:
                    # Directly use the API key specified in the JSON
                    self.api_keys[name] = model.get('api_key')
        except FileNotFoundError:
            print(f"Configuration file {config_file} not found.")
        except json.JSONDecodeError as err:
            print(f"Error parsing JSON file: {err}")
        except Exception as e:
            print(f"An error occurred: {e}")
        

    def load_models(self):
        #load candidate models 
        llama2_candidate_model = llama2(name="llama2",key=self.api_keys["LLAMA2"])
        mistral_candidate_model = mistral(name="mistral",key=self.api_keys["LLAMA2"])
        self.candidate_models.append(llama2_candidate_model)
        self.candidate_models.append(mistral_candidate_model)


        #load evaluation model
        openai_eval_model = gpt4("openai",self.api_keys["OPENAI"])
        self.evaluator_models.append(openai_eval_model)
    
    def run_candidate_models(self):
        for model in self.candidate_models:
            model.generate_response(self.input_object)
    
    def run_evaluation_models(self):
        for model in self.evaluator_models:
            model.generate_evaluation(self.evaluation_objects)
    
    def create_evaluation_objects(self):
        transposed_data = {}
        evaluation_objects = []
        # Iterate over each model object
        for model in self.candidate_models:
            # Iterate over each response in the model's response list
            for response in model._response_list:
                
                # Use the input_id from the input_object as the key
                input_id = response._input_object._input_id

                # If the input_id is not already in the dictionary, create a new list
                if input_id not in transposed_data:
                    transposed_data[input_id] = {
                        'input_text': response._input_object.input_text,
                        'context': response._input_object.context,
                        'responses': []
                    }

                # Append the current ModelResponseObject to the list for this input_id
                transposed_data[input_id]['responses'].append(response)

        # Create EvaluationObject instances
        for input_id, data in transposed_data.items():
            evaluation_object = EvaluationObject(
                input_id=input_id,
                input_text=data['input_text'],
                context=data['context'],
                responses=data['responses']
            )
            print(repr(evaluation_object))
            evaluation_objects.append(evaluation_object)
            self.evaluation_objects= evaluation_objects
        return 
    

    

