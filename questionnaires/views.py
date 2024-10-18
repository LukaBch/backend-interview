from rest_framework.mixins import ListModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from .models import ExpiringToken
from questionnaires.models import ExpiringToken, Questionnaire, Question
from questionnaires.serializers import (
    QuestionnaireSerializer,
    QuestionSerializer,
    TokenSerializer,
)


class QuestionnaireViewSet(ListModelMixin, GenericViewSet):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class QuestionViewSet(ListModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Question.objects.all().prefetch_related("answers")
    serializer_class = QuestionSerializer
    filterset_fields = ["questionnaire"]

    def get_queryset(self):
        if isinstance(self.request.auth, ExpiringToken):
            return super().get_queryset().filter(questionnaire=self.request.auth.questionnaire)
        return super().get_queryset().filter(questionnaire__user=self.request.user)


class TokenCreateView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = TokenSerializer

    def post(self, request):
        questionnaire_id = request.data.get("questionnaire_id")
        try:
            questionnaire = Questionnaire.objects.get(id=questionnaire_id)
        except Questionnaire.DoesNotExist:
            return Response({"error": "Questionnaire not found."}, status=status.HTTP_404_NOT_FOUND)

        expiring_token = ExpiringToken.objects.create(questionnaire=questionnaire)

        return Response({"token": expiring_token.key}, status=status.HTTP_201_CREATED)