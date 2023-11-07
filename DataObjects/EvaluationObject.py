class EvaluationObject:
    def __init__(self, input_id, input_text, context, responses):
        self.input_id = input_id
        self.input_text = input_text
        self.context = context
        self.responses = responses

    def __repr__(self):
        return f"EvaluationObject(input_id={self.input_id}, input_text='{self.input_text}', context='{self.context}', responses={self.responses})"