from abc import ABC, abstractmethod

from DataObjects.Model.model import Model

class CandidateModel(Model):
    

    @abstractmethod
    def generate_response(self, input_object_array):
        """
        Abstract method to generate a response from the model.

        :param input_object_array: An array of input objects to be processed by the model.
        """
        pass