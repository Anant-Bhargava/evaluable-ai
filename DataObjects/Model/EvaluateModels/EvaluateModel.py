from abc import ABC, abstractmethod

from DataObjects.Model.model import Model

class EvaluateModel(Model):
   
    @abstractmethod
    def generate_evaluation(self, transpose_object_list):
        """
        Abstract method to generate a response from the model.

        :param input_object_array: An array of input objects to be processed by the model.
        """
        pass