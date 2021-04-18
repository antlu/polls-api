from rest_framework import serializers

from polls.models import Answer, Poll, Question


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
