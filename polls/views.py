from django.utils import timezone
from rest_framework import generics

from polls.models import CompletedPoll, Poll, Question
from polls.permissions import ReadOnly
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
    serializer_class = CompletedPollSerializer

    def get_queryset(self):
        queryset = CompletedPoll.objects.all()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return queryset.filter(user=user_id)
        return queryset


class ActivePollList(generics.ListCreateAPIView):
    current_time = timezone.now()
    queryset = Poll.objects.filter(
        start_time__lte=current_time, end_time__gte=current_time,
    )
    serializer_class = PollSerializer
    permission_classes = (ReadOnly,)
