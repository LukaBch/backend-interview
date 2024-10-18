from rest_framework import serializers

from questionnaires.models import Questionnaire, Answer, Question


class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = ["id", "name", "status"]


class AnswerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()  # Ensure the id is available for the save method

    class Meta:
        model = Answer
        fields = ["id", "index", "text", "user_text", "selected"]
        read_only_fields = ["index", "text"]


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "text", "hint", "index", "type", "status", "answers"]
        read_only_fields = ["text", "hint", "index", "type", "status"]

    def save(self):
        answers = self.validated_data["answers"]
        for answer_dict in answers:
            answer = Answer.objects.filter(id=answer_dict["id"]).first()
            if answer is None:
                raise serializers.ValidationError("The answer does not exist")
            if answer.question_id != self.instance.id:
                raise serializers.ValidationError(
                    "The answer does not belong to this question."
                )
            answer.selected = answer_dict["selected"]
            answer.user_text = answer_dict["user_text"]
            answer.save()


class TokenSerializer(serializers.Serializer):
    questionnaire_id = serializers.IntegerField()