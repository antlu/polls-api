from django.db import models
from django.utils import timezone

TEXT_LENGTH = 255


class Poll(models.Model):
    title = models.CharField(max_length=TEXT_LENGTH)
    start_time = models.DateTimeField(default=timezone.localtime)
    end_time = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return self.title


class Question(models.Model):
    TYPES = (
        ('text', 'Text'),
        ('single_choice', 'Single choice'),
        ('multi_choice', 'Multiple choice'),
    )

    poll = models.ForeignKey(Poll, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=TEXT_LENGTH)
    type = models.CharField(max_length=20, choices=TYPES, default='text')

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=TEXT_LENGTH)

    def __str__(self):
        return self.text


class CompletedPoll(models.Model):
    user = models.IntegerField()
    poll = models.ForeignKey(Poll, on_delete=models.PROTECT)

    def __str__(self):
        return self.poll.title


class UserAnswer(models.Model):
    completed_poll = models.ForeignKey(CompletedPoll, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    answer = models.TextField()
