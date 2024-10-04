class TestQuestion:
    def __init__(self, questionType, number, question, correct):
        self.questionType = questionType # TF or MC
        self.number = number # Question number
        self.question = question # Text of question
        self.correct = correct # The letter answer

class TfQuestion(TestQuestion):
    """True or False Question. Correct = either True or False boolean value"""
    def __init__(self, number, question, correct):
        super().__init__("TF", number, question, correct)
 

class McQuestion(TestQuestion):
    """Multiple Choice Question. Correct = the letter of the correct answer"""
    def __init__(self, number, question, correct, a, b, c, d, e):
        super().__init__(number, question, correct)
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
