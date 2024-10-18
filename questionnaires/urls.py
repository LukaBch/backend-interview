from rest_framework.routers import DefaultRouter
from django.urls import path

from questionnaires.views import QuestionViewSet, QuestionnaireViewSet, TokenCreateView

router = DefaultRouter()
router.register(r"questions", QuestionViewSet, basename="questions")
router.register(r"questionnaires", QuestionnaireViewSet, basename="questionnaires")
urlpatterns = router.urls + [
    path('token/', TokenCreateView.as_view(), name='create-token'),
]
