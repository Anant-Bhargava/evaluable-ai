class ModelResponseObject:
    def __init__(self, response_id, response_text,input_object,model):
        self._response_id = response_id
        self._response_text = response_text
        self._input_object = input_object
        self._model = model
        