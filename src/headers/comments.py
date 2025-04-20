from headers.people import Patient, Doctor
from headers.prompter import ask_claude

class Comment():
    def __init__(self, title: str, content: str, author: Patient, first: bool):
        self.title = title
        self.content = content
        self.patient = author
        self.response = None
        self.aicomment = None
    def add_response(self, response):
        self.response = response
    def view_aicomment(self):
        if self.aicomment is None:
            self.aicomment = ask_claude(self.content)
        return self.aicomment
# Response is an outline for how the doctor will reply to the comment, the patient can reply again if there is like a further additional question
class Response():
    def __init__(self, content: str, author: Doctor):
        self.content = content
        self.doctor = author
        self.comment = None
    def add_comment(self, comment):
        self.comment = comment