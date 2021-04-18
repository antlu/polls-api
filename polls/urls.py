from django.urls import path

from polls.views import PollDetail, PollList

urlpatterns = [
    path('polls/', PollList.as_view(), name='poll-list'),
    path('polls/<int:pk>', PollDetail.as_view(), name='poll-detail'),
]
