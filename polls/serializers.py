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
