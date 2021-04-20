from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers

from polls.models import Answer, CompletedPoll, Poll, Question, UserAnswer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Answer
        exclude = ('question', 'id')


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, required=False)

    class Meta(object):
        model = Question
        exclude = ('poll',)

    def validate(self, data):
        if data['type'] == 'text':
            if data['answers']:
                raise serializers.ValidationError(
                    "Text question cannot have answers.",
                )
        elif not data['answers']:
            raise serializers.ValidationError(
                "Non-text question must have answers.",
            )
        return data


def add_questions(poll, questions_data):
    for question_data in questions_data:
        answers_data = question_data.pop('answers', {})
        question = Question.objects.create(poll=poll, **question_data)
        for answer_data in answers_data:
            Answer.objects.create(question=question, **answer_data)


class PollSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='poll-detail')
    questions = QuestionSerializer(many=True)

    class Meta(object):
        model = Poll
        fields = '__all__'

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        poll = Poll.objects.create(**validated_data)
        add_questions(poll, questions_data)
        return poll

    def update(self, instance, validated_data):
        instance.questions.all().delete()
        add_questions(instance, validated_data['questions'])
        instance.title = validated_data['title']
        instance.end_time = validated_data['end_time']
        instance.description = validated_data['description']
        instance.save()
        return instance

    def validate_questions(self, questions):
        if not questions:
            raise serializers.ValidationError(
                "Poll must have questions.",
            )
        return questions

    def validate_start_time(self, datetime):
        if self.instance:
            raise serializers.ValidationError(
                "Start time cannot be changed.",
            )
        return datetime


class UserAnswerSerializer(serializers.ModelSerializer):
    question = serializers.StringRelatedField()
    question_id = serializers.IntegerField()

    class Meta(object):
        model = UserAnswer
        exclude = ('completed_poll', 'id')


class CompletedPollSerializer(serializers.ModelSerializer):
    answers = UserAnswerSerializer(many=True)
    poll = serializers.HyperlinkedRelatedField(view_name='poll-detail', read_only=True)
    poll_id = serializers.IntegerField()

    class Meta(object):
        model = CompletedPoll
        exclude = ('id',)

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        completed_poll = CompletedPoll.objects.create(**validated_data)
        for answer_data in answers_data:
            UserAnswer.objects.create(completed_poll=completed_poll, **answer_data)
        return completed_poll

    def validate_answers(self, answers):
        if not answers:
            raise serializers.ValidationError(
                "Poll must have answers.",
            )
        return answers

    def validate(self, data):
        poll = get_object_or_404(Poll, pk=data['poll_id'])

        current_time = timezone.now()
        if current_time < poll.start_time or current_time > poll.end_time:
            raise serializers.ValidationError(
                "Can't participate in inactive polls.",
            )

        if not all(
            poll.questions.filter(id=answer_data['question_id']).exists()
            for answer_data in data['answers']
        ):
            raise serializers.ValidationError(
                "Questions must belong to the poll {}.".format(poll.id),
            )

        return data
