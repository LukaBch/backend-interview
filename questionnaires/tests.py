from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from questionnaires.models import Questionnaire, Question, Answer


class AuthenticatedQuestionTest(APITestCase):
    username = "testuser"
    password = "<PASSWORD>"

    @classmethod
    def setUpTestData(cls) -> None:
        user = User.objects.create_user(username=cls.username, password=cls.password)
        questionnaire = Questionnaire.objects.create(name="ESG campaign", user=user)
        question_1 = Question.objects.create(
            index=1,
            type=Question.Type.FREE_TEXT,
            questionnaire=questionnaire,
            text="What is the weather like today?",
        )
        Answer.objects.create(question=question_1, index=1)

    def setUp(self):
        self.client.login(username=self.username, password=self.password)

    def test_can_see_questions(self):
        response = self.client.get("/questionnaires/questions/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["text"], "What is the weather like today?")
        self.assertEqual(response.json()[0]["status"], "UNANSWERED")

    def test_can_answer_questions(self):
        response = self.client.get("/questionnaires/questions/")
        self.assertEqual(response.status_code, 200)
        question_id = response.json()[0]["id"]
        text = "Hello"
        response = self.client.put(
            f"/questionnaires/questions/{question_id}/",
            data={
                "answers": [
                    {
                        "id": response.json()[0]["answers"][0]["id"],
                        "user_text": text,
                        "selected": True,
                    }
                ]
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/questionnaires/questions/")
        self.assertEqual(response.json()[0]["status"], "ANSWERED")
        self.assertEqual(response.json()[0]["answers"][0]["user_text"], text)


### TO DO ###
# Test /token route : an object ExpiringToken should be created with correct expiration date
# Test routes related to QuestionViewSet (GET/PUT)
# # with a valid token : should be able to GET/PUT
# # with an invalid token : should fail
# # with an expired token : should fail