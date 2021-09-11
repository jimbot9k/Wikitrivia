"""
Question - A question generated from Wikipedia
"""
class Question:

    def __init__(self, question, content, answer, falseAnswers):
        self.question = question
        self.content = content
        self.answer = answer
        self.falseAnswers = falseAnswers

    def get_question(self):
        return self.question

    def get_content(self):
        return self.content

    def get_answer(self):
        return self.answer

    def get_falseAnswers(self):
        return self.falseAnswers
