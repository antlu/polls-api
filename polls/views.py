from rest_framework import generics

from polls.models import CompletedPoll, Poll
from polls.serializers import (
    CompletedPollSerializer, PollSerializer,
)


class PollList(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class PollDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class CompletedPollList(generics.ListCreateAPIView):
    queryset = CompletedPoll.objects.all()
    serializer_class = CompletedPollSerializer
