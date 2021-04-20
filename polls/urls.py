from django.urls import path

from polls.views import CompletedPollList, PollDetail, PollList, QuestionDetail

urlpatterns = [
    path('polls/', PollList.as_view(), name='poll-list'),
    path('polls/<int:pk>', PollDetail.as_view(), name='poll-detail'),
    path('questions/<int:pk>', QuestionDetail.as_view(), name='question-detail'),
    path('results/', CompletedPollList.as_view(), name='completed-poll-list'),
]
