import json
from question import question_factory


class Trivia:
    def __init__(self):
        self.questions = []
        self.users = {}
        self._get_questions()
    
    def add_user(self, id):
        self.users[id] = 0
    
    def send_question(self, user_id):
        if user_id not in self.users:
            return None
        question_index = self.users[user_id]
        if question_index > len(self.questions):
            return "Done"
        return self.questions[question_index].send()
    
    def get_answer(self, user_id, ans):
        if user_id not in self.users:
            return None
        question_index = self.users[user_id]
        if question_index > len(self.questions):
            return "Done"
        if self.questions[question_index].check_answer(ans):
            self.users[user_id] += 1
            return True
        return False
    
    def _get_questions(self):
        with open("questions.json", "r") as f:
            questions_data = json.load(f)["questions"]
            for question_data in questions_data:
                self.questions.append(question_factory(question_data))
