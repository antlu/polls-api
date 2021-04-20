from rest_framework import generics

from polls.models import CompletedPoll, Poll, Question
from polls.serializers import (
    CompletedPollSerializer, PollSerializer, QuestionSerializer,
)


class PollList(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class PollDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class CompletedPollList(generics.ListCreateAPIView):
    queryset = CompletedPoll.objects.all()
    serializer_class = CompletedPollSerializer
