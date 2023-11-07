import uuid

class InputObject:
    def __init__(self, input_text, context, input_id=None):
        self._input_id = input_id if input_id is not None else uuid.uuid4()
        self._input_text = input_text
        self._context = context

    @property
    def input_id(self):
        return self._input_id

    @input_id.setter
    def input_id(self, value):
        raise ValueError("input_id cannot be changed once set.")

    @property
    def input_text(self):
        return self._input_text

    @input_text.setter
    def input_text(self, value):
        self._input_text = value

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, value):
        self._context = value