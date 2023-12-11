from abc import abstractmethod, ABC


class Question(ABC):
    def __init__(self, data):
        self.id = data.get("id")
        self.question_text = data.get("question")
        self.answer = data.get("answer")
    
    @abstractmethod
    def send(self):
        pass
    @abstractmethod
    def check_answer(self, ans):
        pass
    
    def _validate_data(self):
        assert_type(self.id, int)
        assert_type(self.question_text, str)
    

class BoolQuestion(Question):
    possible_answers = {True: ["true", "נכון", 'אמת'],
                        False: ["false", "לא נכון", "שקר"]}
    
    def __init__(self, data):
        super().__init__(data)

    def send(self):
        return (f"{self.question_text} (נכון\לא נכון)")
    
    def check_answer(self, ans):
        ans = ans.lower()
        for k, v in self.possible_answers.items():
            if ans in v:
                return k is self.answer
        return None
    
    def _validate_data(self):
        super()._validate_data()
        assert_type(self.answer, bool)
    

class TextQuestion(Question):
    def __init__(self, data):
        super().__init__(data)

    def send(self):
        return self.question_text
    
    def check_answer(self, ans):
        return ans.lower() == self.answer
    
    def _validate_data(self):
        super()._validate_data()
        assert_type(self.answer, str)

class MultichoiceQuestion(Question):
    def __init__(self, data):
        self.choices = data.get("choices")
        super().__init__(data)

    def send(self):
        text = self.question_text + "\n"
        for count, q in enumerate(self.choices):
            text += f"\n{count}. {q}"
        return text
    
    def check_answer(self, ans):
        try:
            ans = int(ans)
        except ValueError:
            return None
        if len(self.choices) - 1 < ans or ans < 0:
            return None
        return ans == self.answer
    
    def _validate_data(self):
        super()._validate_data()
        assert_type(self.answer, int)
        assert_type(self.choices, list)


def question_factory(question_data):
    q_type = question_data["type"]
    if q_type == "bool":
        return BoolQuestion(question_data)
    elif q_type == "text":
        return TextQuestion(question_data)
    elif q_type == "multichoice":
        return MultichoiceQuestion(question_data)
    else:
        return ValueError(q_type)


def assert_type(obj, typ):
    """A helper function for validating the field types"""
    if not isinstance(obj, typ):
        raise TypeError(f"{obj} must by of type {typ}")
    

if __name__ == "__main__":
    t = MultichoiceQuestion({"id":0, "question":"what?",
                         "choices": ["a", "why?", "c", "d"],
                         "answer": 1})