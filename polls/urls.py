from django.urls import path

from polls.views import (
    ActivePollList, CompletedPollList, PollDetail, PollList, QuestionDetail, home
)

urlpatterns = [
    path('polls/', PollList.as_view(), name='poll-list'),
    path('polls/<int:pk>', PollDetail.as_view(), name='poll-detail'),
    path('questions/<int:pk>', QuestionDetail.as_view(), name='question-detail'),
    path('results/', CompletedPollList.as_view(), name='completed-poll-list'),
    path('active-polls/', ActivePollList.as_view(), name='active-poll-list'),
    path('', home, name='home')
]
